import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import FreelancerProfile
from core.interfaces import PurchasableInterface
from .services.image_service import MicroserviceImageService


class Category(models.Model):
    """
    Represents a category for microservices (e.g., Web Development, Graphic Design).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID")
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name"),
        help_text=_("Enter a unique category name.")
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly version of the name.")
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class MicroService(models.Model):
    """
    Represents a small, fixed-price service offered by a freelancer.
    Implements PurchasableInterface for cart/wishlist integration.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID")
    )
    freelancer = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="microservices",
        verbose_name=_("Freelancer"),
        help_text=_("The freelancer offering this microservice.")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="microservices",
        verbose_name=_("Category"),
        help_text=_("Select the category that best fits this service.")
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("A clear, compelling title for your service.")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Describe what you offer, what’s included, and any requirements.")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Price (USD)"),
        help_text=_("Fixed price for this service in USD.")
    )
    delivery_time = models.PositiveIntegerField(
        verbose_name=_("Delivery Time (days)"),
        help_text=_("How many days it takes to deliver the final work.")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Uncheck to hide this service from the marketplace.")
    )
    image_path = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Image Path"),
        help_text=_("Path to the uploaded service image.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("MicroService")
        verbose_name_plural = _("MicroServices")
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=Decimal("0.00")),
                name="microservice_price_non_negative"
            ),
            models.CheckConstraint(
                check=models.Q(delivery_time__gte=1),
                name="microservice_delivery_time_positive"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.title} - {self.freelancer.user.get_full_name() or self.freelancer.user.username}"

    def get_price(self) -> float:
        """Return price as float for PurchasableInterface."""
        return float(self.price)

    def get_title(self) -> str:
        """Return service title."""
        return self.title

    def get_description(self) -> str:
        """Return service description."""
        return self.description

    def get_type(self) -> str:
        """Return type identifier for cart/wishlist."""
        return _("MicroService")

    def get_image_path(self) -> str:
        """Return full image URL or default placeholder."""
        image_service = MicroserviceImageService()
        return image_service.get_image_url(self.image_path)