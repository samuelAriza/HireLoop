import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import ClientProfile, FreelancerProfile
from core.interfaces import PurchasableInterface
from .services.image_service import MentorshipImageService


class MentorshipSession(models.Model):
    class MentorshipStatus(models.TextChoices):
        SCHEDULED = "scheduled", _("Scheduled")
        COMPLETED = "completed", _("Completed")
        CANCELED = "canceled", _("Canceled")
        NO_SHOW = "no_show", _("No Show")

    PRICE_PER_MINUTE = Decimal("2.50")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(
        max_length=255,
        verbose_name=_("Topic"),
        help_text=_("The main topic of the mentorship session"),
    )
    start_time = models.DateTimeField(
        verbose_name=_("Start Time"),
        help_text=_("When the session will begin"),
    )
    duration_minutes = models.PositiveIntegerField(
        verbose_name=_("Duration (minutes)"),
        help_text=_("How long the session will last in minutes"),
    )
    mentor = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="mentorship_sessions",
        verbose_name=_("Mentor"),
    )
    mentee = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="mentorship_bookings",
        verbose_name=_("Mentee"),
    )
    status = models.CharField(
        max_length=20,
        choices=MentorshipStatus.choices,
        default=MentorshipStatus.SCHEDULED,
        verbose_name=_("Status"),
    )
    image_path = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Image Path"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Mentorship Session")
        verbose_name_plural = _("Mentorship Sessions")
        ordering = ["-start_time"]

    def __str__(self):
        return f"{self.topic} - ({self.get_status_display()})"

    def get_price(self) -> float:
        """Calculate total price based on duration and price per minute."""
        return float(self.PRICE_PER_MINUTE * self.duration_minutes)

    def get_title(self) -> str:
        return _("Mentorship: {topic}").format(topic=self.topic)

    def get_description(self) -> str:
        return _(
            "Mentorship session about '{topic}', duration {duration} minutes."
        ).format(topic=self.topic, duration=self.duration_minutes)

    def get_type(self) -> str:
        return _("Mentorship")

    def get_image_path(self) -> str:
        image_service = MentorshipImageService()
        return image_service.get_image_url(self.image_path)