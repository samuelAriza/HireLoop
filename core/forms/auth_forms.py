from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ..mixins.forms import BootstrapStylingMixin

User = get_user_model()


class RegisterForm(BootstrapStylingMixin, UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Username")}
        ),
        label=_("Username")
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("your@email.com")}
        ),
        label=_("Email")
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "password1": _("Password"),
            "password2": _("Password confirmation"),
        }
        help_texts = {
            "password1": _(
                "Enter a password with at least 8 characters, including letters and numbers."
            ),
        }


class LoginForm(BootstrapStylingMixin, AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Username")}
        ),
        label=_("Username")
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Password")}
        ),
        label=_("Password")
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }