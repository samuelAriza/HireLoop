import uuid
from decimal import Decimal
from django.db import models
from core.models import ClientProfile, FreelancerProfile
from core.interfaces import PurchasableInterface
from .services.image_service import MentorshipImageService

class MentorshipSession(models.Model):
    class MentorshipStatus(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"
        NO_SHOW = "no_show", "No Show"

    PRICE_PER_MINUTE = Decimal("2.50")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    mentor = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    mentee = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=20,
        choices=MentorshipStatus.choices,
        default=MentorshipStatus.SCHEDULED,
    )
    image_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} - ({self.get_status_display()})"

    def get_price(self) -> float:
        return float(self.PRICE_PER_MINUTE * self.duration_minutes)

    def get_title(self) -> str:
        return f"Mentorship: {self.topic}"

    def get_description(self) -> str:
        return f"Mentorship session about '{self.topic}', duration {self.duration_minutes} minutes."

    def get_type(self) -> str:
        return "Mentorship"

    def get_image_path(self) -> str:
        image_service = MentorshipImageService()
        return image_service.get_image_url(self.image_path)
