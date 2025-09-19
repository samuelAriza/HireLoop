__all__ = ['BootstrapStylingMixin']

def __getattr__(name):
    if name == 'BootstrapStylingMixin':
        from .forms import BootstrapStylingMixin
        return BootstrapStylingMixin
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")