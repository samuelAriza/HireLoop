import uuid
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _
from ..interfaces.storage_interface import StorageInterface
from ..factories.storage_factory import StorageFactory


class BaseImageService:
    """Base service for handling images following SRP and DIP."""

    def __init__(self, storage: StorageInterface = None):
        self._storage = storage or StorageFactory.create_storage()

    def upload_image(
        self, identifier: str, image_file: UploadedFile, path_prefix: str
    ) -> str:
        """Upload image and return the saved path."""
        # Generate unique filename
        file_extension = image_file.name.split(".")[-1]
        filename = f"{path_prefix}_{identifier}_{uuid.uuid4().hex}.{file_extension}"
        path = f"{self.get_upload_directory()}/{filename}"

        # Validate image
        if not self._is_valid_image(image_file):
            raise ValueError(_("Invalid image file"))

        # Save image
        saved_path = self._storage.save(image_file, path)
        return saved_path

    def delete_image(self, image_path: str) -> bool:
        """Delete image."""
        if not image_path:
            return True
        return self._storage.delete(image_path)

    def get_image_url(self, image_path: str) -> str:
        """Get URL for image."""
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
        allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        if image_file.content_type not in allowed_types:
            return False

        return True

    def get_upload_directory(self) -> str:
        """Get the upload directory for this service. Override in subclasses."""
        raise NotImplementedError(_("Subclasses must implement get_upload_directory"))

    def _get_default_image_url(self) -> str:
        """Get default image URL. Override in subclasses."""
        raise NotImplementedError(_("Subclasses must implement _get_default_image_url"))


class ProfileImageService(BaseImageService):
    """Service for handling profile images following SRP and DIP."""

    def upload_profile_image(self, user_id: int, image_file: UploadedFile) -> str:
        """Upload profile image and return the saved path."""
        return self.upload_image(str(user_id), image_file, "profile")

    def delete_profile_image(self, image_path: str) -> bool:
        """Delete profile image."""
        return self.delete_image(image_path)

    def get_upload_directory(self) -> str:
        """Get upload directory for profile images."""
        return "profiles"

    def _get_default_image_url(self) -> str:
        """Get default profile image URL."""
        return "/static/core/images/default.png"


class PortfolioImageService(BaseImageService):
    """Service for handling portfolio item images following SRP and DIP."""

    def upload_portfolio_image(
        self, portfolio_id: str, image_file: UploadedFile
    ) -> str:
        """Upload portfolio image and return the saved path."""
        return self.upload_image(portfolio_id, image_file, "portfolio")

    def delete_portfolio_image(self, image_path: str) -> bool:
        """Delete portfolio image."""
        return self.delete_image(image_path)

    def get_upload_directory(self) -> str:
        """Get upload directory for portfolio images."""
        return "portfolios"

    def _get_default_image_url(self) -> str:
        """Get default portfolio image URL."""
        return "/static/core/images/default_portfolio.png"