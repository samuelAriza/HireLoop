from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import MentorshipSession
from core.mixins.forms import BootstrapStylingMixin


class MentorshipSessionCreateForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = MentorshipSession
        fields = ["topic", "start_time", "duration_minutes", "status"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "status": forms.Select(choices=MentorshipSession.MentorshipStatus.choices),
        }
        labels = {
            "topic": _("Topic"),
            "start_time": _("Start Time"),
            "duration_minutes": _("Duration (minutes)"),
            "status": _("Status"),
        }
        help_texts = {
            "topic": _("Brief description of the mentorship session topic."),
            "start_time": _("Select the date and time when the session will start."),
            "duration_minutes": _("Duration of the session in minutes (e.g., 30, 60)."),
        }


class MentorshipSessionUpdateForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = MentorshipSession
        fields = ["topic", "start_time", "duration_minutes", "status"]
        widgets = {
            "status": forms.Select(choices=MentorshipSession.MentorshipStatus.choices)
        }
        labels = {
            "topic": _("Topic"),
            "start_time": _("Start Time"),
            "duration_minutes": _("Duration (minutes)"),
            "status": _("Status"),
        }
        help_texts = {
            "topic": _("Brief description of the mentorship session topic."),
            "start_time": _("Select the date and time when the session will start."),
            "duration_minutes": _("Duration of the session in minutes (e.g., 30, 60)."),
        }