__all__ = ["RegisterForm", "LoginForm", "ClientProfileForm", "FreelancerProfileForm"]


def __getattr__(name):
    if name == "RegisterForm":
        from .auth_forms import RegisterForm

        return RegisterForm
    elif name == "LoginForm":
        from .auth_forms import LoginForm

        return LoginForm
    elif name == "ClientProfileForm":
        from .profile_forms import ClientProfileForm

        return ClientProfileForm
    elif name == "FreelancerProfileForm":
        from .profile_forms import FreelancerProfileForm

        return FreelancerProfileForm
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
