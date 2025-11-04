import uuid
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.interfaces.storage_interface import StorageInterface
from core.factories.storage_factory import StorageFactory


class MicroserviceImageService:
    """
    Service for handling microservice image upload, deletion, and URL generation.
    Supports local or cloud storage via StorageInterface.
    """

    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif"]

    def __init__(self, storage: StorageInterface = None):
        self._storage: StorageInterface = storage or StorageFactory.create_storage()

    def upload_microservice_image(
        self, microservice_id: uuid.UUID, image_file: UploadedFile
    ) -> str:
        """Upload microservice image and return filename only."""
        file_extension = image_file.name.split(".")[-1]
        filename = f"microservice_{microservice_id}_{uuid.uuid4().hex}.{file_extension}"
        path = f"microservices/{filename}"

        if not self._is_valid_image(image_file):
            raise ValueError("Invalid image file")

        # Storage saves with full path, but return only filename for ImageField
        self._storage.save(image_file, path)
        return filename

    def delete_microservice_image(self, image_path: str) -> None:
        """Delete microservice image from storage."""
        if not image_path:
            return True
        
        # If it's just a filename, prepend the microservices directory
        if '/' not in image_path:
            full_path = f"microservices/{image_path}"
        else:
            full_path = image_path
        
        return self._storage.delete(full_path)

    def get_image_url(self, image_path: str) -> str:
        """
        Get URL for microservice image.
        image_path can be either:
        - Just the filename (e.g., 'microservice_xxx.jpg')
        - Full path (e.g., 'microservices/microservice_xxx.jpg')
        """
        if not image_path:
            return self._get_default_image_url()
        
        # If it's just a filename, prepend the microservices directory
        if '/' not in image_path:
            full_path = f"microservices/{image_path}"
        else:
            full_path = image_path
        
        if self._storage.exists(full_path):
            return self._storage.url(full_path)
        return self._get_default_image_url()

    def _is_valid_image(self, image_file: UploadedFile) -> bool:
        """Validate file size and content type."""
        return (
            image_file.size <= self.MAX_SIZE
            and image_file.content_type in self.ALLOWED_TYPES
        )

    def _get_default_image_url(self) -> str:
        """Return path to default placeholder image."""
        return "/static/core/images/default_microservice.png"