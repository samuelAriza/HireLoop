from django import forms
from django.forms import widgets


class BootstrapStylingMixin:
    """
    Automatically adds Bootstrap classes to form widgets.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                widget.attrs["class"] = (
                    widget.attrs.get("class", "") + " form-check-input"
                ).strip()
            elif isinstance(
                widget,
                (forms.Select, forms.TextInput, forms.NumberInput, forms.Textarea),
            ):
                widget.attrs["class"] = (
                    widget.attrs.get("class", "") + " form-control"
                ).strip()
            elif isinstance(widget, widgets.Input):
                widget.attrs["class"] = (
                    widget.attrs.get("class", "") + " form-control"
                ).strip()
