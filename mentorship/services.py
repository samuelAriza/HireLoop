"""
Mentorship Services - Business Logic Layer

Following SOLID principles and Clean Architecture:
- Single Responsibility: Each service class has one clear responsibility
- Open/Closed: Easily extensible without modifying existing code
- Liskov Substitution: Abstract base classes for consistent interfaces
- Interface Segregation: Small, focused interfaces
- Dependency Inversion: Depend on abstractions, not concretions
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta, date
from django.db import models
from django.db.models import Q, Count, Avg, F, Sum, Case, When, IntegerField
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import MentorshipSession
from core.models import User


class MentorshipSearchInterface(ABC):
    """Abstract interface for mentorship search operations"""
    
    @abstractmethod
    def search_sessions(self, topic: Optional[str] = None, state: Optional[str] = None,
                       mentor: Optional[User] = None, mentee: Optional[User] = None,
                       date_from: Optional[date] = None, date_to: Optional[date] = None) -> models.QuerySet:
        pass
    
    @abstractmethod
    def get_available_mentors(self) -> models.QuerySet:
        pass
    
    @abstractmethod
    def get_session_stats(self, user: User) -> Dict[str, Any]:
        pass


class MentorshipValidatorInterface(ABC):
    """Abstract interface for mentorship validation"""
    
    @abstractmethod
    def validate_session_data(self, data: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def validate_session_timing(self, start_time: datetime, duration: timedelta, 
                               mentor: User, exclude_session: Optional[str] = None) -> None:
        pass


class MentorshipAnalyticsInterface(ABC):
    """Abstract interface for mentorship analytics"""
    
    @abstractmethod
    def get_mentor_performance(self, mentor: User) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_mentee_progress(self, mentee: User) -> Dict[str, Any]:
        pass


class MentorshipSearchService(MentorshipSearchInterface):
    """
    Service for handling mentorship search and filtering operations
    Implements Single Responsibility Principle
    """
    
    def __init__(self):
        self.base_queryset = self._get_optimized_queryset()
    
    def _get_optimized_queryset(self) -> models.QuerySet:
        """Get optimized queryset to prevent N+1 queries"""
        return MentorshipSession.objects.select_related(
            'mentor',
            'mentee'
        ).annotate(
            mentor_name=F('mentor__user__username'),
            mentee_name=F('mentee__user__username'),
            duration_in_hours=F('duration_hours')
        )
    
    def search_sessions(self, topic: Optional[str] = None, state: Optional[str] = None,
                       mentor: Optional[User] = None, mentee: Optional[User] = None,
                       date_from: Optional[date] = None, date_to: Optional[date] = None) -> models.QuerySet:
        """
        Search mentorship sessions with multiple filters
        
        Args:
            topic: Text search in session topics
            state: Session state filter
            mentor: Filter by specific mentor
            mentee: Filter by specific mentee
            date_from: Start date filter
            date_to: End date filter
            
        Returns:
            Filtered and optimized QuerySet
        """
        queryset = self.base_queryset
        
        if topic:
            queryset = queryset.filter(topic__icontains=topic)
        
        if state:
            queryset = queryset.filter(state=state)
        
        if mentor:
            queryset = queryset.filter(mentor=mentor)
        
        if mentee:
            queryset = queryset.filter(mentee=mentee)
        
        if date_from:
            queryset = queryset.filter(start_time__date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(start_time__date__lte=date_to)
        
        return queryset.order_by('-start_time')
    
    def get_available_mentors(self) -> models.QuerySet:
        """Get list of available mentors with session statistics"""
        from django.db.models import Count, Case, When, IntegerField
        
        return User.objects.annotate(
            total_sessions=Count('mentor_sessions'),
            completed_sessions=Count(
                Case(
                    When(mentor_sessions__state='COMPLETED', then=1),
                    output_field=IntegerField()
                )
            )
        ).filter(
            mentor_sessions__isnull=False
        ).distinct().order_by('-completed_sessions')
    
    def get_session_stats(self, user: User) -> Dict[str, Any]:
        """Get comprehensive session statistics for a user"""
        mentor_sessions = user.mentor_sessions.all()
        mentee_sessions = user.mentee_sessions.all()
        
        return {
            'as_mentor': {
                'total': mentor_sessions.count(),
                'completed': mentor_sessions.filter(state='COMPLETED').count(),
                'scheduled': mentor_sessions.filter(state='SCHEDULED').count(),
                'canceled': mentor_sessions.filter(state='CANCELED').count(),
                'no_show': mentor_sessions.filter(state='NO_SHOW').count(),
            },
            'as_mentee': {
                'total': mentee_sessions.count(),
                'completed': mentee_sessions.filter(state='COMPLETED').count(),
                'scheduled': mentee_sessions.filter(state='SCHEDULED').count(),
                'canceled': mentee_sessions.filter(state='CANCELED').count(),
                'no_show': mentee_sessions.filter(state='NO_SHOW').count(),
            },
            'upcoming_sessions': self._get_upcoming_sessions(user),
        }
    
    def _get_upcoming_sessions(self, user: User) -> List[Dict]:
        """Get upcoming sessions for a user"""
        upcoming = MentorshipSession.objects.filter(
            Q(mentor=user) | Q(mentee=user),
            state='SCHEDULED',
            start_time__gt=timezone.now()
        ).order_by('start_time')[:5]
        
        return [
            {
                'id': str(session.id),
                'topic': session.topic,
                'start_time': session.start_time,
                'duration': session.duration,
                'role': 'mentor' if session.mentor == user else 'mentee',
                'other_user': session.mentee if session.mentor == user else session.mentor,
            }
            for session in upcoming
        ]


class MentorshipValidator(MentorshipValidatorInterface):
    """
    Service for mentorship data validation
    Implements Single Responsibility Principle
    """
    
    def validate_session_data(self, data: Dict[str, Any]) -> None:
        """Validate mentorship session data"""
        errors = []
        
        # Topic validation
        if not data.get('topic', '').strip():
            errors.append("El tema de la mentoría es requerido")
        
        if len(data.get('topic', '')) > 255:
            errors.append("El tema no puede exceder 255 caracteres")
        
        # Time validation
        start_time = data.get('start_time')
        if not start_time:
            errors.append("La fecha y hora de inicio son requeridas")
        elif start_time < timezone.now():
            errors.append("La sesión no puede programarse en el pasado")
        
        # Duration validation
        duration = data.get('duration')
        if not duration:
            errors.append("La duración de la sesión es requerida")
        elif duration < timedelta(minutes=15):
            errors.append("La duración mínima es de 15 minutos")
        elif duration > timedelta(hours=4):
            errors.append("La duración máxima es de 4 horas")
        
        # Users validation
        mentor = data.get('mentor')
        mentee = data.get('mentee')
        
        if not mentor:
            errors.append("Se requiere un mentor")
        
        if not mentee:
            errors.append("Se requiere un mentee")
        
        if mentor and mentee and mentor == mentee:
            errors.append("El mentor y el mentee no pueden ser la misma persona")
        
        # State validation
        state = data.get('state', 'SCHEDULED')
        valid_states = dict(MentorshipSession.STATUS_CHOICES).keys()
        if state not in valid_states:
            errors.append("Estado de sesión inválido")
        
        if errors:
            raise ValidationError(errors)
    
    def validate_session_timing(self, start_time: datetime, duration: timedelta, 
                               mentor: User, exclude_session: Optional[str] = None) -> None:
        """Validate that the session timing doesn't conflict with existing sessions"""
        end_time = start_time + duration
        
        # Check for overlapping sessions for the mentor
        overlapping_query = Q(
            mentor=mentor,
            state='SCHEDULED',
            start_time__lt=end_time,
            start_time__gt=start_time - F('duration')
        )
        
        if exclude_session:
            overlapping_query &= ~Q(id=exclude_session)

        overlapping_sessions = MentorshipSession.objects.filter(overlapping_query)

        if overlapping_sessions.exists():
            raise ValidationError(
                "El mentor ya tiene una sesión programada en este horario"
            )


