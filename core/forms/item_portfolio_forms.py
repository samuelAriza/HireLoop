from django import forms
from ..models import ItemPortfolio
from ..mixins.forms import BootstrapStylingMixin


class ItemPortfolioForm(BootstrapStylingMixin, forms.ModelForm):
    class Meta:
        model = ItemPortfolio
        fields = ["title", "description", "url_demo"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "url_demo": forms.URLInput(attrs={"placeholder": "https://example.com"}),
        }
