from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class ProfileRequiredMixin(LoginRequiredMixin):
    """
    Mixin that checks if user has required profile type.
    """
    required_profile = None  # Override in subclass
    
    def dispatch(self, request, *args, **kwargs):
        if not self.user_has_required_profile(request.user):
            messages.warning(
                request, 
                f'You need a {self.required_profile} profile to access this page.'
            )
            return redirect('core:profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def user_has_required_profile(self, user):
        if self.required_profile == 'freelancer':
            return hasattr(user, 'freelancer_profile')
        elif self.required_profile == 'client':
            return hasattr(user, 'client_profile')
        return True