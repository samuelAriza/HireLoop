__all__ = ["MicroServiceRepository"]

def __getattr__(name):
    if name == "MicroServiceRepository":
        from .microservices_repository import MicroServiceRepository

        return MicroServiceRepository
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
