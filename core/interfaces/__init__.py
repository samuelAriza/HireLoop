__all__ = [
    'StorageInterface', 'PurchasableInterface'
]

def __getattr__(name):
    if name == 'StorageInterface':
        from .storage_interface import StorageInterface
        return StorageInterface
    elif name == 'PurchasableInterface':
        from .cart_interface import PurchasableInterface
        return PurchasableInterface
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")