import uuid
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.interfaces.storage_interface import StorageInterface
from core.factories.storage_factory import StorageFactory


class MentorshipImageService:
    def __init__(self, storage: StorageInterface = None):
        self.storage: StorageInterface = storage or StorageFactory.create_storage()

    def upload_mentorship_image(
        self, mentorship_id: uuid.UUID, image_file: UploadedFile
    ) -> str:
        ext = image_file.name.split(".")[-1]
        filename = f"mentorship_{mentorship_id}_{uuid.uuid4().hex}.{ext}"
        path = f"mentorships/{filename}"
        if not self._is_valid_image(image_file):
            raise ValidationError(_("Invalid image file"))
        return self.storage.save(image_file, path)

    def delete_mentorship_image(self, image_path: str) -> None:
        if image_path:
            return self.storage.delete(image_path)

    def get_image_url(self, image_path: str) -> str:
        if not image_path:
            return self._get_default_image_url()
        if self.storage.exists(image_path):
            return self.storage.url(image_path)
        return self._get_default_image_url()

    def _is_valid_image(self, image_file: UploadedFile) -> bool:
        if image_file.size > 5 * 1024 * 1024:
            return False
        allowed_types = ["image/jpeg", "image/png", "image/gif"]
        return image_file.content_type in allowed_types

    def _get_default_image_url(self) -> str:
        return "/static/core/images/default_mentorship.png"