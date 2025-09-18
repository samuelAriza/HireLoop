from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        help_text="Upload a profile image",
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    
    def get_roles(self):
        roles = []
        if hasattr(self, 'freelancer_profile'):
            roles.append('Freelancer')
        if hasattr(self, 'client_profile'):
            roles.append('Client')
        return roles
    
    def get_profile_image_url(self):
        from .services.image_service import ProfileImageService
        service = ProfileImageService()
        return service.get_image_url(self.profile_image.url if self.profile_image else None)

class FreelancerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    bio = models.TextField(max_length=500, blank=True)
    skills = models.CharField(
        max_length=500, 
        blank=True, 
        help_text="Enter skills separated by commas",
        verbose_name="Skills"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"FreelancerProfile of {self.user.email}"
    
class ClientProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    company = models.CharField(max_length=100, blank=True)
    billing_address = models.TextField(blank=True)
    billing_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ClientProfile of {self.user.email}"