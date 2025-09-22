from typing import Optional, Tuple, List
from django.db import IntegrityError

from ..repositories.base_repository import BaseRepository
from ..models import FreelancerProfile, ClientProfile, User
from projects.models import ProjectApplication


class ProfileRepository(BaseRepository):
    """
    Repository for profile operations.
    Encapsulates data access logic.
    """
    
    def create(self, **kwargs):
        """Not used - implement specific methods instead."""
        pass
    
    def get_by_id(self, entity_id):
        """Not used - implement specific methods instead."""
        pass
    
    def update(self, entity, **kwargs):
        """Not used - implement specific methods instead."""
        pass
    
    def delete(self, entity):
        """Not used - implement specific methods instead."""
        pass
    
    def create_freelancer_profile(self, user: User, **kwargs) -> Tuple[FreelancerProfile, bool]:
        """Create freelancer profile."""
        if hasattr(user, 'freelancer_profile'):
            return user.freelancer_profile, False
            
        try:
            profile = FreelancerProfile.objects.create(user=user, **kwargs)
            return profile, True
        except IntegrityError:
            return user.freelancer_profile, False
    
    def create_client_profile(self, user: User, **kwargs) -> Tuple[ClientProfile, bool]:
        """Create client profile."""
        if hasattr(user, 'client_profile'):
            return user.client_profile, False
            
        try:
            profile = ClientProfile.objects.create(user=user, **kwargs)
            return profile, True
        except IntegrityError:
            return user.client_profile, False
    
    def get_freelancer_profile(self, user: User) -> Optional[FreelancerProfile]:
        """Get freelancer profile for user."""
        try:
            return user.freelancer_profile
        except FreelancerProfile.DoesNotExist:
            return None
    
    def get_client_profile(self, user: User) -> Optional[ClientProfile]:
        """Get client profile for user."""
        try:
            return user.client_profile
        except ClientProfile.DoesNotExist:
            return None
    
    def update_freelancer_profile(self, profile: FreelancerProfile, **kwargs) -> FreelancerProfile:
        """Update freelancer profile."""
        print("locomotra"*100)
        for field, value in kwargs.items():
            setattr(profile, field, value)
        profile.save()
        return profile
    
    def update_client_profile(self, profile: ClientProfile, **kwargs) -> ClientProfile:
        """Update client profile."""
        for field, value in kwargs.items():
            setattr(profile, field, value)
        profile.save()
        return profile
    
    def get_freelancer_applications(self, freelancer: FreelancerProfile) -> List[ProjectApplication]:
        """Get all applications for a freelancer."""
        return freelancer.applications.all().order_by("-created_at")