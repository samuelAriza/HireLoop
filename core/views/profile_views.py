from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages

from .base_views import BaseProfileCreateView
from ..forms.profile_forms import ClientProfileForm, FreelancerProfileForm, ProfileImageForm
from ..services import ProfileService


class FreelancerProfileCreateView(BaseProfileCreateView):
    form_class = FreelancerProfileForm
    
    def get_profile_type(self):
        return 'freelancer'
    
    def create_profile(self, user, validated_data):
        service = ProfileService()
        return service.create_freelancer_profile(user, validated_data)
    
    def user_has_profile(self, user):
        return hasattr(user, 'freelancer_profile')


class ClientProfileCreateView(BaseProfileCreateView):
    form_class = ClientProfileForm
    
    def get_profile_type(self):
        return 'client'
    
    def create_profile(self, user, validated_data):
        service = ProfileService()
        return service.create_client_profile(user, validated_data)
    
    def user_has_profile(self, user):
        return hasattr(user, 'client_profile')


class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'core/multi_profile_detail.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_service = ProfileService()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get profile information using service layer
        profile_data = self.profile_service.get_user_profiles(user)
        
        context.update({
            'user_profile': user,
            'profiles': profile_data,
            'has_freelancer': profile_data['has_freelancer'],
            'has_client': profile_data['has_client'],
            'user_roles': user.get_roles(),
            'primary_role': self.profile_service.get_primary_role(user),
            'profile_image_url': self.profile_service.get_user_profile_image_url(user),
            # Forms for editing
            'freelancer_form': FreelancerProfileForm(
                instance=profile_data['freelancer']
            ) if profile_data['has_freelancer'] else None,
            'client_form': ClientProfileForm(
                instance=profile_data['client']
            ) if profile_data['has_client'] else None,
            'image_form': ProfileImageForm(instance=user),
        })
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle profile updates and deletions."""
        action = request.POST.get('action')
        profile_type = request.POST.get('profile_type')
        
        print(f"DEBUG - Action: {action}, Profile Type: {profile_type}")
        
        # Handle image actions
        if action == 'update_image':
            return self._handle_image_update(request)
        elif action == 'delete_image':
            return self._handle_image_delete(request)
        
        # Handle profile deletion
        elif action == 'delete':
            return self._handle_profile_deletion(request, profile_type)
        
        # Handle profile update (when no action specified, it's an update)
        elif profile_type in ['freelancer', 'client']:
            return self._handle_profile_update(request, profile_type)
        
        messages.error(request, 'Invalid action or profile type.')
        return redirect('core:profile_detail')

    def update_freelancer_profile(self, request):
        """Update freelancer profile - wrapper for backward compatibility."""
        return self._handle_profile_update(request, 'freelancer')

    def update_client_profile(self, request):
        """Update client profile - wrapper for backward compatibility."""
        return self._handle_profile_update(request, 'client')
        
    def _handle_profile_deletion(self, request, profile_type):
        """Handle profile deletion logic."""
        print(f"DEBUG: Attempting to delete profile type: {profile_type}")
        
        if profile_type == 'freelancer':
            success = self.profile_service.delete_freelancer_profile(request.user)
            profile_name = 'Freelancer'
        elif profile_type == 'client':
            success = self.profile_service.delete_client_profile(request.user)
            profile_name = 'Client'
        else:
            messages.error(request, 'Invalid profile type for deletion.')
            return redirect('core:profile_detail')
        
        if success:
            messages.success(request, f'{profile_name} profile deleted successfully!')
        else:
            messages.error(request, f'{profile_name} profile not found or could not be deleted.')
        
        return redirect('core:profile_detail')
    
    def _handle_profile_update(self, request, profile_type):
        """Handle profile update logic."""
        form_classes = {
            'freelancer': FreelancerProfileForm,
            'client': ClientProfileForm
        }
        
        service_methods = {
            'freelancer': self.profile_service.update_freelancer_profile,
            'client': self.profile_service.update_client_profile
        }
        
        profiles = self.profile_service.get_user_profiles(request.user)
        profile_instance = profiles.get(profile_type)
        
        if not profile_instance:
            messages.error(request, f'{profile_type.title()} profile not found.')
            return redirect('core:profile_detail')
        
        form = form_classes[profile_type](
            request.POST, 
            instance=profile_instance
        )
        
        if form.is_valid():
            try:
                updated_profile = service_methods[profile_type](
                    request.user, 
                    form.cleaned_data
                )
                if updated_profile:
                    messages.success(request, f'{profile_type.title()} profile updated successfully!')
                else:
                    messages.error(request, f'Failed to update {profile_type} profile.')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors in the form.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        
        return redirect('core:profile_detail')
    
    def _handle_image_update(self, request):
        """Handle profile image update."""
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            image_file = form.cleaned_data.get('profile_image')
            success = self.profile_service.update_user_profile_image(request.user, image_file)
            
            if success:
                messages.success(request, 'Profile image updated successfully!')
            else:
                messages.error(request, 'Failed to update profile image.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        
        return redirect('core:profile_detail')

    def _handle_image_delete(self, request):
        """Handle profile image deletion."""
        success = self.profile_service.delete_user_profile_image(request.user)
        
        if success:
            messages.success(request, 'Profile image deleted successfully!')
        else:
            messages.error(request, 'Failed to delete profile image.')
        
        return redirect('core:profile_detail')