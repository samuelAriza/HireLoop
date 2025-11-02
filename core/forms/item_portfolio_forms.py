from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import ItemPortfolio
from ..mixins.forms import BootstrapStylingMixin


class ItemPortfolioForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ItemPortfolio
        fields = ["title", "description", "url_demo", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "url_demo": forms.URLInput(attrs={"placeholder": _("https://example.com")}),
        }
        labels = {
            "title": _("Title"),
            "description": _("Description"),
            "url_demo": _("Demo URL"),
            "image": _("Image"),
        }
        help_texts = {
            "url_demo": _("Optional: Provide a link to a live demo or example of your work."),
            "image": _("Upload an image showcasing your work. Supported formats: JPEG, PNG, GIF, WebP."),
        }


class PortfolioImageForm(forms.ModelForm):
    """Form for updating portfolio item image only."""

    class Meta:
        model = ItemPortfolio
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(
                attrs={
                    "accept": "image/jpeg,image/png,image/gif,image/webp",
                    "class": "form-control"
                }
            )
        }
        labels = {
            "image": _("Update Image")
        }
        help_texts = {
            "image": _("Choose a new image to replace the current one. Supported formats: JPEG, PNG, GIF, WebP.")
        }