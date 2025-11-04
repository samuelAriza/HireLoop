from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class ProfileRequiredMixin(LoginRequiredMixin):
    """
    Mixin that checks if user has required profile type.
    """

    required_profile = None

    def dispatch(self, request, *args, **kwargs):
        if not self.user_has_required_profile(request.user):
            profile_name = _(self.required_profile.capitalize()) if self.required_profile else ""
            messages.warning(
                request,
                _("You need a %(profile)s profile to access this page.") % {"profile": profile_name},
            )
            return redirect("core:profile_detail")
        return super().dispatch(request, *args, **kwargs)

    def user_has_required_profile(self, user):
        if self.required_profile == "freelancer":
            return hasattr(user, "freelancer_profile")
        elif self.required_profile == "client":
            return hasattr(user, "client_profile")
        return True