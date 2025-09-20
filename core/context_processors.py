from cart.models import CartItem, WishlistItem 
from django.db.models import Sum

def user_profile_type(request):
    user_types = []
    if request.user.is_authenticated:
        if hasattr(request.user, 'freelancer_profile'):
            user_types.append('freelancer')
        if hasattr(request.user, 'client_profile'):
            user_types.append('client')
    return {'user_type': user_types}

def cart_and_wishlist_counts(request):
    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        wishlist_count = WishlistItem.objects.filter(user=request.user).count()

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    }