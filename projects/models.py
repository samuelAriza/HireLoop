from django.db import models
from django.core.exceptions import ValidationError
from core.models import ClientProfile, FreelancerProfile
import uuid


class Project(models.Model):
    """
    Modelo Project mejorado con freelancer asignado.
    Sigue SRP: Solo maneja datos y lógica de negocio de proyectos.
    """
    # Estados del proyecto
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    
    STATE_CHOICES = [
        (OPEN, 'Abierto'),
        (IN_PROGRESS, 'En Progreso'),
        (COMPLETED, 'Completado'),
        (CANCELLED, 'Cancelado'),
    ]
    
    # Campos del modelo
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey('core.ClientProfile', on_delete=models.CASCADE, related_name='projects')
    assigned_freelancer = models.ForeignKey(
        'core.FreelancerProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_projects',
        help_text="Freelancer asignado al proyecto"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
    
    def __str__(self):
        return self.title
    
    @property
    def is_open(self):
        """Verifica si el proyecto está abierto para aplicaciones"""
        return self.state == self.OPEN
    
    @property
    def is_assigned(self):
        """Verifica si el proyecto tiene un freelancer asignado"""
        return self.assigned_freelancer is not None
    
    @property
    def applications_count(self):
        """Cuenta total de aplicaciones al proyecto"""
        return self.applications.count()
    
    def assign_freelancer(self, freelancer_profile):
        """Asigna un freelancer al proyecto y cambia estado a EN_PROGRESO"""
        if not isinstance(freelancer_profile, FreelancerProfile):
            raise ValidationError("Solo se pueden asignar FreelancerProfiles")
        
        self.assigned_freelancer = freelancer_profile
        self.state = self.IN_PROGRESS
        self.save()
    
    def complete_project(self):
        """Marca el proyecto como completado"""
        if self.state != self.IN_PROGRESS:
            raise ValidationError("Solo se pueden completar proyectos en progreso")
        
        self.state = self.COMPLETED
        self.save()
    
    def cancel_project(self):
        """Cancela el proyecto"""
        if self.state == self.COMPLETED:
            raise ValidationError("No se puede cancelar un proyecto completado")
        
        self.state = self.CANCELLED
        self.assigned_freelancer = None
        self.save()


class ProjectApplication(models.Model):
    """
    Modelo para aplicaciones de freelancers a proyectos.
    Sigue SRP: Solo maneja aplicaciones.
    """
    # Estados de la aplicación
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (ACCEPTED, 'Aceptada'),
        (REJECTED, 'Rechazada'),
    ]
    
    # Campos del modelo
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey('core.FreelancerProfile', on_delete=models.CASCADE, related_name='project_applications')
    message = models.TextField(blank=True, help_text="Mensaje opcional del freelancer")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['project', 'freelancer']  # Un freelancer solo puede aplicar una vez
        verbose_name = 'Aplicación al Proyecto'
        verbose_name_plural = 'Aplicaciones a Proyectos'
    
    def __str__(self):
        return f"{self.freelancer.user.username} -> {self.project.title}"
    
    @property
    def is_pending(self):
        """Verifica si la aplicación está pendiente"""
        return self.status == self.PENDING
    
    @property
    def is_accepted(self):
        """Verifica si la aplicación fue aceptada"""
        return self.status == self.ACCEPTED
    
    @property
    def is_rejected(self):
        """Verifica si la aplicación fue rechazada"""
        return self.status == self.REJECTED
    
    def accept(self):
        """Acepta la aplicación y asigna el freelancer al proyecto"""
        if self.status != self.PENDING:
            raise ValidationError("Solo se pueden aceptar aplicaciones pendientes")
        
        # Marcar esta aplicación como aceptada
        self.status = self.ACCEPTED
        self.save()
        
        # Asignar freelancer al proyecto
        self.project.assign_freelancer(self.freelancer)
        
        # Rechazar todas las otras aplicaciones
        other_applications = ProjectApplication.objects.filter(
            project=self.project,
            status=self.PENDING
        ).exclude(id=self.id)
        
        other_applications.update(status=self.REJECTED)
    
    def reject(self):
        """Rechaza la aplicación"""
        if self.status != self.PENDING:
            raise ValidationError("Solo se pueden rechazar aplicaciones pendientes")
        
        self.status = self.REJECTED
        self.save()


