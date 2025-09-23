from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


class BaseProfileCreateView(LoginRequiredMixin, CreateView):
    """
    Base class for profile creation views.
    Follows Open/Closed Principle - open for extension, closed for modification.
    """

    template_name = "core/create_profile.html"
    success_url = reverse_lazy("core:profile_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_type"] = self.get_profile_type()
        return context

    def form_valid(self, form):
        profile, created = self.create_profile(self.request.user, form.cleaned_data)

        if created:
            messages.success(
                self.request,
                f"{self.get_profile_type().title()} profile created successfully!",
            )
        else:
            messages.info(
                self.request, f"You already have a {self.get_profile_type()} profile."
            )

        return redirect(self.success_url)

    def get_profile_type(self):
        """Override in subclasses to specify profile type."""
        raise NotImplementedError

    def create_profile(self, user, validated_data):
        """Override in subclasses to create specific profile type."""
        raise NotImplementedError

    def dispatch(self, request, *args, **kwargs):
        """Check if user already has this profile type."""
        if self.user_has_profile(request.user):
            messages.info(
                request, f"You already have a {self.get_profile_type()} profile."
            )
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def user_has_profile(self, user):
        """Override in subclasses to check profile existence."""
        return False
