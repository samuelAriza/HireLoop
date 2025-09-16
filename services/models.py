from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid


class Service(models.Model):
    """
    Modelo de Servicio que ofrece un freelancer.
    Sigue SRP: Solo maneja datos y lógica de servicios.
    """
    # Categorías de servicios
    CATEGORY_CHOICES = [
        ('web_dev', 'Desarrollo Web'),
        ('mobile_dev', 'Desarrollo Mobile'),
        ('design', 'Diseño Gráfico'),
        ('writing', 'Redacción'),
        ('marketing', 'Marketing Digital'),
        ('translation', 'Traducción'),
        ('video', 'Video y Animación'),
        ('music', 'Audio y Música'),
        ('programming', 'Programación'),
        ('data', 'Análisis de Datos'),
        ('other', 'Otros'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    freelancer = models.ForeignKey('core.FreelancerProfile', on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.PositiveIntegerField(help_text="Días de entrega")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
    
    def clean(self):
        if self.price <= 0:
            raise ValidationError("El precio debe ser mayor a 0")
        if self.delivery_time <= 0:
            raise ValidationError("El tiempo de entrega debe ser mayor a 0")
    
    def __str__(self):
        return self.title


class Cart(models.Model):
    """
    Modelo para carrito de compras.
    Sigue SRP: Solo maneja items del carrito.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
    
    def __str__(self):
        return f"Carrito de {self.user.username}"
    
    @property
    def total_items(self):
        """Cuenta total de items en el carrito"""
        return self.items.count()
    
    @property
    def total_price(self):
        """Precio total del carrito"""
        total = 0
        for item in self.items.all():
            if hasattr(item.content_object, 'price'):
                total += item.content_object.price
        return total
    
    def add_item(self, content_object):
        """Agrega un item genérico al carrito (servicio o mentoría)"""
        if not hasattr(content_object, 'price'):
            raise ValidationError("El objeto debe tener precio")
        
        # Verificar que el usuario no sea el creador
        if hasattr(content_object, 'freelancer'):
            if content_object.freelancer.user == self.user:
                raise ValidationError("No puedes agregar tus propios items al carrito")
        elif hasattr(content_object, 'mentor'):
            if content_object.mentor.user == self.user:
                raise ValidationError("No puedes agregar tus propias mentorías al carrito")
        
        # Para mentorías, verificar disponibilidad
        if hasattr(content_object, 'is_available'):
            if not content_object.is_available:
                raise ValidationError("Esta mentoría no está disponible")
        
        # Crear o obtener el item del carrito
        content_type = ContentType.objects.get_for_model(content_object)
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            content_type=content_type,
            object_id=content_object.id
        )
        
        return cart_item
    
    def remove_item(self, content_object):
        """Remueve un item del carrito"""
        content_type = ContentType.objects.get_for_model(content_object)
        CartItem.objects.filter(
            cart=self,
            content_type=content_type,
            object_id=content_object.id
        ).delete()
    
    def clear(self):
        """Vacía el carrito"""
        self.items.all().delete()


class CartItem(models.Model):
    """
    Item individual del carrito (genérico para servicios y mentorías).
    Sigue SRP: Solo maneja relación entre carrito y objeto comprable.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    
    # Generic relation para servicios y mentorías
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'content_type', 'object_id']
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
    
    def __str__(self):
        item_name = getattr(self.content_object, 'title', str(self.content_object))
        return f"{item_name} en carrito de {self.cart.user.username}"


class Wishlist(models.Model):
    """
    Modelo para lista de deseos.
    Sigue SRP: Solo maneja servicios y mentorías favoritos.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lista de Deseos'
        verbose_name_plural = 'Listas de Deseos'
    
    def __str__(self):
        return f"Wishlist de {self.user.username}"
    
    @property
    def total_items(self):
        """Cuenta total de items en la wishlist"""
        return self.items.count()
    
    def add_item(self, content_object):
        """Agrega un item genérico a la wishlist"""
        if hasattr(content_object, 'active') and not content_object.active:
            raise ValidationError("No se pueden agregar items inactivos a la wishlist")
        
        # Para mentorías, verificar disponibilidad
        if hasattr(content_object, 'is_available'):
            if not content_object.is_available:
                raise ValidationError("No se pueden agregar mentorías no disponibles a la wishlist")
        
        # Crear o obtener el item de wishlist
        content_type = ContentType.objects.get_for_model(content_object)
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=self,
            content_type=content_type,
            object_id=content_object.id
        )
        
        return wishlist_item
    
    def remove_item(self, content_object):
        """Remueve un item de la wishlist"""
        content_type = ContentType.objects.get_for_model(content_object)
        WishlistItem.objects.filter(
            wishlist=self,
            content_type=content_type,
            object_id=content_object.id
        ).delete()
    
    def clear(self):
        """Vacía la wishlist"""
        self.items.all().delete()


class WishlistItem(models.Model):
    """
    Item individual de la wishlist (genérico para servicios y mentorías).
    Sigue SRP: Solo maneja relación entre wishlist y objeto favorito.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    
    # Generic relation para servicios y mentorías
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['wishlist', 'content_type', 'object_id']
        verbose_name = 'Item de Wishlist'
        verbose_name_plural = 'Items de Wishlist'
    
    def __str__(self):
        item_name = getattr(self.content_object, 'title', str(self.content_object))
        return f"{item_name} en wishlist de {self.wishlist.user.username}"


class Cart(models.Model):
    """
    Modelo para carrito de compras.
    Sigue SRP: Solo maneja items del carrito.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
    
    def __str__(self):
        return f"Carrito de {self.user.username}"
    
    @property
    def total_items(self):
        """Cuenta total de items en el carrito"""
        return self.items.count()
    
    @property
    def total_price(self):
        """Precio total del carrito"""
        return sum(item.service.price for item in self.items.all())
    
    def add_service(self, service):
        """Agrega un servicio al carrito"""
        if not service.active:
            raise ValidationError("No se pueden agregar servicios inactivos")
        
        # Verificar que el usuario no sea el creador del servicio
        if service.freelancer.user == self.user:
            raise ValidationError("No puedes agregar tus propios servicios al carrito")
        
        # Crear o obtener el item del carrito
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            service=service
        )
        
        return cart_item
    
    def remove_service(self, service):
        """Remueve un servicio del carrito"""
        CartItem.objects.filter(cart=self, service=service).delete()
    
    def clear(self):
        """Vacía el carrito"""
        self.items.all().delete()


class CartItem(models.Model):
    """
    Item individual del carrito.
    Sigue SRP: Solo maneja relación entre carrito y servicio.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'service']
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
    
    def __str__(self):
        return f"{self.service.title} en carrito de {self.cart.user.username}"


class Wishlist(models.Model):
    """
    Modelo para lista de deseos.
    Sigue SRP: Solo maneja servicios favoritos.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lista de Deseos'
        verbose_name_plural = 'Listas de Deseos'
    
    def __str__(self):
        return f"Wishlist de {self.user.username}"
    
    @property
    def total_items(self):
        """Cuenta total de items en la wishlist"""
        return self.items.count()
    
    def add_service(self, service):
        """Agrega un servicio a la wishlist"""
        if not service.active:
            raise ValidationError("No se pueden agregar servicios inactivos a la wishlist")
        
        # Crear o obtener el item de wishlist
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=self,
            service=service
        )
        
        return wishlist_item
    
    def remove_service(self, service):
        """Remueve un servicio de la wishlist"""
        WishlistItem.objects.filter(wishlist=self, service=service).delete()
    
    def clear(self):
        """Vacía la wishlist"""
        self.items.all().delete()


class WishlistItem(models.Model):
    """
    Item individual de la wishlist.
    Sigue SRP: Solo maneja relación entre wishlist y servicio.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['wishlist', 'service']
        verbose_name = 'Item de Wishlist'
        verbose_name_plural = 'Items de Wishlist'
    
    def __str__(self):
        return f"{self.service.title} en wishlist de {self.wishlist.user.username}"