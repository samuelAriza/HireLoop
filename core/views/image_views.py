from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from ..forms.profile_forms import ProfileImageForm
from ..services.profile_service import ProfileService

class ProfileImageUpdateView(LoginRequiredMixin, View):
    """View for updating profile image following DIP."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_service = ProfileService()

    def post(self, request, *args, **kwargs):
        """Handle profile image update."""
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


class ProfileImageDeleteView(LoginRequiredMixin, View):
    """View for deleting profile image."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_service = ProfileService()

    def post(self, request, *args, **kwargs):
        """Handle profile image deletion."""
        success = self.profile_service.delete_user_profile_image(request.user)

        if success:
            messages.success(request, "Profile image deleted successfully!")
        else:
            messages.error(request, "Failed to delete profile image.")

        return redirect("core:profile_detail")
