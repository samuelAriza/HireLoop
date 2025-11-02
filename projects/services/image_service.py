import uuid
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.interfaces.storage_interface import StorageInterface
from core.factories.storage_factory import StorageFactory


class ProjectImageService:
    """
    Service for handling project image upload, deletion, and URL generation.
    Supports local or cloud storage via StorageInterface.
    """

    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif"]

    def __init__(self, storage: StorageInterface = None):
        self._storage: StorageInterface = storage or StorageFactory.create_storage()

    def upload_project_image(
        self, project_id: uuid.UUID, image_file: UploadedFile
    ) -> str:
        """
        Upload project image and return storage path.
        Raises ValidationError if file is invalid.
        """
        if not self._is_valid_image(image_file):
            raise ValidationError(
                _("Invalid image file. Must be JPEG, PNG, or GIF and under 5MB.")
            )

        file_extension = image_file.name.split(".")[-1].lower()
        filename = f"project_{project_id}_{uuid.uuid4().hex}.{file_extension}"
        path = f"projects/{filename}"

        return self._storage.save(image_file, path)

    def delete_project_image(self, image_path: str) -> bool:
        """
        Delete image from storage if path exists.
        Returns True on success or if path is empty, False on failure.
        """
        if not image_path:
            return True
        try:
            return self._storage.delete(image_path)
        except Exception:
            return False

    def get_image_url(self, image_path: str) -> str:
        """
        Return image URL or default placeholder.
        """
        if not image_path:
            return self._get_default_image_url()

        if self._storage.exists(image_path):
            return self._storage.url(image_path)

        return self._get_default_image_url()

    def _is_valid_image(self, image_file: UploadedFile) -> bool:
        """Validate file size and content type."""
        return (
            image_file.size <= self.MAX_SIZE
            and image_file.content_type in self.ALLOWED_TYPES
        )

    def _get_default_image_url(self) -> str:
        """Return path to default placeholder image."""
        return "/static/core/images/default_project.png"