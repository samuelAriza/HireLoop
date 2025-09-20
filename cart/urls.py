from django.urls import path
from .views.views import (
    CartListView,
    AddToCartView,
    RemoveFromCartView,
    WishlistListView,
    AddToWishlistView,
    RemoveFromWishlistView,
)

app_name = "cart"

urlpatterns = [
    path("", CartListView.as_view(), name="cart_list"),
    path("add/", AddToCartView.as_view(), name="add_to_cart"),
    path("remove/<uuid:pk>/", RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("wishlist/", WishlistListView.as_view(), name="wishlist_list"),
    path("wishlist/add/", AddToWishlistView.as_view(), name="add_to_wishlist"),
    path("wishlist/remove/<uuid:pk>/", RemoveFromWishlistView.as_view(), name="remove_from_wishlist"),
]