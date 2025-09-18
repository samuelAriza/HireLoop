from abc import ABC, abstractmethod
from typing import Optional
from django.core.files.uploadedfile import UploadedFile

class StorageInterface(ABC):
    """Interface for storage implementations following DIP."""
    
    @abstractmethod
    def save(self, file: UploadedFile, path: str) -> str:
        """Save file and return the saved path."""
        pass
    
    @abstractmethod
    def delete(self, path: str) -> bool:
        """Delete file and return success status."""
        pass
    
    @abstractmethod
    def url(self, path: str) -> str:
        """Get URL for accessing the file."""
        pass
    
    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if file exists."""
        pass