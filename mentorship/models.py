from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid


class MentorshipSession(models.Model):
    """
    Modelo para sesiones de mentoría 1:1.
    Sigue SRP: Solo maneja datos y lógica de sesiones de mentoría.
    """
    # Estados de la sesión
    AVAILABLE = 'AVAILABLE'
    BOOKED = 'BOOKED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    
    STATUS_CHOICES = [
        (AVAILABLE, 'Disponible'),
        (BOOKED, 'Reservada'),
        (COMPLETED, 'Completada'),
        (CANCELLED, 'Cancelada'),
    ]
    
    # Categorías de mentoría
    CATEGORY_CHOICES = [
        ('programming', 'Programación'),
        ('design', 'Diseño'),
        ('business', 'Negocios'),
        ('marketing', 'Marketing'),
        ('career', 'Desarrollo de Carrera'),
        ('freelancing', 'Freelancing'),
        ('technology', 'Tecnología'),
        ('other', 'Otros'),
    ]
    
    # Campos del modelo
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        'core.FreelancerProfile', 
        on_delete=models.CASCADE, 
        related_name='mentorship_sessions'
    )
    mentee = models.ForeignKey(
        'core.FreelancerProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mentee_sessions'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.PositiveIntegerField(help_text="Duración en horas")
    
    # Programación de la sesión
    scheduled_datetime = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora programada para la sesión")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    
    # Información adicional
    meeting_link = models.URLField(blank=True, help_text="Link de reunión (Zoom, Meet, etc.)")
    notes = models.TextField(blank=True, help_text="Notas adicionales para la sesión")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sesión de Mentoría'
        verbose_name_plural = 'Sesiones de Mentoría'
    
    def clean(self):
        """Validaciones del modelo"""
        if self.price is not None and self.price <= 0:
            raise ValidationError("El precio debe ser mayor a 0")
        
        if self.duration_hours is not None and self.duration_hours <= 0:
            raise ValidationError("La duración debe ser mayor a 0 horas")
        
        if self.mentor_id and self.mentee_id and self.mentor_id == self.mentee_id:
            raise ValidationError("El mentor no puede ser el mismo que el mentee")
        
        if self.scheduled_datetime and self.scheduled_datetime <= timezone.now():
            raise ValidationError("La fecha programada debe ser en el futuro")

    
    def __str__(self):
        return f"{self.title} - {self.mentor.user.username}"
    
    @property
    def is_available(self):
        """Verifica si la sesión está disponible para reservar"""
        return self.status == self.AVAILABLE and self.mentee is None
    
    @property
    def is_booked(self):
        """Verifica si la sesión está reservada"""
        return self.status == self.BOOKED and self.mentee is not None
    
    @property
    def duration_display(self):
        """Muestra la duración en formato legible"""
        if self.duration_hours == 1:
            return "1 hora"
        return f"{self.duration_hours} horas"
    
    def book_session(self, mentee_profile):
        """Reserva la sesión para un mentee"""
        if not self.is_available:
            raise ValidationError("Esta sesión no está disponible")
        
        if self.mentor == mentee_profile:
            raise ValidationError("No puedes reservar tu propia sesión")
        
        self.mentee = mentee_profile
        self.status = self.BOOKED
        self.save()
    
    def complete_session(self):
        """Marca la sesión como completada"""
        if self.status != self.BOOKED:
            raise ValidationError("Solo se pueden completar sesiones reservadas")
        
        self.status = self.COMPLETED
        self.save()
    
    def cancel_session(self):
        """Cancela la sesión"""
        if self.status == self.COMPLETED:
            raise ValidationError("No se puede cancelar una sesión completada")
        
        self.status = self.CANCELLED
        self.mentee = None
        self.scheduled_datetime = None
        self.save()


class MentorshipReview(models.Model):
    """
    Modelo para reseñas de sesiones de mentoría.
    Sigue SRP: Solo maneja reseñas y calificaciones.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(MentorshipSession, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey('core.FreelancerProfile', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Calificación de 1 a 5 estrellas"
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reseña de Mentoría'
        verbose_name_plural = 'Reseñas de Mentoría'
    
    def clean(self):
        """Validaciones de la reseña"""
        if self.session.status != MentorshipSession.COMPLETED:
            raise ValidationError("Solo se pueden reseñar sesiones completadas")
        
        if self.reviewer not in [self.session.mentor, self.session.mentee]:
            raise ValidationError("Solo el mentor o mentee pueden reseñar la sesión")
    
    def __str__(self):
        return f"Review by {self.reviewer.user.username} for {self.mentorship.title}"


# Modelos para carrito y wishlist de mentorías
# Aplicando principios SOLID: SRP (cada modelo tiene una responsabilidad específica)
class MentorshipCartItem(models.Model):
    """
    Item de mentoría en el carrito.
    Mantiene relación directa sin Generic Foreign Keys para seguir SOLID.
    """
    cart = models.ForeignKey(
        'services.Cart', 
        on_delete=models.CASCADE, 
        related_name='mentorship_items'
    )
    mentorship = models.ForeignKey(
        'MentorshipSession', 
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'mentorship']
        verbose_name = "Item de Mentoría en Carrito"
        verbose_name_plural = "Items de Mentorías en Carrito"
    
    def __str__(self):
        return f"{self.cart.user.username} - {self.mentorship.title}"


class MentorshipWishlistItem(models.Model):
    """
    Item de mentoría en la wishlist.
    Mantiene relación directa sin Generic Foreign Keys para seguir SOLID.
    """
    wishlist = models.ForeignKey(
        'services.Wishlist', 
        on_delete=models.CASCADE, 
        related_name='mentorship_items'
    )
    mentorship = models.ForeignKey(
        'MentorshipSession', 
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['wishlist', 'mentorship']
        verbose_name = "Item de Mentoría en Wishlist"
        verbose_name_plural = "Items de Mentorías en Wishlist"
    
    def __str__(self):
        return f"{self.wishlist.user.username} - {self.mentorship.title}"
