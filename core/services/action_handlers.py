from abc import ABC, abstractmethod
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

class ActionHandler(ABC):
    """Abstract base class for handling actions - Interface Segregation Principle."""

    @abstractmethod
    def handle(self, request: HttpRequest, **kwargs) -> HttpResponse:
        """Handle the specific action."""
        pass

    @abstractmethod
    def can_handle(self, action: str) -> bool:
        """Check if this handler can process the given action."""
        pass

class ProfileImageUpdateHandler(ActionHandler):
    """Handle profile image updates - Single Responsibility Principle."""

    def __init__(self, profile_service):
        self.profile_service = profile_service

    def can_handle(self, action: str) -> bool:
        return action == "update_image"

    def handle(self, request: HttpRequest, **kwargs) -> HttpResponse:
        from ..forms.profile_forms import ProfileImageForm

        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            image_file = form.cleaned_data.get("profile_image")
            success = self.profile_service.update_user_profile_image(
                request.user, image_file
            )

            if success:
                messages.success(request, "Profile image updated successfully!")
            else:
                messages.error(request, "Failed to update profile image.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return redirect("core:profile_detail")

class ProfileImageDeleteHandler(ActionHandler):
    """Handle profile image deletion - Single Responsibility Principle."""

    def __init__(self, profile_service):
        self.profile_service = profile_service

    def can_handle(self, action: str) -> bool:
        return action == "delete_image"

    def handle(self, request: HttpRequest, **kwargs) -> HttpResponse:
        success = self.profile_service.delete_user_profile_image(request.user)

        if success:
            messages.success(request, "Profile image deleted successfully!")
        else:
            messages.error(request, "Failed to delete profile image.")

        return redirect("core:profile_detail")

class ProfileDeleteHandler(ActionHandler):
    """Handle profile deletion - Single Responsibility Principle."""

    def __init__(self, profile_service):
        self.profile_service = profile_service

    def can_handle(self, action: str) -> bool:
        return action == "delete"

    def handle(self, request: HttpRequest, **kwargs) -> HttpResponse:
        profile_type = request.POST.get("profile_type")

        if profile_type == "freelancer":
            success = self.profile_service.delete_freelancer_profile(request.user)
            profile_name = "Freelancer"
        elif profile_type == "client":
            success = self.profile_service.delete_client_profile(request.user)
            profile_name = "Client"
        else:
            messages.error(request, "Invalid profile type for deletion.")
            return redirect("core:profile_detail")

        if success:
            messages.success(request, f"{profile_name} profile deleted successfully!")
        else:
            messages.error(
                request, f"{profile_name} profile not found or could not be deleted."
            )

        return redirect("core:profile_detail")

class ProfileUpdateHandler(ActionHandler):
    """Handle profile updates - Single Responsibility Principle."""

    def __init__(self, profile_service):
        self.profile_service = profile_service

    def can_handle(self, action: str) -> bool:
        return action in [None, ""]  # Default action for profile updates

    def handle(self, request: HttpRequest, **kwargs) -> HttpResponse:
        from ..forms.profile_forms import FreelancerProfileForm, ClientProfileForm

        profile_type = request.POST.get("profile_type")

        if profile_type not in ["freelancer", "client"]:
            messages.error(request, "Invalid profile type.")
            return redirect("core:profile_detail")

        form_classes = {
            "freelancer": FreelancerProfileForm,
            "client": ClientProfileForm,
        }

        service_methods = {
            "freelancer": self.profile_service.update_freelancer_profile,
            "client": self.profile_service.update_client_profile,
        }

        profiles = self.profile_service.get_user_profiles(request.user)
        profile_instance = profiles.get(profile_type)

        if not profile_instance:
            messages.error(request, f"{profile_type.title()} profile not found.")
            return redirect("core:profile_detail")

        form = form_classes[profile_type](request.POST, instance=profile_instance)

        if form.is_valid():
            try:
                updated_profile = service_methods[profile_type](
                    request.user, form.cleaned_data
                )
                if updated_profile:
                    messages.success(
                        request, f"{profile_type.title()} profile updated successfully!"
                    )
                else:
                    messages.error(request, f"Failed to update {profile_type} profile.")
            except Exception as e:
                messages.error(request, f"Error updating profile: {str(e)}")
        else:
            messages.error(request, "Please correct the errors in the form.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return redirect("core:profile_detail")


class PortfolioUpdateHandler(ActionHandler):
    """Handle portfolio updates - Single Responsibility Principle."""

    def can_handle(self, action: str) -> bool:
        return action == "update_portfolio"

    def handle(self, request: HttpRequest, **kwargs) -> HttpResponse:
        from ..services.portfolio_service import PortfolioService

        portfolio_id = request.POST.get("portfolio_id")

        if not portfolio_id:
            messages.error(request, "Portfolio ID not provided.")
            return redirect("core:profile_detail")

        try:
            portfolio_service = PortfolioService()
            portfolio_item = portfolio_service.get_item(portfolio_id)

            if not portfolio_item:
                messages.error(request, "Portfolio item not found.")
                return redirect("core:profile_detail")

            # Check ownership
            print(
                f"DEBUG PortfolioUpdateHandler - Portfolio user: {portfolio_item.freelancer.user}"
            )
            print(f"DEBUG PortfolioUpdateHandler - Request user: {request.user}")
            if portfolio_item.freelancer.user != request.user:
                messages.error(
                    request, "You do not have permission to edit this portfolio item."
                )
                return redirect("core:profile_detail")

            # Prepare update data
            update_data = {
                "title": request.POST.get("title"),
                "description": request.POST.get("description"),
                "technologies": request.POST.get("technologies"),
                "url_demo": request.POST.get("url_demo"),
                "url_repository": request.POST.get("url_repository"),
            }

            if "image" in request.FILES:
                update_data["image"] = request.FILES["image"]

            success = portfolio_service.update_portfolio(portfolio_item, update_data)

            if success:
                messages.success(request, "Portfolio item updated successfully!")
            else:
                messages.error(request, "Failed to update portfolio item.")

        except Exception as e:
            messages.error(request, f"Error updating portfolio item: {str(e)}")

        return redirect("core:profile_detail")


class PortfolioDeleteHandler(ActionHandler):
    """Handle portfolio deletion - Single Responsibility Principle."""

    def can_handle(self, action: str) -> bool:
        return action == "delete_portfolio"

    def handle(self, request: HttpRequest, **kwargs) -> HttpResponse:
        from ..services.portfolio_service import PortfolioService

        portfolio_id = request.POST.get("portfolio_id")

        if not portfolio_id:
            messages.error(request, "Portfolio ID not provided.")
            return redirect("core:profile_detail")

        try:
            portfolio_service = PortfolioService()
            portfolio_item = portfolio_service.get_item(portfolio_id)

            if not portfolio_item:
                messages.error(request, "Portfolio item not found.")
                return redirect("core:profile_detail")

            # Check ownership
            print(
                f"DEBUG PortfolioDeleteHandler - Portfolio user: {portfolio_item.freelancer.user}"
            )
            print(f"DEBUG PortfolioDeleteHandler - Request user: {request.user}")
            if portfolio_item.freelancer.user != request.user:
                messages.error(
                    request, "You do not have permission to delete this portfolio item."
                )
                return redirect("core:profile_detail")

            # Store title for message
            portfolio_title = portfolio_item.title

            success = portfolio_service.delete_portfolio(portfolio_item)

            if success:
                messages.success(
                    request, f'Portfolio "{portfolio_title}" deleted successfully!'
                )
            else:
                messages.error(request, "Failed to delete portfolio item.")

        except Exception as e:
            messages.error(request, f"Error deleting portfolio item: {str(e)}")

        return redirect("core:profile_detail")
