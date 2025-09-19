# ARCHIVO: /home/samargo/Documents/universidad_/software_architecture/hireloop_project/core/services/profile_service.py
from typing import Dict, Any, Optional
from django.core.files.uploadedfile import UploadedFile

from ..services.image_service import ProfileImageService
from ..repositories.profile_repository import ProfileRepository
from ..models import User


class ProfileService:
    """
    Service class following Single Responsibility and Dependency Inversion.
    """
    
    def __init__(self, repository: ProfileRepository = None):
        self._repository = repository or ProfileRepository()
        self._image_service = ProfileImageService()
    
    def get_user_profiles(self, user: User) -> Dict[str, Any]:
        """Get all profiles for a user."""
        freelancer_profile = self._repository.get_freelancer_profile(user)
        client_profile = self._repository.get_client_profile(user)
        
        freelancer_skills = []
        if freelancer_profile and freelancer_profile.skills:
            freelancer_skills = [
                {'name': skill.strip()} 
                for skill in freelancer_profile.skills.split(',') 
                if skill.strip()
            ]
            
        return {
            'freelancer': freelancer_profile,
            'freelancer_skills': freelancer_skills,
            'client': client_profile,
            'has_freelancer': freelancer_profile is not None,
            'has_client': client_profile is not None,
        }
    
    def create_freelancer_profile(self, user: User, validated_data: Dict[str, Any]):
        """Create freelancer profile."""
        return self._repository.create_freelancer_profile(user, **validated_data)
    
    def create_client_profile(self, user: User, validated_data: Dict[str, Any]):
        """Create client profile."""
        return self._repository.create_client_profile(user, **validated_data)
    
    def update_freelancer_profile(self, user: User, validated_data: Dict[str, Any]) -> Optional[Any]:
        """Update freelancer profile."""
        profile = self._repository.get_freelancer_profile(user)
        if not profile:
            return None
        return self._repository.update_freelancer_profile(profile, **validated_data)
    
    def update_client_profile(self, user: User, validated_data: Dict[str, Any]) -> Optional[Any]:
        """Update client profile."""
        profile = self._repository.get_client_profile(user)
        if not profile:
            return None
        return self._repository.update_client_profile(profile, **validated_data)
    
    def delete_freelancer_profile(self, user: User) -> bool:
        """Delete freelancer profile for a user."""
        try:
            if hasattr(user, 'freelancer_profile'):
                user.freelancer_profile.delete()
                return True
            return False
        except Exception as e:
            print(f"Error deleting freelancer profile: {e}")
            return False

    def delete_client_profile(self, user: User) -> bool:
        """Delete client profile for a user."""
        try:
            if hasattr(user, 'client_profile'):
                user.client_profile.delete()
                return True
            return False
        except Exception as e:
            print(f"Error deleting client profile: {e}")
            return False

    def delete_all_profiles(self, user: User) -> Dict[str, bool]:
        """Delete all profiles for a user."""
        result = {
            'freelancer_deleted': self.delete_freelancer_profile(user),
            'client_deleted': self.delete_client_profile(user)
        }
        return result
    
    def update_user_profile_image(self, user: User, image_file: UploadedFile) -> bool:
        """Update user profile image using DIP."""
        try:
            # Delete old image if exists
            if user.profile_image:
                self._image_service.delete_profile_image(user.profile_image.name)
            
            # Upload new image
            if image_file:
                saved_path = self._image_service.upload_profile_image(user.id, image_file)
                user.profile_image = saved_path
            else:
                user.profile_image = None
            
            user.save()
            return True
            
        except Exception as e:
            print(f"Error updating profile image: {e}")
            return False

    def delete_user_profile_image(self, user: User) -> bool:
        """Delete user profile image."""
        try:
            if user.profile_image:
                success = self._image_service.delete_profile_image(user.profile_image.name)
                
                if success:
                    user.profile_image = None
                    user.save()
                    return True
            return False
            
        except Exception as e:
            print(f"Error deleting profile image: {e}")
            return False

    def get_user_profile_image_url(self, user: User) -> str:
        """Get user profile image URL."""
        return self._image_service.get_image_url(
            user.profile_image.name if user.profile_image else None
        )
    
    def get_primary_role(self, user: User) -> Optional[str]:
        """Get primary role for user."""
        profiles = self.get_user_profiles(user)
        if profiles['has_freelancer']:
            return 'freelancer'
        elif profiles['has_client']:
            return 'client'
        return None