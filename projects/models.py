import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import ClientProfile, FreelancerProfile
from .services.image_service import ProjectImageService


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        CREATED = "CREATED", _("Created")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        DELIVERED = "DELIVERED", _("Delivered")
        CANCELLED = "CANCELLED", _("Cancelled")
        COMPLETED = "COMPLETED", _("Completed")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, verbose_name=_("client"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    description = models.TextField(blank=True, verbose_name=_("description"))
    status = models.CharField(
        max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.CREATED, verbose_name=_("status")
    )
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("budget"))
    image_path = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("image path"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def get_image_path(self) -> str:
        image_service = ProjectImageService()
        return image_service.get_image_url(self.image_path)


class ProjectAssignment(models.Model):
    class ProjectAssignmentStatus(models.TextChoices):
        INVITED = "INVITED", _("Invited")
        ACCEPTED = "ACCEPTED", _("Accepted")
        REJECTED = "REJECTED", _("Rejected")
        REMOVED = "REMOVED", _("Removed")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="assignments", verbose_name=_("project")
    )
    freelancer = models.ForeignKey(
        FreelancerProfile, on_delete=models.CASCADE, related_name="assignments", verbose_name=_("freelancer")
    )
    role = models.CharField(max_length=100, blank=True, verbose_name=_("role"))
    agreed_payment = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, default=0, verbose_name=_("agreed payment")
    )
    status = models.CharField(
        max_length=20,
        choices=ProjectAssignmentStatus.choices,
        default=ProjectAssignmentStatus.INVITED,
        verbose_name=_("status"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("project assignment")
        verbose_name_plural = _("project assignments")

    def __str__(self):
        return f"{self.freelancer.user.email} - {self.project.title} ({self.get_status_display()})"


class ProjectApplication(models.Model):
    class ApplicationStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        ACCEPTED = "ACCEPTED", _("Accepted")
        REJECTED = "REJECTED", _("Rejected")
        WITHDRAWN = "WITHDRAWN", _("Withdrawn")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="applications", verbose_name=_("project")
    )
    freelancer = models.ForeignKey(
        FreelancerProfile, on_delete=models.CASCADE, related_name="applications", verbose_name=_("freelancer")
    )
    cover_letter = models.TextField(blank=True, verbose_name=_("cover letter"))
    proposed_payment = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=_("proposed payment")
    )
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
        verbose_name=_("status"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        unique_together = ("project", "freelancer")  # Evita aplicaciones duplicadas
        verbose_name = _("project application")
        verbose_name_plural = _("project applications")

    def __str__(self):
        return f"Application from {self.freelancer.user.email} to {self.project.title} ({self.get_status_display()})"