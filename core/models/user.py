from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Custom User model for HireLoop platform
# Extends Django's AbstractUser to add UUID primary key and enhanced functionality
# Follows SRP: Handles user authentication and role detection


class User(AbstractUser):
    """
    Custom User model with UUID primary key and unique email constraint.
    
    Extends Django's AbstractUser to provide enhanced security with UUID
    and supports dual-role system (freelancer/client) through profile relationships.
    Follows SRP: Handles authentication, basic user data, and role detection.
    """
    
    # UUID primary key instead of auto-incrementing integer
    # Provides better security and scalability for distributed systems
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Enforce unique email addresses across all users
    # Allows email-based login and prevents duplicate accounts
    email = models.EmailField(unique=True)

    # Authentication configuration
    # USERNAME_FIELD: Field used for login (username in this case)
    # REQUIRED_FIELDS: Additional fields required when creating superuser
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """String representation returns username for admin interface"""
        return self.username

    @property
    def has_freelancer_profile(self):
        """
        Check if user has an associated freelancer profile.
        
        Uses hasattr to safely check for freelancerprofile relationship
        without triggering database queries or exceptions.
        
        Returns:
            bool: True if user has freelancer profile, False otherwise
        """
        return hasattr(self, 'freelancerprofile')

    @property
    def has_client_profile(self):
        """
        Check if user has an associated client profile.
        
        Uses hasattr to safely check for clientprofile relationship
        without triggering database queries or exceptions.
        
        Returns:
            bool: True if user has client profile, False otherwise
        """
        return hasattr(self, 'clientprofile')

    @property
    def user_roles(self):
        """
        Get all roles associated with this user.
        
        Delegates to role service for complex role determination logic.
        Follows SRP: User model doesn't contain role logic, just delegates.
        
        Returns:
            list: List of role strings (e.g., ['freelancer', 'client'])
        """
        from core.services.roles import get_user_roles
        return get_user_roles(self)

    @property
    def primary_role(self):
        """
        Get the primary/main role for this user.
        
        Useful for UI display and permission checks when user has multiple roles.
        Delegates to role service for consistent role priority logic.
        
        Returns:
            str: Primary role string (e.g., 'freelancer', 'client', or None)
        """
        from core.services.roles import get_primary_role
        return get_primary_role(self)
