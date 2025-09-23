# services/services/microservices_service.py
from typing import List, Optional
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
        return self.repository.create(freelancer=freelancer, **data)

    def update_microservice(
        self, microservice: MicroService, data: dict
    ) -> MicroService:
        return self.repository.update(microservice, **data)

    def list_freelancer_microservices(
        self, freelancer: FreelancerProfile
    ) -> List[MicroService]:
        return self.repository.list_by_freelancer(freelancer)

    def list_active_microservices(self) -> List[MicroService]:
        return self.repository.list_active()

    def deactivate_microservice(self, microservice: MicroService) -> MicroService:
        return self.repository.deactivate(microservice)

    def get_microservice(self, microservice_id) -> Optional[MicroService]:
        return self.repository.get_by_id(microservice_id)
