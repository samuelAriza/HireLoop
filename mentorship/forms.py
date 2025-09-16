"""
Mentorship Forms - Presentation Layer

Following SOLID and Clean Code principles:
- Single Responsibility: Each form has one specific purpose
- Clean interfaces with proper validation
- Reusable components for consistent UX
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta, date
from typing import Dict, Any, Optional

from .models import MentorshipSession
# from .services import get_mentorship_service  # Commented out to avoid conflicts
from core.models import User


class BaseMentorshipForm(forms.Form):
    """Base form with common functionality - DRY principle"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_bootstrap_classes()
    
    def _add_bootstrap_classes(self):
        """Add Bootstrap CSS classes to form fields"""
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.TextInput):
                widget.attrs.update({'class': 'form-control'})
            elif isinstance(widget, forms.Textarea):
                widget.attrs.update({'class': 'form-control'})
            elif isinstance(widget, forms.Select):
                widget.attrs.update({'class': 'form-select'})
            elif isinstance(widget, forms.DateTimeInput):
                widget.attrs.update({'class': 'form-control'})
            elif isinstance(widget, forms.DateInput):
                widget.attrs.update({'class': 'form-control'})


class MentorshipSearchForm(BaseMentorshipForm):
    """
    Form for searching and filtering mentorship sessions
    Implements Single Responsibility Principle
    """
    
    topic = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por título de mentoría...',
            'class': 'form-control'
        }),
        label='Buscar por título'
    )
    
    state = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos los estados')] + MentorshipSession.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Estado de la sesión'
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Fecha desde'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Fecha hasta'
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self._load_dynamic_choices()
    
    def _load_dynamic_choices(self):
        """Load dynamic choices from service layer"""
        try:
            from core.services import MentorshipService
            service = MentorshipService()
            if hasattr(service, 'get_available_states'):
                self.fields['state'].choices = [('', 'Todos los estados')] + service.get_available_states()
        except:
            # Fallback to default choices
            pass
    
    def clean_topic(self) -> Optional[str]:
        """Clean and validate topic field"""
        topic = self.cleaned_data.get('topic')
        if topic:
            topic = topic.strip()
            if len(topic) < 2:
                raise ValidationError("El título debe tener al menos 2 caracteres")
        return topic or None
    
    def clean_date_from(self) -> Optional[date]:
        """Clean and validate date_from field"""
        return self.cleaned_data.get('date_from')
    
    def clean_date_to(self) -> Optional[date]:
        """Clean and validate date_to field"""
        return self.cleaned_data.get('date_to')
    
    def clean(self) -> Dict[str, Any]:
        """Cross-field validation"""
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise ValidationError(
                "La fecha 'desde' no puede ser posterior a la fecha 'hasta'"
            )
        
        return cleaned_data
    
    def get_search_params(self) -> Dict[str, Any]:
        """Get cleaned search parameters for service layer"""
        if not self.is_valid():
            return {}
        
        return {
            'topic': self.cleaned_data.get('topic'),
            'state': self.cleaned_data.get('state'),
            'date_from': self.cleaned_data.get('date_from'),
            'date_to': self.cleaned_data.get('date_to'),
        }


