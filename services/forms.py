from django import forms
from .models import Service


class ServiceSearchForm(forms.Form):
    """
    Formulario de búsqueda de servicios.
    Sigue SRP: Solo maneja criterios de búsqueda.
    """
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar servicios...',
            'id': 'search-query'
        })
    )
    
    category = forms.ChoiceField(
        choices=[('', 'Todas las categorías')] + Service.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'category-filter'
        })
    )
    
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio mínimo',
            'min': '0',
            'step': '0.01'
        })
    )
    
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio máximo',
            'min': '0',
            'step': '0.01'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError(
                "El precio mínimo no puede ser mayor al precio máximo"
            )
        
        return cleaned_data