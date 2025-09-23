from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from ..models import CartItem, WishlistItem
from ..services.cart_service import CartService, WishlistService


class CartListView(ListView):
    model = CartItem
    template_name = "cart/cart_list.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        service = CartService()
        return service.list_cart(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context["cart_items"]
        context["items_quantity_total"] = sum(item.quantity for item in cart_items)
        context["cart_total"] = sum(
            item.content_object.get_price() * item.quantity for item in cart_items
        )
        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        service = CartService()
        content_type_id = request.POST.get("content_type")
        object_id = request.POST.get("object_id")
        quantity = int(request.POST.get("quantity", 1))

        content_type = get_object_or_404(ContentType, id=content_type_id)
        model_class = content_type.model_class()
        obj = get_object_or_404(model_class, id=object_id)

        service.add_to_cart(user=request.user, obj=obj, quantity=quantity)
        return redirect("cart:cart_list")


class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        service = CartService()
        item = get_object_or_404(CartItem, id=kwargs["pk"], user=request.user)
        service.remove_from_cart(user=request.user, obj=item.content_object)
        return redirect("cart:cart_list")


class WishlistListView(ListView):
    model = WishlistItem
    template_name = "cart/wishlist_list.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        service = WishlistService()
        return service.list_wishlist(self.request.user)


class AddToWishlistView(View):
    def post(self, request, *args, **kwargs):
        service = WishlistService()
        content_type_id = request.POST.get("content_type")
        object_id = request.POST.get("object_id")

        content_type = get_object_or_404(ContentType, id=content_type_id)
        model_class = content_type.model_class()
        obj = get_object_or_404(model_class, id=object_id)

        service.add_to_wishlist(user=request.user, obj=obj)
        return redirect("cart:wishlist_list")


class RemoveFromWishlistView(View):
    def post(self, request, *args, **kwargs):
        service = WishlistService()
        item = get_object_or_404(WishlistItem, id=kwargs["pk"], user=request.user)
        service.remove_from_wishlist(user=request.user, obj=item.content_object)
        return redirect("cart:wishlist_list")
