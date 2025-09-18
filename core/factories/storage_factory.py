from django.conf import settings
from ..interfaces.storage_interface import StorageInterface
from ..storage.local_storage import LocalStorage

class StorageFactory:
    """Factory for creating storage instances following DIP."""
    
    @staticmethod
    def create_storage(storage_type: str = None) -> StorageInterface:
        """Create storage instance based on configuration."""
        storage_type = storage_type or getattr(settings, 'PROFILE_STORAGE_TYPE', 'local')
        
        if storage_type == 'local':
            return LocalStorage()
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")