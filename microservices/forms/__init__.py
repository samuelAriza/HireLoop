__all__ = [
    'MicroServiceForm',
]

def __getattr__(name):
    if name == 'MicroServiceForm':
        from .microservices_form import MicroServiceForm
        return MicroServiceForm
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")