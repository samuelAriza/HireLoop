from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import DetailView
from .base_views import BaseProfileCreateView
from ..forms.profile_forms import ClientProfileForm, FreelancerProfileForm
from ..services.profile_service import ProfileService
from ..services.action_dispatcher import ActionDispatcher
from ..services.profile_context_provider import ProfileContextProvider
from ..models import User

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
        context = super().get_context_data(**kwargs)
        profile_context = self.context_provider.get_context_data(self.request.user)
        context.update(profile_context)
        context["primary_role"] = self.profile_service.get_primary_role(self.request.user)
        context["is_owner"] = True
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

class PublicProfileDetailView(DetailView):
    """Public Profile Detail View for sharing profiles by username."""
    model = User
    template_name = 'core/multi_profile_detail.html'
    context_object_name = 'profile_user'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = ProfileService()
        provider = ProfileContextProvider(service)
        public_context = provider.get_public_context_data(self.object)
        context.update(public_context)
        context["is_owner"] = self.request.user == self.object
        return context