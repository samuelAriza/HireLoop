from typing import Dict, Any
from django.contrib.auth.models import AbstractUser

from .profile_service import ProfileService
from ..forms.profile_forms import ClientProfileForm, FreelancerProfileForm, ProfileImageForm

class ProfileContextProvider:
    """
    Provides context data for profile views - Single Responsibility Principle.
    Depends on abstractions, not concrete classes - Dependency Inversion Principle.
    """
    
    def __init__(self, profile_service: ProfileService):
        self.profile_service = profile_service
    
    def get_context_data(self, user: AbstractUser) -> Dict[str, Any]:
        """Get all context data needed for profile view."""
        # Get profile information using service layer
        profile_data = self.profile_service.get_user_profiles(user)
        user_portfolios = []
        
        # Get portfolios if user is a freelancer
        if profile_data['has_freelancer']:
            user_portfolios = self._get_user_portfolios(profile_data['freelancer'])
        
        return {
            'user_profile': user,
            'profiles': profile_data,
            'has_freelancer': profile_data['has_freelancer'],
            'has_client': profile_data['has_client'],
            'user_roles': user.get_roles(),
            'primary_role': self.profile_service.get_primary_role(user),
            'profile_image_url': self.profile_service.get_user_profile_image_url(user),
            'user_portfolios': user_portfolios,
            # Forms for editing
            'freelancer_form': self._get_freelancer_form(profile_data),
            'client_form': self._get_client_form(profile_data),
            'image_form': ProfileImageForm(instance=user),
        }
    
    def _get_user_portfolios(self, freelancer_profile):
        """Get portfolios for freelancer - private method to maintain encapsulation."""
        try:
            from .portfolio_service import PortfolioService
            portfolio_service = PortfolioService()
            return portfolio_service.list_items(freelancer_profile)
        except Exception as e:
            print(f"Error getting portfolios: {e}")
            return []
    
    def _get_freelancer_form(self, profile_data):
        """Get freelancer form instance."""
        return FreelancerProfileForm(
            instance=profile_data['freelancer']
        ) if profile_data['has_freelancer'] else None
    
    def _get_client_form(self, profile_data):
        """Get client form instance."""
        return ClientProfileForm(
            instance=profile_data['client']
        ) if profile_data['has_client'] else None