from decimal import Decimal
from django.db import models
import uuid
from core.models import FreelancerProfile
from core.interfaces import PurchasableInterface
from .services.image_service import MicroserviceImageService


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class MicroService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    freelancer = models.ForeignKey(
        FreelancerProfile, on_delete=models.CASCADE, related_name="microservices"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="microservices"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    delivery_time = models.PositiveIntegerField(help_text="Delivery time in days")
    is_active = models.BooleanField(default=True)
    image_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.freelancer.user.email}"

    def get_price(self) -> float:
        return float(self.price)

    def get_title(self) -> str:
        return self.title

    def get_description(self) -> str:
        return self.description

    def get_type(self) -> str:
        return "MicroService"

    def get_image_path(self) -> str:
        image_service = MicroserviceImageService()
        return image_service.get_image_url(self.image_path)
