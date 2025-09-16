"""
Mentorship Service for managing mentorship operations.
"""

from typing import List, Dict, Any, Optional, Union
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from .base import BaseService

User = get_user_model()

from typing import Dict, Any, Optional, List
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, PermissionDenied
from .base import BaseService

User = get_user_model()


class MentorshipService(BaseService):
    """
    Service for managing mentorship sessions.
    
    Handles mentorship creation, booking, and management
    following business rules and validation.
    """
    
    def __init__(self):
        """Initialize mentorship service."""
        super().__init__()
        self._errors = []
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate mentorship data."""
        self._errors = []
        
        # Validate required fields for creating a mentorship offer
        required_fields = ['title', 'description', 'category', 'price', 'duration_hours']
        for field in required_fields:
            if field not in data or not data[field]:
                self._errors.append(f"Field '{field}' is required")
        
        # Validate price
        price = data.get('price')
        if price and (not isinstance(price, (int, float)) or price <= 0):
            self._errors.append("Price must be a positive number")
        
        # Validate duration
        duration = data.get('duration_hours')
        if duration and (not isinstance(duration, int) or duration > 1 or duration > 8):
            self._errors.append("Duration must be between 1 and 8 hours")
        
        return len(self._errors) == 0
    
    def validate_session_booking(self, data: Dict[str, Any]) -> bool:
        """Validate mentorship session booking data (different from creation)."""
        self._errors = []
        
        # This is for booking a session, not creating a mentorship offer
        required_fields = ['session', 'mentee']
        for field in required_fields:
            if field not in data or not data[field]:
                self._errors.append(f"Field '{field}' is required for booking")
        
        return len(self._errors) == 0
    
    def create_mentorship_session(self, mentor, **kwargs) -> Optional[Any]:
        """
        Create a new mentorship session.
        
        Args:
            mentor: FreelancerProfile instance
            **kwargs: Mentorship data
            
        Returns:
            MentorshipSession instance or None if failed
        """
        try:
            from mentorship.models import MentorshipSession
            
            # Validate data
            if not self.validate(kwargs):
                return None
            
            # Create mentorship session
            mentorship = MentorshipSession.objects.create(
                title=kwargs['title'],
                description=kwargs['description'],
                category=kwargs['category'],
                price=kwargs['price'],
                duration_hours=kwargs['duration_hours'],
                notes=kwargs.get('notes', ''),
                mentor=mentor,
            )
            
            return mentorship
            
        except Exception as e:
            self._errors.append(f"Failed to create mentorship: {str(e)}")
            return None
    
    def get_available_mentorships(self, category=None):
        """
        Get available mentorship sessions.
        
        Args:
            category: Optional category filter
            
        Returns:
            QuerySet of available mentorships
        """
        try:
            from mentorship.models import MentorshipSession
            
            queryset = MentorshipSession.objects.filter(
                status=MentorshipSession.AVAILABLE
            ).select_related('mentor__user')
            
            if category:
                queryset = queryset.filter(category=category)
                
            return queryset.order_by('-created_at')
            
        except Exception:
            return MentorshipSession.objects.none()
    
    def get_mentor_mentorships(self, user) -> QuerySet:
        """Get all mentorships where user is the mentor."""
        try:
            from mentorship.models import MentorshipSession
            if hasattr(user, 'freelancerprofile'):
                return MentorshipSession.objects.filter(
                    mentor=user.freelancerprofile
                ).order_by('-created_at')
            return MentorshipSession.objects.none()
        except ImportError:
            # Return empty queryset-like object
            from django.db.models import QuerySet
            return QuerySet().none()
    
    def get_mentee_bookings(self, user) -> QuerySet:
        """Get all bookings where user is the mentee."""
        try:
            from mentorship.models import MentorshipBooking
            if hasattr(user, 'freelancerprofile'):
                return MentorshipBooking.objects.filter(
                    mentee=user.freelancerprofile
                ).order_by('-created_at')
            return MentorshipBooking.objects.none()
        except (ImportError, AttributeError):
            # Return empty queryset-like object
            from django.db.models import QuerySet
            return QuerySet().none()
    
    def get_mentor_bookings(self, user) -> QuerySet:
        """Get all bookings where user is the mentor."""
        try:
            from mentorship.models import MentorshipBooking
            if hasattr(user, 'freelancerprofile'):
                return MentorshipBooking.objects.filter(
                    session__mentor=user.freelancerprofile
                ).order_by('-created_at')
            return MentorshipBooking.objects.none()
        except (ImportError, AttributeError):
            # Return empty queryset-like object
            from django.db.models import QuerySet
            return QuerySet().none()


# Factory function for backward compatibility
def get_mentorship_service():
    """
    Factory function to get MentorshipService instance.
    
    Returns:
        MentorshipService: Service instance for mentorship operations
    """
    return MentorshipService()