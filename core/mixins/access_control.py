from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class FreelancerRequiredMixin(LoginRequiredMixin):
    """
    Mixin to ensure the user is a freelancer.
    
    This mixin enforces that only authenticated users with a freelancer profile
    can access certain views. It's used to protect freelancer-specific functionality
    like creating services, applying to projects, or offering mentorships.
    
    Follows SRP: Single responsibility of validating freelancer access.
    Extends LoginRequiredMixin to ensure authentication first.
    
    Usage:
        class CreateServiceView(FreelancerRequiredMixin, CreateView):
            model = Service
            ...
    
    Raises:
        PermissionDenied: If user is not authenticated or not a freelancer
    """
    
    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to check freelancer status before processing request.
        
        Args:
            request: HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponse: Continues to parent dispatch if user is freelancer
            
        Raises:
            PermissionDenied: If user lacks freelancer privileges
        """
        # First check authentication (handled by LoginRequiredMixin)
        # Then verify user has freelancer profile
        if not request.user.is_authenticated or not hasattr(request.user, 'freelancerprofile'):
            raise PermissionDenied("You must be a freelancer to access this page.")
        return super().dispatch(request, *args, **kwargs)


class FreelancerOrOwnerRequiredMixin(LoginRequiredMixin):
    """
    Mixin to ensure the user is either a freelancer or the owner of the object.
    
    This mixin provides flexible access control for objects that can be accessed
    by either their owner or by freelancers (depending on the object type).
    It handles both freelancer-owned objects and user-owned objects.
    
    Follows SRP: Single responsibility of validating ownership/freelancer access.
    Applies KISS: Simple ownership checks based on object attributes.
    
    Object types handled:
        - Objects with 'freelancer' attribute: Checks if current user's freelancer 
          profile matches the object's freelancer
        - Objects with 'user' attribute: Checks if current user matches the object's user
    
    Usage:
        class ServiceDetailView(FreelancerOrOwnerRequiredMixin, DetailView):
            model = Service
            ...
    
    Raises:
        PermissionDenied: If user doesn't own the object or isn't the associated freelancer
    """
    
    def get_object(self, queryset=None):
        """
        Override get_object to enforce ownership/freelancer access control.
        
        This method retrieves the object and then validates that the current user
        has permission to access it based on ownership or freelancer relationship.
        
        Args:
            queryset: Optional queryset to use for object lookup
            
        Returns:
            Model instance: The requested object if user has permission
            
        Raises:
            PermissionDenied: If user lacks permission to access the object
        """
        # Get the object using parent class logic
        obj = super().get_object(queryset)
        
        # Check different ownership patterns
        if hasattr(obj, 'freelancer'):
            # Object belongs to a freelancer (e.g., Service, MentorshipSession)
            # Verify current user's freelancer profile matches
            if obj.freelancer != self.request.user.freelancerprofile:
                raise PermissionDenied("You do not have permission to access this object.")
                
        elif hasattr(obj, 'user'):
            # Object belongs directly to a user (e.g., Project, User profile)
            # Verify current user matches the object's owner
            if obj.user != self.request.user:
                raise PermissionDenied("You do not have permission to access this object.")
        
        # If object passes ownership checks, return it
        return obj

class FreelancerRequiredMixin(LoginRequiredMixin):
    """
    Ensures the user is authenticated and has a freelancer profile.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.has_freelancer_profile:
            raise PermissionDenied("You must be a freelancer to access this page.")
        return super().dispatch(request, *args, **kwargs)


class FreelancerOrOwnerRequiredMixin(LoginRequiredMixin):
    """
    Ensures the user is either a freelancer (object.freelancer) 
    or the owner (object.user).
    """

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if hasattr(obj, 'freelancer'):
            if obj.freelancer != self.request.user.freelancerprofile:
                raise PermissionDenied("You do not have permission to access this object.")

        elif hasattr(obj, 'user'):
            if obj.user != self.request.user:
                raise PermissionDenied("You do not have permission to access this object.")

        return obj