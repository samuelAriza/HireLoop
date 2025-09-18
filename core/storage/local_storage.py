import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from ..interfaces.storage_interface import StorageInterface

class LocalStorage(StorageInterface):
    """Local file system storage implementation."""
    
    def save(self, file: UploadedFile, path: str) -> str:
        """Save file to local storage."""
        return default_storage.save(path, file)
    
    def delete(self, path: str) -> bool:
        """Delete file from local storage."""
        try:
            if default_storage.exists(path):
                default_storage.delete(path)
                return True
            return False
        except Exception:
            return False
    
    def url(self, path: str) -> str:
        """Get URL for local file."""
        return default_storage.url(path)
    
    def exists(self, path: str) -> bool:
        """Check if file exists locally."""
        return default_storage.exists(path)