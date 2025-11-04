from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from ..interfaces.storage_interface import StorageInterface


class GCSStorage(StorageInterface):
    """Google Cloud Storage implementation using django-storages backend."""

    def save(self, file: UploadedFile, path: str) -> str:
        """
        Save file to GCS.
        Returns the full path as saved in storage.
        """
        saved_path = default_storage.save(path, file)
        print(f"GCSStorage.save - Input path: {path}, Saved path: {saved_path}")
        return saved_path

    def delete(self, path: str) -> bool:
        """Delete file from GCS."""
        try:
            if default_storage.exists(path):
                default_storage.delete(path)
                return True
            return False
        except Exception:
            return False

    def url(self, path: str) -> str:
        """Get public URL for GCS file."""
        try:
            return default_storage.url(path)
        except Exception:
            return ""

    def exists(self, path: str) -> bool:
        """Check if file exists in GCS."""
        try:
            return default_storage.exists(path)
        except Exception:
            return False
