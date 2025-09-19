from django.conf import settings
from ..interfaces.storage_interface import StorageInterface
from ..storage.local_storage import LocalStorage

'''
El codigo no depende directamente de LocalStorage u otra implementacion, sino de la abstraccion StorageInterface.
Centralizacion de la logica de seleccion concentrada en StorageFactory.
Configurabilidad settings.PROFILE_STORAGE_TYPE para elegir la implementacion deseada.

'''

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
        '''
        elif storage_type == 's3':
            return S3Storage()
        '''