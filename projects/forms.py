"""
Project Forms - Presentation Layer

Following SOLID and Clean Code principles:
- Single Responsibility: Each form has one specific purpose
- Clean interfaces with proper validation
- Reusable components
"""

from django import forms
from django.core.exceptions import ValidationError
from typing import Dict, Any, Optional

from .models import Project
from .services import get_project_service


class BaseProjectForm(forms.Form):
    """Base form with common functionality - DRY principle"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_bootstrap_classes()
    
    def _add_bootstrap_classes(self):
        """Add Bootstrap CSS classes to form fields"""
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})


class ProjectSearchForm(BaseProjectForm):
    """
    Form for searching and filtering projects
    Implements Single Responsibility Principle
    """
    
    query = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar proyectos...',
            'class': 'form-control'
        }),
        label='Buscar por palabra clave'
    )
    
    state = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos los estados')] + Project.STATE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Estado del proyecto'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_dynamic_choices()
    
    def _load_dynamic_choices(self):
        """Load dynamic choices from service layer"""
        service = get_project_service()
        state = service.get_available_states()
        self.fields['state'].choices = [('', 'Todos los estados')] + state

    def clean_query(self) -> Optional[str]:
        """Clean and validate query field"""
        query = self.cleaned_data.get('query')
        if query:
            query = query.strip()
            if len(query) < 2:
                raise ValidationError("La consulta debe tener al menos 2 caracteres")
        return query or None
    
    def clean_state(self) -> Optional[str]:
        """Clean and validate state field"""
        state = self.cleaned_data.get('state')
        return state or None
    
    def get_search_params(self) -> Dict[str, Any]:
        """Get cleaned search parameters for service layer"""
        if not self.is_valid():
            return {}
        
        return {
            'query': self.cleaned_data.get('query'),
            'state': self.cleaned_data.get('state'),
        }


class ProjectFilterForm(BaseProjectForm):
    """
    Advanced filtering form for projects
    Extends search functionality
    """
    
    SORT_CHOICES = [
        ('', 'Ordenar por...'),
        ('-created_at', 'Más recientes'),
        ('created_at', 'Más antiguos'),
        ('title', 'Título A-Z'),
        ('-title', 'Título Z-A'),
        ('-avg_payment', 'Mayor presupuesto'),
        ('avg_payment', 'Menor presupuesto'),
    ]
    
    query = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar en título y descripción...',
            'class': 'form-control'
        }),
        label='Buscar'
    )
    
    state = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos los estados')] + Project.STATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Estado'
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Ordenar por'
    )
    
    def get_filter_params(self) -> Dict[str, Any]:
        """Get all filter parameters"""
        if not self.is_valid():
            return {}
        
        params = {
            'query': self.cleaned_data.get('query'),
            'state': self.cleaned_data.get('state'),
        }
        
        # Remove None values
        return {k: v for k, v in params.items() if v is not None}
    
    def get_sort_param(self) -> Optional[str]:
        """Get sorting parameter"""
        return self.cleaned_data.get('sort_by') if self.is_valid() else None


class ProjectCreateForm(BaseProjectForm, forms.ModelForm):
    """
    Form for creating new projects
    Integrates with service layer for validation
    """
    
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del proyecto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe tu proyecto en detalle...'
            }),
        }
    
    def clean(self) -> Dict[str, Any]:
        """Validate form data using service layer"""
        cleaned_data = super().clean()
        
        try:
            service = get_project_service()
            service.validate_project(cleaned_data)
        except ValidationError as e:
            for error in e.messages:
                self.add_error(None, error)
        
        return cleaned_data


# Factory Pattern for form creation
class ProjectFormFactory:
    """Factory for creating different project forms"""
    
    @staticmethod
    def create_search_form(data=None, initial=None) -> ProjectSearchForm:
        """Create project search form"""
        return ProjectSearchForm(data=data, initial=initial)
    
    @staticmethod
    def create_filter_form(data=None, initial=None) -> ProjectFilterForm:
        """Create project filter form"""
        return ProjectFilterForm(data=data, initial=initial)
    
    @staticmethod
    def create_project_form(data=None, initial=None, instance=None) -> ProjectCreateForm:
        """Create project creation form"""
        return ProjectCreateForm(data=data, initial=initial, instance=instance)


# Convenience functions following KISS principle
def get_search_form(request_data=None, initial_data=None) -> ProjectSearchForm:
    """Get project search form instance"""
    return ProjectFormFactory.create_search_form(data=request_data, initial=initial_data)

def get_filter_form(request_data=None, initial_data=None) -> ProjectFilterForm:
    """Get project filter form instance"""
    return ProjectFormFactory.create_filter_form(data=request_data, initial=initial_data)

def get_project_form(request_data=None, initial_data=None, instance=None) -> ProjectCreateForm:
    """Get project creation form instance"""
    return ProjectFormFactory.create_project_form(data=request_data, initial=initial_data, instance=instance)
