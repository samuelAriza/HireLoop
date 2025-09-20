from ..repositories.cart_repository import CartRepository
from ..repositories.wishlist_repository import WishlistRepository

class CartService:
    def __init__(self, cart_repository: CartRepository = None):
        self.cart_repo = cart_repository or CartRepository()

    def add_to_cart(self, user, obj, quantity=1):
        item = self.cart_repo.get_or_create(user, obj, defaults={"quantity": 0})
        item.quantity += quantity
        self.cart_repo.update(item, quantity=item.quantity)
        
        return item

    def remove_from_cart(self, user, obj):
        item = self.cart_repo.get_or_create(user, obj)
        return self.cart_repo.delete(item)

    def list_cart(self, user):
        return self.cart_repo.list_by_user(user)


class WishlistService:
    def __init__(self, wishlist_repository: WishlistRepository = None):
        self.wishlist_repo = wishlist_repository or WishlistRepository()

    def add_to_wishlist(self, user, obj):
        return self.wishlist_repo.get_or_create(user, obj)

    def remove_from_wishlist(self, user, obj):
        item = self.wishlist_repo.get_or_create(user, obj)
        return self.wishlist_repo.delete(item)

    def list_wishlist(self, user):
        return self.wishlist_repo.list_by_user(user)