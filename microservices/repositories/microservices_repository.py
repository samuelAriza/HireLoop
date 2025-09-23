from typing import Optional, List
from ..models import MicroService
from core.models import FreelancerProfile
from core.repositories.base_repository import BaseRepository

class MicroServiceRepository(BaseRepository):
    """
    Repository for MicroService operations.
    Encapsulates all DB interactions for MicroService.
    """

    def create(self, freelancer: FreelancerProfile, **data) -> MicroService:
        data = data.copy()
        data.pop("image", None)
        return MicroService.objects.create(freelancer=freelancer, **data)

    def get_by_id(self, entity_id) -> Optional[MicroService]:
        try:
            return MicroService.objects.get(id=entity_id)
        except MicroService.DoesNotExist:
            return None

    def update(self, entity: MicroService, **kwargs) -> MicroService:
        kwargs = kwargs.copy()
        kwargs.pop("image", None)
        for field, value in kwargs.items():
            setattr(entity, field, value)
        entity.save()
        return entity

    def delete(self, entity: MicroService) -> bool:
        entity.delete()
        return True

    # Extra repository methods
    def list_by_freelancer(self, freelancer: FreelancerProfile) -> List[MicroService]:
        return MicroService.objects.filter(freelancer=freelancer).select_related(
            "freelancer", "freelancer__user", "category"
        )

    def deactivate(self, microservice: MicroService) -> MicroService:
        microservice.is_active = False
        microservice.save()
        return microservice

    def list_active(self) -> List[MicroService]:
        return MicroService.objects.filter(is_active=True).select_related(
            "freelancer", "freelancer__user", "category"
        )
