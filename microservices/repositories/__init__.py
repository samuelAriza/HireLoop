__all__ = ['MicroServiceRepository']

from core.repositories.base_repository import BaseRepository


def __getattr__(name):
    if name == 'MicroServiceRepository':
        from .microservices_repository import MicroServiceRepository
        return MicroServiceRepository
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")