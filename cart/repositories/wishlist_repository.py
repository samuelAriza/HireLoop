# cart/repositories/wishlist_repository.py
from typing import Optional, List
from django.contrib.contenttypes.models import ContentType
from core.repositories.base_repository import BaseRepository
from cart.models import WishlistItem

class WishlistRepository(BaseRepository):
    """
    Repository for WishlistItem entities.
    """

    def create(self, **kwargs) -> WishlistItem:
        return WishlistItem.objects.create(**kwargs)

    def get_by_id(self, entity_id) -> Optional[WishlistItem]:
        return WishlistItem.objects.filter(id=entity_id).first()

    def update(self, entity: WishlistItem, **kwargs) -> WishlistItem:
        for key, value in kwargs.items():
            setattr(entity, key, value)
        entity.save()
        return entity

    def delete(self, entity: WishlistItem) -> bool:
        deleted, _ = WishlistItem.objects.filter(id=entity.id).delete()
        return bool(deleted)

    def get_or_create(self, user, obj) -> WishlistItem:
        content_type = ContentType.objects.get_for_model(obj)
        item, _ = WishlistItem.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=obj.id
        )
        return item

    def list_by_user(self, user) -> List[WishlistItem]:
        return list(WishlistItem.objects.filter(user=user))
