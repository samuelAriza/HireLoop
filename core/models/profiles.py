from django.db import models
import uuid
from .user import User

# Profile models for HireLoop platform
# Follows SRP: Each profile model handles specific user role data
# Applies DRY: Common patterns like UUID primary keys and timestamps


class FreelancerProfile(models.Model):
    """
    Profile model for freelancers in the HireLoop platform.
    
    Extends User model with freelancer-specific information like skills and bio.
    Uses OneToOne relationship to maintain single freelancer profile per user.
    Follows SRP: Only handles freelancer-related data and behavior.
    """
    
    # UUID primary key for enhanced security and scalability
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # One-to-one relationship with User model
    # CASCADE ensures profile is deleted when user is deleted
    # related_name allows access via user.freelancerprofile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancerprofile")
    
    # JSON field to store list of skills (e.g., ["Python", "Django", "React"])
    # Default empty list, allows flexible skill management
    skills = models.JSONField(default=list, blank=True)
    
    # Biography text field with reasonable character limit
    # Allows freelancers to describe their experience and expertise
    bio = models.TextField(max_length=1000, blank=True)
    
    # Automatic timestamp fields for audit trail
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)      # Updated on every save

    def __str__(self):
        """String representation showing freelancer status and username"""
        return f"Freelancer: {self.user.username}"


class ClientProfile(models.Model):
    """
    Profile model for clients in the HireLoop platform.
    
    Extends User model with client-specific information like company and billing details.
    Uses OneToOne relationship to maintain single client profile per user.
    Follows SRP: Only handles client-related data and billing information.
    """
    
    # UUID primary key for enhanced security and scalability
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # One-to-one relationship with User model
    # CASCADE ensures profile is deleted when user is deleted
    # related_name allows access via user.clientprofile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="clientprofile")
    
    # Optional company name field
    # Allows clients to associate projects with their company
    company = models.CharField(max_length=255, blank=True)
    
    # Optional separate billing email
    # Useful for companies that use different emails for billing/accounting
    billing_email = models.EmailField(blank=True)
    
    # Automatic timestamp fields for audit trail
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)      # Updated on every save

    def __str__(self):
        """String representation showing client status and username"""
        return f"Client: {self.user.username}"