import uuid
from django.core.files.uploadedfile import UploadedFile
from ..interfaces.storage_interface import StorageInterface
from ..factories.storage_factory import StorageFactory

class ProfileImageService:
    """Service for handling profile images following SRP and DIP."""

    def __init__(self, storage: StorageInterface = None):
        self._storage = storage or StorageFactory.create_storage()

    def upload_profile_image(self, user_id: int, image_file: UploadedFile) -> str:
        """Upload profile image and return the saved path."""
        # Generate unique filename
        file_extension = image_file.name.split(".")[-1]
        filename = f"profile_{user_id}_{uuid.uuid4().hex}.{file_extension}"
        path = f"profiles/{filename}"

        # Validate image
        if not self._is_valid_image(image_file):
            raise ValueError("Invalid image file")

        # Save image
        saved_path = self._storage.save(image_file, path)
        return saved_path

    def delete_profile_image(self, image_path: str) -> bool:
        """Delete profile image."""
        if not image_path:
            return True
        return self._storage.delete(image_path)

    def get_image_url(self, image_path: str) -> str:
        """Get URL for profile image."""
        if not image_path:
            return self._get_default_image_url()

        if self._storage.exists(image_path):
            return self._storage.url(image_path)

        return self._get_default_image_url()

    def _is_valid_image(self, image_file: UploadedFile) -> bool:
        """Validate image file."""
        # Size validation (max 5MB)
        if image_file.size > 5 * 1024 * 1024:
            return False

        # Type validation
        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        if image_file.content_type not in allowed_types:
            return False

        return True

    def _get_default_image_url(self) -> str:
        """Get default profile image URL."""
        return "/static/core/images/default.png"
