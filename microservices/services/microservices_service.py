# services/services/microservices_service.py
from typing import List, Optional
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.models import FreelancerProfile
from ..models import MicroService
from ..repositories.microservices_repository import MicroServiceRepository


class MicroServiceService:
    """
    Service layer for business logic around MicroServices.
    Uses repository for persistence operations.
    """

    def __init__(self, repository: MicroServiceRepository = None):
        self.repository = repository or MicroServiceRepository()

    def create_microservice(
        self, freelancer: FreelancerProfile, data: dict
    ) -> MicroService:
        """
        Create a new microservice for the given freelancer.
        Validates ownership and data before creation.
        """
        if not freelancer:
            raise ValidationError(_("Freelancer profile is required."))

        return self.repository.create(freelancer=freelancer, **data)

    def update_microservice(
        self, microservice: MicroService, data: dict
    ) -> MicroService:
        """
        Update an existing microservice.
        Ensures the microservice exists and belongs to the freelancer.
        """
        if not microservice:
            raise ValidationError(_("Microservice does not exist."))

        return self.repository.update(microservice, **data)

    def list_freelancer_microservices(
        self, freelancer: FreelancerProfile
    ) -> List[MicroService]:
        """
        List all microservices created by the given freelancer.
        """
        if not freelancer:
            return []

        return self.repository.list_by_freelancer(freelancer)

    def list_active_microservices(self) -> List[MicroService]:
        """
        List all active microservices available in the marketplace.
        """
        return self.repository.list_active()

    def deactivate_microservice(self, microservice: MicroService) -> MicroService:
        """
        Deactivate a microservice (soft delete or hide from marketplace).
        """
        if not microservice:
            raise ValidationError(_("Microservice does not exist."))

        if not microservice.is_active:
            raise ValidationError(_("Microservice is already inactive."))

        return self.repository.deactivate(microservice)

    def get_microservice(self, microservice_id) -> Optional[MicroService]:
        """
        Retrieve a microservice by ID.
        Returns None if not found.
        """
        try:
            return self.repository.get_by_id(microservice_id)
        except MicroService.DoesNotExist:
            return None