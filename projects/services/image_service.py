import uuid
from django.core.files.uploadedfile import UploadedFile
from core.interfaces.storage_interface import StorageInterface
from core.factories.storage_factory import StorageFactory


class ProjectImageService:
    def __init__(self, storage: StorageInterface = None):
        self._storage = storage or StorageFactory.create_storage()

    def upload_project_image(
        self, project_id: uuid.UUID, image_file: UploadedFile
    ) -> str:
        ext = image_file.name.split(".")[-1]
        filename = f"project_{project_id}_{uuid.uuid4().hex}.{ext}"
        path = f"projects/{filename}"
        if not self._is_valid_image(image_file):
            raise ValueError("Invalid image file")
        # Storage saves with full path, but return only filename for ImageField
        self._storage.save(image_file, path)
        return filename

    def delete_project_image(self, image_path: str) -> None:
        """Delete project image from storage."""
        if not image_path:
            return
        
        # If it's just a filename, prepend the projects directory
        if '/' not in image_path:
            full_path = f"projects/{image_path}"
        else:
            full_path = image_path
        
        return self._storage.delete(full_path)

    def get_image_url(self, image_path: str) -> str:
        """
        Get URL for project image.
        image_path can be either:
        - Just the filename (e.g., 'project_xxx.jpg')
        - Full path (e.g., 'projects/project_xxx.jpg')
        """
        if not image_path:
            return self._get_default_image_url()
        
        # If it's just a filename, prepend the projects directory
        if '/' not in image_path:
            full_path = f"projects/{image_path}"
        else:
            full_path = image_path
        
        if self._storage.exists(full_path):
            return self._storage.url(full_path)
        return self._get_default_image_url()

    def _is_valid_image(self, image_file: UploadedFile) -> bool:
        if image_file.size > 5 * 1024 * 1024:
            return False
        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        return image_file.content_type in allowed_types

    def _get_default_image_url(self) -> str:
        return "/static/core/images/default_project.png"
