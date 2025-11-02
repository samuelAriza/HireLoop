from django import forms
from ..models import ItemPortfolio
from ..mixins.forms import BootstrapStylingMixin


class ItemPortfolioForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ItemPortfolio
        fields = ["title", "description", "url_demo", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "url_demo": forms.URLInput(attrs={"placeholder": "https://example.com"}),
        }


class PortfolioImageForm(forms.ModelForm):
    """Form for updating portfolio item image only."""

    class Meta:
        model = ItemPortfolio
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(
                attrs={"accept": "image/jpeg,image/png,image/gif,image/webp"}
            )
        }