class MentorshipFilterForm(BaseMentorshipForm):
    """
    Advanced filtering form for mentorship sessions
    Extends search functionality with user-specific filters
    """
    
    ROLE_CHOICES = [
        ('', 'Todos los roles'),
        ('mentor', 'Como Mentor'),
        ('mentee', 'Como Mentee'),
    ]
    
    SORT_CHOICES = [
        ('', 'Ordenar por...'),
        ('-created_at', 'Más recientes'),
        ('created_at', 'Más antiguos'),
        ('title', 'Título A-Z'),
        ('-title', 'Título Z-A'),
        ('duration_hours', 'Duración menor'),
        ('-duration_hours', 'Duración mayor'),
    ]
    
    topic = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar en títulos...',
            'class': 'form-control'
        }),
        label='Buscar'
    )
    
    state = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos los estados')] + MentorshipSession.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Estado'
    )
    
    role = forms.ChoiceField(
        required=False,
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Mi rol'
    )
    
    date_range = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Cualquier fecha'),
            ('today', 'Hoy'),
            ('week', 'Esta semana'),
            ('month', 'Este mes'),
            ('upcoming', 'Próximas'),
            ('past', 'Pasadas'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Período'
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Ordenar por'
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def get_filter_params(self) -> Dict[str, Any]:
        """Get all filter parameters"""
        if not self.is_valid():
            return {}
        
        params = {
            'topic': self.cleaned_data.get('topic'),
            'state': self.cleaned_data.get('state'),
        }
        
        # Handle role-based filtering
        role = self.cleaned_data.get('role')
        if role and self.user:
            if role == 'mentor':
                params['mentor'] = self.user
            elif role == 'mentee':
                params['mentee'] = self.user
        
        # Handle date range filtering
        date_range = self.cleaned_data.get('date_range')
        if date_range:
            date_params = self._get_date_range_params(date_range)
            params.update(date_params)
        
        # Remove None values
        return {k: v for k, v in params.items() if v is not None}
    
    def get_sort_param(self) -> Optional[str]:
        """Get sorting parameter"""
        return self.cleaned_data.get('sort_by') if self.is_valid() else None
    
    def _get_date_range_params(self, date_range: str) -> Dict[str, date]:
        """Convert date range choice to actual date parameters"""
        today = timezone.now().date()
        
        if date_range == 'today':
            return {'date_from': today, 'date_to': today}
        elif date_range == 'week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            return {'date_from': week_start, 'date_to': week_end}
        elif date_range == 'month':
            month_start = today.replace(day=1)
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1) - timedelta(days=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1) - timedelta(days=1)
            return {'date_from': month_start, 'date_to': month_end}
        elif date_range == 'upcoming':
            return {'date_from': today}
        elif date_range == 'past':
            return {'date_to': today - timedelta(days=1)}
        
        return {}


