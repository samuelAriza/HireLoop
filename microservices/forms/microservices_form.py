from django import forms
from core.mixins.forms import BootstrapStylingMixin
from ..models import MicroService

class MicroServiceForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = MicroService
        fields = ['category', 'title', 'description', 'price', 'delivery_time', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_time': forms.TextInput(attrs={'placeholder': 'Ej: 3 days'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