class MentorshipAnalyticsService(MentorshipAnalyticsInterface):
    """
    Service for mentorship analytics and reporting
    Implements Single Responsibility Principle
    """
    
    def get_mentor_performance(self, mentor: User) -> Dict[str, Any]:
        """Get detailed performance metrics for a mentor"""
        sessions = mentor.mentor_sessions.all()
        completed_sessions = sessions.filter(state='COMPLETED')
        
        if not sessions.exists():
            return self._empty_performance_stats()
        
        total_duration = sum(
            [session.duration for session in completed_sessions],
            timedelta()
        )
        
        return {
            'total_sessions': sessions.count(),
            'completed_sessions': completed_sessions.count(),
            'completion_rate': (completed_sessions.count() / sessions.count()) * 100,
            'total_hours': total_duration.total_seconds() / 3600,
            'avg_session_duration': total_duration / completed_sessions.count() if completed_sessions.exists() else timedelta(),
            'no_show_rate': (sessions.filter(state='NO_SHOW').count() / sessions.count()) * 100,
            'cancellation_rate': (sessions.filter(state='CANCELED').count() / sessions.count()) * 100,
            'most_common_topics': self._get_common_topics(mentor),
        }
    
    def get_mentee_progress(self, mentee: User) -> Dict[str, Any]:
        """Get progress metrics for a mentee"""
        sessions = mentee.mentee_sessions.all()
        completed_sessions = sessions.filter(state='COMPLETED')
        
        if not sessions.exists():
            return self._empty_progress_stats()
        
        return {
            'total_sessions': sessions.count(),
            'completed_sessions': completed_sessions.count(),
            'hours_learned': sum([s.duration for s in completed_sessions], timedelta()).total_seconds() / 3600,
            'different_mentors': sessions.values('mentor').distinct().count(),
            'learning_topics': list(sessions.values_list('topic', flat=True).distinct()),
            'recent_activity': self._get_recent_activity(mentee),
        }
    
    def _get_common_topics(self, mentor: User) -> List[Dict[str, Any]]:
        """Get most common topics for a mentor"""
        return list(
            mentor.mentor_sessions.values('topic')
            .annotate(count=Count('topic'))
            .order_by('-count')[:5]
        )
    
    def _get_recent_activity(self, mentee: User) -> List[Dict[str, Any]]:
        """Get recent mentorship activity for a mentee"""
        recent_sessions = mentee.mentee_sessions.filter(
            state='COMPLETED'
        ).order_by('-start_time')[:5]
        
        return [
            {
                'topic': session.topic,
                'mentor': session.mentor.username,
                'date': session.start_time.date(),
                'duration': session.duration,
            }
            for session in recent_sessions
        ]
    
    def _empty_performance_stats(self) -> Dict[str, Any]:
        """Return empty performance stats structure"""
        return {
            'total_sessions': 0,
            'completed_sessions': 0,
            'completion_rate': 0,
            'total_hours': 0,
            'avg_session_duration': timedelta(),
            'no_show_rate': 0,
            'cancellation_rate': 0,
            'most_common_topics': [],
        }
    
    def _empty_progress_stats(self) -> Dict[str, Any]:
        """Return empty progress stats structure"""
        return {
            'total_sessions': 0,
            'completed_sessions': 0,
            'hours_learned': 0,
            'different_mentors': 0,
            'learning_topics': [],
            'recent_activity': [],
        }


