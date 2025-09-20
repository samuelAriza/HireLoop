from django import forms
from ..models import MentorshipSession
from core.mixins.forms import BootstrapStylingMixin

class MentorshipSessionCreateForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = MentorshipSession
        fields = ['topic', 'start_time', 'duration_minutes', 'status']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(choices=MentorshipSession.MentorshipStatus.choices)
        }

class MentorshipSessionUpdateForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = MentorshipSession
        fields = ['topic', 'start_time', 'duration_minutes', 'status']
        widgets = {
            'status': forms.Select(choices=MentorshipSession.MentorshipStatus.choices)
        }