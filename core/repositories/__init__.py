__all__ = ['ProfileRepository', 'BaseRepository']

def __getattr__(name):
    if name == 'BaseRepository':
        from .base_repository import BaseRepository
        return BaseRepository
    elif name == 'ProfileRepository':
        from .profile_repository import ProfileRepository
        return ProfileRepository
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")