class MentorshipService:
    """
    Main mentorship service - Facade pattern
    Coordinates between different services following Dependency Inversion
    """
    
    def __init__(self, 
                 search_service: Optional[MentorshipSearchInterface] = None,
                 validator: Optional[MentorshipValidatorInterface] = None,
                 analytics_service: Optional[MentorshipAnalyticsInterface] = None):
        # Dependency Injection - depends on abstractions
        self.search_service = search_service or MentorshipSearchService()
        self.validator = validator or MentorshipValidator()
        self.analytics_service = analytics_service or MentorshipAnalyticsService()
    
    def get_sessions(self, **filters) -> models.QuerySet:
        """Get filtered mentorship sessions"""
        return self.search_service.search_sessions(**filters)
    
    def get_session_with_details(self, session_id: str) -> Optional[MentorshipSession]:
        """Get a single session with all related data"""
        try:
            return self.search_service._get_optimized_queryset().get(id=session_id)
        except MentorshipSession.DoesNotExist:
            return None
    
    def get_available_mentors(self) -> models.QuerySet:
        """Get list of available mentors"""
        return self.search_service.get_available_mentors()
    
    def get_user_stats(self, user: User) -> Dict[str, Any]:
        """Get user statistics"""
        return self.search_service.get_session_stats(user)
    
    def get_mentor_performance(self, mentor: User) -> Dict[str, Any]:
        """Get mentor performance metrics"""
        return self.analytics_service.get_mentor_performance(mentor)
    
    def get_mentee_progress(self, mentee: User) -> Dict[str, Any]:
        """Get mentee progress metrics"""
        return self.analytics_service.get_mentee_progress(mentee)
    
    def validate_session(self, data: Dict[str, Any]) -> None:
        """Validate session data"""
        self.validator.validate_session_data(data)
    
    def validate_timing(self, start_time: datetime, duration: timedelta, 
                       mentor: User, exclude_session: Optional[str] = None) -> None:
        """Validate session timing"""
        self.validator.validate_session_timing(start_time, duration, mentor, exclude_session)
    
    def get_available_states(self) -> List[tuple]:
        """Get all available session states"""
        return MentorshipSession.STATUS_CHOICES


# Factory Pattern for service creation
class MentorshipServiceFactory:
    """Factory for creating mentorship services with different configurations"""
    
    @staticmethod
    def create_default_service() -> MentorshipService:
        """Create service with default implementations"""
        return MentorshipService()
    
    @staticmethod
    def create_custom_service(search_service: MentorshipSearchInterface,
                            validator: MentorshipValidatorInterface,
                            analytics_service: MentorshipAnalyticsInterface) -> MentorshipService:
        """Create service with custom implementations"""
        return MentorshipService(
            search_service=search_service,
            validator=validator,
            analytics_service=analytics_service
        )


# Singleton pattern for global service instance
class MentorshipServiceManager:
    """Singleton manager for mentorship service"""
    
    _instance = None
    _service = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_service(self) -> MentorshipService:
        """Get or create mentorship service instance"""
        if self._service is None:
            self._service = MentorshipServiceFactory.create_default_service()
        return self._service
    
    def set_service(self, service: MentorshipService):
        """Set custom service instance"""
        self._service = service


# Convenience function following KISS principle
def get_mentorship_service() -> MentorshipService:
    """Simple function to get mentorship service instance"""
    return MentorshipServiceManager().get_service()
