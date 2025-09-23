from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect

from ..forms.auth_forms import RegisterForm, LoginForm
from ..models import User


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "core/register.html"
    success_url = reverse_lazy("core:profile_detail")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "core/login.html"

    def get_success_url(self):
        return reverse_lazy("core:profile_detail")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("core:login")
