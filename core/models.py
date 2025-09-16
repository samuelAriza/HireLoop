from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    @property
    def has_freelancer_profile(self):
        return hasattr(self, 'freelancerprofile')

    @property
    def has_client_profile(self):
        return hasattr(self, 'clientprofile')

    @property
    def user_roles(self):
        roles = []
        if self.has_freelancer_profile:
            roles.append('Freelancer')
        if self.has_client_profile:
            roles.append('Cliente')
        return roles

    @property
    def primary_role(self):
        roles = self.user_roles
        if len(roles) == 1:
            return roles[0]
        elif len(roles) > 1:
            return "Múltiples roles"
        return "Sin rol asignado"


class FreelancerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancerprofile")
    skills = models.JSONField(default=list, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Freelancer: {self.user.username}"


class ClientProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="clientprofile")
    company = models.CharField(max_length=255, blank=True)
    billing_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cliente: {self.user.username}"