__all__ = ["BootstrapStylingMixin", "ProfileRequiredMixin"]


def __getattr__(name):
    if name == "BootstrapStylingMixin":
        from .forms import BootstrapStylingMixin

        return BootstrapStylingMixin
    elif name == "ProfileRequiredMixin":
        from .views import ProfileRequiredMixin

        return ProfileRequiredMixin
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
