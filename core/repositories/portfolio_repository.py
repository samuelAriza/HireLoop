from typing import Optional, List
from ..repositories.base_repository import BaseRepository
from ..models import ItemPortfolio, FreelancerProfile


class PortfolioRepository(BaseRepository):
    """
    Repository for ItemPortfolio operations.
    Encapsulates data access for portfolio items.
    """

    def create(self, freelancer: FreelancerProfile, **kwargs) -> ItemPortfolio:
        return ItemPortfolio.objects.create(freelancer=freelancer, **kwargs)

    def get_by_id(self, entity_id) -> Optional[ItemPortfolio]:
        try:
            return ItemPortfolio.objects.get(id=entity_id)
        except ItemPortfolio.DoesNotExist:
            return None

    def update(self, entity: ItemPortfolio, **kwargs) -> ItemPortfolio:
        for field, value in kwargs.items():
            setattr(entity, field, value)
        entity.save()
        return entity

    def delete(self, entity: ItemPortfolio) -> bool:
        deleted, _ = entity.delete()
        return deleted > 0

    def list_by_freelancer(self, freelancer: FreelancerProfile) -> List[ItemPortfolio]:
        return freelancer.portfolio_items.all()
