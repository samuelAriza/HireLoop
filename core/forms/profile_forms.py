from django import forms
from ..models import ClientProfile, FreelancerProfile, User
from ..mixins.forms import BootstrapStylingMixin
from ..utils.validators import SkillValidator


class ClientProfileForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ["company", "billing_address", "billing_email"]


class FreelancerProfileForm(BootstrapStylingMixin, forms.ModelForm):
    skills = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter skills separated by commas (e.g., Python, Django, JavaScript)"
            }
        ),
        help_text="Enter your skills separated by commas",
        validators=[SkillValidator()],
    )

    class Meta:
        model = FreelancerProfile
        fields = ["bio", "skills"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class ProfileImageForm(BootstrapStylingMixin, forms.ModelForm):
    """Form for updating profile image."""

    class Meta:
        model = User
        fields = ["profile_image"]
        widgets = {"profile_image": forms.FileInput(attrs={"accept": "image/*"})}

    def clean_profile_image(self):
        image = self.cleaned_data.get("profile_image")
        if image:
            # Size validation
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("Image size must be less than 5MB")

            # Type validation
            if not image.content_type.startswith("image"):
                raise forms.ValidationError("File must be an image")

        return image
