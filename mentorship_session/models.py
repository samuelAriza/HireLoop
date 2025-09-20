import uuid
from django.db import models
from core.models import ClientProfile, FreelancerProfile

class MentorshipSession(models.Model):
    class MentorshipStatus(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'
        NO_SHOW = 'no_show', 'No Show'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    mentor = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    mentee = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=MentorshipStatus.choices, default=MentorshipStatus.SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.topic} - ({self.get_status_display()})"