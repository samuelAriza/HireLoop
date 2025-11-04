from django import forms
from django.utils.translation import gettext_lazy as _
from core.mixins.forms import BootstrapStylingMixin
from ..models import MicroService


class MicroServiceForm(BootstrapStylingMixin, forms.ModelForm):
    image = forms.ImageField(
        label=_("Service Image"),
        required=False,
        help_text=_("Optional. Upload an image for your microservice (JPEG, PNG, GIF). Max 5MB."),
    )

    class Meta:
        model = MicroService
        fields = [
            "category",
            "title",
            "description",
            "price",
            "delivery_time",
            "is_active",
        ]
        labels = {
            "category": _("Category"),
            "title": _("Title"),
            "description": _("Description"),
            "price": _("Price"),
            "delivery_time": _("Delivery Time"),
            "is_active": _("Active"),
        }
        help_texts = {
            "title": _("A clear and attractive title for your service."),
            "description": _("Describe what you offer in detail. Include what’s included and any requirements."),
            "price": _("Fixed price for this service (in USD)."),
            "delivery_time": _("Example: 3 days, 1 week, etc."),
            "is_active": _("Uncheck to hide this service from the marketplace."),
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": _("e.g., I will design a professional logo")}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": _("Detailed description...")}),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": "5", "step": "0.01"}),
            "delivery_time": forms.TextInput(attrs={"class": "form-control", "placeholder": _("e.g., 3 days")}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }