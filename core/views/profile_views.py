from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages

from .base_views import BaseProfileCreateView
from ..forms.profile_forms import ClientProfileForm, FreelancerProfileForm
from ..services.profile_service import ProfileService
from ..services.action_dispatcher import ActionDispatcher
from ..services.profile_context_provider import ProfileContextProvider


class FreelancerProfileCreateView(BaseProfileCreateView):
    """Create Freelancer Profile - Single Responsibility Principle."""
    form_class = FreelancerProfileForm
    
    def get_profile_type(self):
        return 'freelancer'
    
    def create_profile(self, user, validated_data):
        service = ProfileService()
        return service.create_freelancer_profile(user, validated_data)
    
    def user_has_profile(self, user):
        return hasattr(user, 'freelancer_profile')


class ClientProfileCreateView(BaseProfileCreateView):
    """Create Client Profile - Single Responsibility Principle."""
    form_class = ClientProfileForm

    def get_profile_type(self):
        return 'client'
    
    def create_profile(self, user, validated_data):
        service = ProfileService()
        return service.create_client_profile(user, validated_data)

    def user_has_profile(self, user):
        return hasattr(user, 'client_profile')


class ProfileDetailView(LoginRequiredMixin, TemplateView):
    """
    Profile Detail View following SOLID Principles.
    
    - Single Responsibility: Only handles HTTP request/response
    - Open/Closed: Easy to extend with new actions via ActionDispatcher
    - Liskov Substitution: Uses interface-based handlers
    - Interface Segregation: Small, focused interfaces for each handler
    - Dependency Inversion: Depends on abstractions (services), not concrete classes
    """
    template_name = 'core/multi_profile_detail.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dependency Injection - depends on abstractions
        self.profile_service = ProfileService()
        self.context_provider = ProfileContextProvider(self.profile_service)
        self.action_dispatcher = ActionDispatcher(self.profile_service)
    
    def get_context_data(self, **kwargs):
        """Get context data using dedicated provider - Single Responsibility."""
        context = super().get_context_data(**kwargs)
        profile_context = self.context_provider.get_context_data(self.request.user)
        context.update(profile_context)
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests by dispatching to appropriate handlers.
        Follows Open/Closed Principle - easy to add new actions without modification.
        """
        action = request.POST.get('action', '')
        
        # Log for debugging
        print(f"DEBUG - Action: {action}")
        print(f"DEBUG - POST data: {dict(request.POST)}")
        
        # Use new Action Handler system
        for handler in self.action_dispatcher.handlers:
            if handler.can_handle(action):
                print(f"DEBUG - Found handler: {handler.__class__.__name__}")
                return handler.handle(request)
        
        # No handler found
        messages.error(request, f'Unknown action: {action}')
        return redirect('core:profile_detail')

    # Backward compatibility methods (can be removed later)
    def update_freelancer_profile(self, request):
        """Backward compatibility wrapper."""
        return self.action_dispatcher.dispatch(request, '', profile_type='freelancer')

    def update_client_profile(self, request):
        """Backward compatibility wrapper."""
        return self.action_dispatcher.dispatch(request, '', profile_type='client')