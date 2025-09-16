"""
Profile management services for HireLoop platform.

Contains all services related to user profile management including
creation, updates, validation, and role-specific operations.
"""

from typing import Dict, Any, Optional, List
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .base import BaseService

User = get_user_model()


class ProfileService(BaseService):
    """
    Base profile service providing common profile operations.
    
    Follows SRP: Handles only profile-related business logic.
    Provides factory methods for different profile types.
    """
    
    def __init__(self):
        """Initialize profile service with message tracking."""
        super().__init__()
        self._errors = []
        self._warnings = []
    
    def clear_messages(self):
        """Clear all error and warning messages."""
        self._errors = []
        self._warnings = []
    
    def add_error(self, message: str):
        """Add an error message."""
        self._errors.append(message)
    
    def add_warning(self, message: str):
        """Add a warning message."""
        self._warnings.append(message)
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self._errors) > 0
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> bool:
        """Validate that all required fields are present."""
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            for field in missing_fields:
                self.add_error(f"Field '{field}' is required")
            return False
        return True
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate common profile data."""
        return True  # Base implementation
    
    @staticmethod
    def get_profile_service(profile_type: str):
        """
        Factory method to get appropriate profile service.
        
        Args:
            profile_type: 'freelancer', 'client', or 'user'
            
        Returns:
            Appropriate profile service instance
        """
        if profile_type == 'freelancer':
            return FreelancerProfileService()
        elif profile_type == 'client':
            return ClientProfileService()
        elif profile_type == 'user':
            return UserProfileService()
        else:
            raise ValueError(f"Unknown profile type: {profile_type}")


class UserProfileService(ProfileService):
    """
    Service for managing base user profile operations.
    
    Handles user-level profile management including
    authentication data, basic info updates, etc.
    """
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate user profile data."""
        self.clear_messages()
        
        # Validate required fields
        required_fields = ['username', 'email']
        if not self.validate_required_fields(data, required_fields):
            return False
            
        # Validate email format
        email = data.get('email', '')
        if email and '@' not in email:
            self.add_error("Invalid email format")
            return False
            
        return not self.has_errors()
    
    def update_user_profile(self, user, data: Dict[str, Any]) -> bool:
        """
        Update base user profile information.
        
        Args:
            user: User instance to update
            data: Updated profile data
            
        Returns:
            bool: True if update successful
        """
        if not self.validate(data):
            return False
            
        try:
            # Update user fields
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
                
            user.save()
            return True
            
        except Exception as e:
            self.add_error(f"Failed to update user profile: {str(e)}")
            return False


class FreelancerProfileService(ProfileService):
    """
    Service for managing freelancer profiles.
    
    Handles freelancer-specific operations including
    skills management, bio updates, and freelancer verification.
    """
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate freelancer profile data."""
        self.clear_messages()
        
        # Validate skills if provided
        skills = data.get('skills', [])
        if skills:
            if isinstance(skills, str):
                # Convert comma-separated string to list
                skills = [s.strip() for s in skills.split(',') if s.strip()]
                data['skills'] = skills
                
            if len(skills) > 20:
                self.add_error("Maximum 20 skills allowed")
                return False
                
        # Validate bio length
        bio = data.get('bio', '')
        if bio and len(bio) > 1000:
            self.add_error("Bio cannot exceed 1000 characters")
            return False
            
        return not self.has_errors()
    
    def create_freelancer_profile(self, user, data: Dict[str, Any]):
        """
        Create a new freelancer profile.
        
        Args:
            user: User instance
            data: Profile data including skills and bio
            
        Returns:
            FreelancerProfile instance or None if failed
        """
        try:
            from core.models import FreelancerProfile
        except ImportError:
            from core.models.profiles import FreelancerProfile
        
        # Check if user already has freelancer profile
        if hasattr(user, 'freelancerprofile'):
            self.add_error("User already has a freelancer profile")
            return None
            
        if not self.validate(data):
            return None
            
        try:
            profile = FreelancerProfile.objects.create(
                user=user,
                skills=data.get('skills', []),
                bio=data.get('bio', '')
            )
            return profile
            
        except Exception as e:
            self.add_error(f"Failed to create freelancer profile: {str(e)}")
            return None
    
    def update_freelancer_profile(self, user, data: Dict[str, Any]) -> bool:
        """
        Update existing freelancer profile.
        
        Args:
            user: User instance
            data: Updated profile data
            
        Returns:
            bool: True if update successful
        """
        if not hasattr(user, 'freelancerprofile'):
            self.add_error("User doesn't have a freelancer profile")
            return False
            
        if not self.validate(data):
            return False
            
        try:
            profile = user.freelancerprofile
            
            if 'skills' in data:
                profile.skills = data['skills']
            if 'bio' in data:
                profile.bio = data['bio']
                
            profile.save()
            return True
            
        except Exception as e:
            self.add_error(f"Failed to update freelancer profile: {str(e)}")
            return False


class ClientProfileService(ProfileService):
    """
    Service for managing client profiles.
    
    Handles client-specific operations including
    company information, billing details, and client verification.
    """
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate client profile data."""
        self.clear_messages()
        
        # Validate company name length
        company = data.get('company', '')
        if company and len(company) > 255:
            self.add_error("Company name cannot exceed 255 characters")
            return False
            
        # Validate billing email format
        billing_email = data.get('billing_email', '')
        if billing_email and '@' not in billing_email:
            self.add_error("Invalid billing email format")
            return False
            
        return not self.has_errors()
    
    def create_client_profile(self, user, data: Dict[str, Any]):
        """
        Create a new client profile.
        
        Args:
            user: User instance
            data: Profile data including company and billing info
            
        Returns:
            ClientProfile instance or None if failed
        """
        try:
            from core.models import ClientProfile
        except ImportError:
            from core.models.profiles import ClientProfile
        
        # Check if user already has client profile
        if hasattr(user, 'clientprofile'):
            self.add_error("User already has a client profile")
            return None
            
        if not self.validate(data):
            return None
            
        try:
            profile = ClientProfile.objects.create(
                user=user,
                company=data.get('company', ''),
                billing_email=data.get('billing_email', '')
            )
            return profile
            
        except Exception as e:
            self.add_error(f"Failed to create client profile: {str(e)}")
            return None
    
    def update_client_profile(self, user, data: Dict[str, Any]) -> bool:
        """
        Update existing client profile.
        
        Args:
            user: User instance
            data: Updated profile data
            
        Returns:
            bool: True if update successful
        """
        if not hasattr(user, 'clientprofile'):
            self.add_error("User doesn't have a client profile")
            return False
            
        if not self.validate(data):
            return False
            
        try:
            profile = user.clientprofile
            
            if 'company' in data:
                profile.company = data['company']
            if 'billing_email' in data:
                profile.billing_email = data['billing_email']
                
            profile.save()
            return True
            
        except Exception as e:
            self.add_error(f"Failed to update client profile: {str(e)}")
            return False