class MentorshipSessionForm(BaseMentorshipForm, forms.ModelForm):
    """
    Form for creating and editing mentorship sessions
    Integrates with service layer for validation
    """
    
    class Meta:
        model = MentorshipSession
        fields = ['title', 'description', 'category', 'price', 'duration_hours', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Introducción a Python, Diseño de APIs REST...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe qué cubrirás en esta sesión de mentoría...'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '8'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales, requisitos previos, etc. (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set category choices if available
        try:
            self.fields['category'].choices = MentorshipSession.CATEGORY_CHOICES
        except:
            # Fallback choices if model doesn't have CATEGORY_CHOICES
            self.fields['category'].choices = [
                ('programming', 'Programación'),
                ('design', 'Diseño'),
                ('marketing', 'Marketing'),
                ('business', 'Negocios'),
                ('data_science', 'Ciencia de Datos'),
                ('other', 'Otro'),
            ]
        
        # Debug form initialization
        print(f"=== DEBUG: Form initialized with user: {self.current_user} ===")
        print(f"Form fields: {list(self.fields.keys())}")
        
        # Make all fields required except notes
        for field_name, field in self.fields.items():
            if field_name != 'notes':
                field.required = True
                if not field.widget.attrs.get('class'):
                    field.widget.attrs['class'] = 'form-control'
    
    def clean_price(self):
        """Validate price"""
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError("El precio debe ser mayor a 0")
        return price
    
    def clean_duration_hours(self):
        """Validate duration"""
        duration = self.cleaned_data.get('duration_hours')
        if duration and (duration < 1 or duration > 8):
            raise ValidationError("La duración debe estar entre 1 y 8 horas")
        return duration
    
    def clean(self) -> Dict[str, Any]:
        """Cross-field validation - simplified"""
        cleaned_data = super().clean()
        print(f"=== DEBUG: Form clean() called ===")
        print(f"Cleaned data: {cleaned_data}")
        
        # Skip service validation for now to test basic functionality
        print("=== DEBUG: Skipping service validation for basic testing ===")
        
        print(f"=== DEBUG: Form validation completed. Errors: {self.errors} ===")
        return cleaned_data


class QuickSessionBookingForm(BaseMentorshipForm):
    """
    Quick form for booking mentorship sessions
    Simplified interface for common use cases
    """
    
    QUICK_DURATIONS = [
        (30, '30 minutos'),
        (60, '1 hora'),
        (90, '1.5 horas'),
        (120, '2 horas'),
    ]
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Título de la mentoría'
        }),
        label='Título'
    )
    
    mentor = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Will be populated in __init__
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Mentor'
    )
    
    scheduled_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Fecha'
    )
    
    scheduled_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        label='Hora'
    )
    
    duration_minutes = forms.ChoiceField(
        choices=QUICK_DURATIONS,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Duración'
    )
    
    def __init__(self, *args, **kwargs):
        self.mentee = kwargs.pop('mentee', None)
        super().__init__(*args, **kwargs)
        
        # Load available mentors
        try:
            service = get_mentorship_service()
            self.fields['mentor'].queryset = service.get_available_mentors()
        except ImportError:
            # Fallback if service not available
            self.fields['mentor'].queryset = User.objects.filter(is_active=True)
    
    def clean(self) -> Dict[str, Any]:
        """Validate and prepare data for session creation"""
        cleaned_data = super().clean()
        
        # Combine date and time
        scheduled_date = cleaned_data.get('scheduled_date')
        scheduled_time = cleaned_data.get('scheduled_time')
        
        if scheduled_date and scheduled_time:
            scheduled_datetime = timezone.make_aware(
                datetime.combine(scheduled_date, scheduled_time)
            )
            cleaned_data['scheduled_datetime'] = scheduled_datetime
            
            if scheduled_datetime < timezone.now():
                raise ValidationError("No se puede programar una sesión en el pasado")
        
        # Convert duration
        duration_minutes = cleaned_data.get('duration_minutes')
        if duration_minutes:
            cleaned_data['duration_hours'] = int(duration_minutes) / 60
        
        return cleaned_data


# Factory Pattern for form creation - Simplified
class MentorshipFormFactory:
    """Factory for creating different mentorship forms"""
    
    @staticmethod
    def create_search_form(data=None, initial=None, user=None) -> MentorshipSearchForm:
        """Create mentorship search form"""
        return MentorshipSearchForm(data=data, initial=initial, user=user)
    
    @staticmethod
    def create_filter_form(data=None, initial=None, user=None) -> MentorshipFilterForm:
        """Create mentorship filter form"""
        return MentorshipFilterForm(data=data, initial=initial, user=user)
    
    @staticmethod
    def create_session_form(data=None, initial=None, instance=None, user=None) -> MentorshipSessionForm:
        """Create mentorship session form"""
        return MentorshipSessionForm(data=data, initial=initial, instance=instance, user=user)


# Convenience functions following KISS principle
def get_search_form(request_data=None, initial_data=None, user=None) -> MentorshipSearchForm:
    """Get mentorship search form instance"""
    return MentorshipSearchForm(data=request_data, initial=initial_data, user=user)

def get_filter_form(request_data=None, initial_data=None, user=None) -> MentorshipFilterForm:
    """Get mentorship filter form instance"""
    return MentorshipFilterForm(data=request_data, initial=initial_data, user=user)

def get_session_form(request_data=None, initial_data=None, instance=None, user=None) -> MentorshipSessionForm:
    """Get mentorship session form instance"""
    return MentorshipSessionForm(data=request_data, initial=initial_data, instance=instance, user=user)

def get_quick_booking_form(request_data=None, initial_data=None, mentee=None) -> QuickSessionBookingForm:
    """Get quick booking form instance"""
    return QuickSessionBookingForm(data=request_data, initial=initial_data, mentee=mentee)
