import uuid
from django.db import models
from core.models import ClientProfile, FreelancerProfile

class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        CREATED = "CREATED", "Created"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.CREATED)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class ProjectAssignment(models.Model):
    class ProjectAssignmentStatus(models.TextChoices):
        INVITED = "INVITED", "Invited"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        REMOVED = "REMOVED", "Removed"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="assignments")
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="assignments")
    role = models.CharField(max_length=100, blank=True)
    agreed_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
    status = models.CharField(max_length=20, choices=ProjectAssignmentStatus.choices, default=ProjectAssignmentStatus.INVITED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.freelancer.user.email} - {self.project.title} ({self.get_status_display()})"