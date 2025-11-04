from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import ClientProfile, FreelancerProfile, User
from ..mixins.forms import BootstrapStylingMixin
from ..utils.validators import SkillValidator


class ClientProfileForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ["company", "billing_address", "billing_email"]
        labels = {
            "company": _("Company"),
            "billing_address": _("Billing Address"),
            "billing_email": _("Billing Email"),
        }
        help_texts = {
            "billing_email": _("Email used for invoices and payment notifications."),
        }


class FreelancerProfileForm(BootstrapStylingMixin, forms.ModelForm):
    skills = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Enter skills separated by commas (e.g., Python, Django, JavaScript)"),
                "class": "form-control"
            }
        ),
        label=_("Skills"),
        help_text=_("Enter your skills separated by commas"),
        validators=[SkillValidator()],
    )

    class Meta:
        model = FreelancerProfile
        fields = ["bio", "skills"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }
        labels = {
            "bio": _("Bio"),
        }
        help_texts = {
            "bio": _("Tell us about yourself, your experience, and what you specialize in."),
        }


class ProfileImageForm(BootstrapStylingMixin, forms.ModelForm):
    """Form for updating profile image."""

    class Meta:
        model = User
        fields = ["profile_image"]
        widgets = {
            "profile_image": forms.FileInput(
                attrs={
                    "accept": "image/*",
                    "class": "form-control"
                }
            )
        }
        labels = {
            "profile_image": _("Profile Image")
        }
        help_texts = {
            "profile_image": _("Upload a profile picture. Max size: 5MB. Supported formats: JPG, PNG, GIF, WebP.")
        }

    def clean_profile_image(self):
        image = self.cleaned_data.get("profile_image")
        if image:
            # Size validation
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError(_("Image size must be less than 5MB"))

            # Type validation
            if not image.content_type.startswith("image"):
                raise forms.ValidationError(_("File must be an image"))

        return image