# cart/repositories/cart_repository.py
from typing import Optional, List
from django.contrib.contenttypes.models import ContentType
from core.repositories.base_repository import BaseRepository
from cart.models import CartItem

class CartRepository(BaseRepository):
    """
    Repository for CartItem entities.
    """

    def create(self, **kwargs) -> CartItem:
        return CartItem.objects.create(**kwargs)

    def get_by_id(self, entity_id) -> Optional[CartItem]:
        return CartItem.objects.filter(id=entity_id).first()

    def update(self, entity: CartItem, **kwargs) -> CartItem:
        for key, value in kwargs.items():
            setattr(entity, key, value)
        entity.save()
        return entity

    def delete(self, entity: CartItem) -> bool:
        deleted, _ = CartItem.objects.filter(id=entity.id).delete()
        return bool(deleted)

    def get_or_create(self, user, obj, defaults=None) -> CartItem:
        content_type = ContentType.objects.get_for_model(obj)
        item, _ = CartItem.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=obj.id,
            defaults=defaults or {}
        )
        return item

    def list_by_user(self, user) -> List[CartItem]:
        return list(CartItem.objects.filter(user=user))
