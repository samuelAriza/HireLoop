# Simple export sin importación inmediata
__all__ = ['ProfileService']

def __getattr__(name):
    if name == 'ProfileService':
        from .profile_service import ProfileService
        return ProfileService
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")