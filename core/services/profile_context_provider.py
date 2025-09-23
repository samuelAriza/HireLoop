from typing import Dict, Any
from django.contrib.auth.models import AbstractUser
from .profile_service import ProfileService
from ..forms.profile_forms import (
    ClientProfileForm,
    FreelancerProfileForm,
    ProfileImageForm,
)

class ProfileContextProvider:
    def __init__(self, profile_service: ProfileService):
        self.profile_service = profile_service

    def get_public_context_data(self, user):
        """
        Get public context data for profile sharing.
        Only includes non-sensitive information, structured to match the private view context.
        """
        # Obtener datos del perfil usando el servicio
        profile_data = self.profile_service.get_user_profiles(user)

        # Preparar datos del portafolio
        user_portfolios = []
        if profile_data["has_freelancer"]:
            user_portfolios = self._get_public_portfolio_items(user, "freelancer")

        context = {
            "user_profile": user,
            "profile_image_url": self.profile_service.get_user_profile_image_url(user),
            "user_roles": user.get_roles(),  # Añadir user_roles para compatibilidad con el template
            "has_freelancer": hasattr(user, "freelancer_profile"),
            "has_client": hasattr(user, "client_profile"),
            "profiles": {
                "freelancer": (
                    user.freelancer_profile
                    if hasattr(user, "freelancer_profile")
                    else None
                ),
                "freelancer_skills": profile_data["freelancer_skills"],
                "client": (
                    user.client_profile if hasattr(user, "client_profile") else None
                ),
            },
            "user_portfolios": user_portfolios,
        }

        return context

    def _get_public_portfolio_items(self, user, profile_type):
        """Get public portfolio items."""
        try:
            from ..repositories.portfolio_repository import PortfolioRepository

            portfolio_repo = PortfolioRepository()

            if profile_type == "freelancer" and hasattr(user, "freelancer_profile"):
                items = portfolio_repo.list_by_freelancer(user.freelancer_profile)
                return [item for item in items if getattr(item, "is_public", True)]

            return []
        except Exception as e:
            print(f"Error getting public portfolio items: {e}")
            return []

    def _get_public_microservices(self, user):
        """Get public microservices."""
        try:
            return user.freelancer_profile.microservices.filter(is_active=True)[:6]
        except Exception:
            return []

    def _get_public_projects(self, user):
        """Get public projects."""
        try:
            return user.client_profile.projects.filter(is_public=True)[:6]
        except Exception:
            return []

    def get_context_data(self, user: AbstractUser) -> Dict[str, Any]:
        """Get all context data needed for profile view."""
        profile_data = self.profile_service.get_user_profiles(user)
        user_portfolios = []

        if profile_data["has_freelancer"]:
            user_portfolios = self._get_user_portfolios(profile_data["freelancer"])

        return {
            "user_profile": user,
            "profiles": profile_data,
            "has_freelancer": profile_data["has_freelancer"],
            "has_client": profile_data["has_client"],
            "user_roles": user.get_roles(),
            "primary_role": self.profile_service.get_primary_role(user),
            "profile_image_url": self.profile_service.get_user_profile_image_url(user),
            "user_portfolios": user_portfolios,
            "freelancer_form": self._get_freelancer_form(profile_data),
            "client_form": self._get_client_form(profile_data),
            "image_form": ProfileImageForm(instance=user),
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
        return (
            FreelancerProfileForm(instance=profile_data["freelancer"])
            if profile_data["has_freelancer"]
            else None
        )

    def _get_client_form(self, profile_data):
        """Get client form instance."""
        return (
            ClientProfileForm(instance=profile_data["client"])
            if profile_data["has_client"]
            else None
        )