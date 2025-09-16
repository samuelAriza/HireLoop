"""
Context processors para datos globales del template.
Sigue principios SOLID: Responsabilidad única de proveer contexto global.
Aplica DRY: Evita repetir lógica de carrito/wishlist en cada vista.
"""
from core.services import UnifiedCartService, UnifiedWishlistService


def global_context(request):
    """
    Context processor unificado para todos los datos globales.
    Sigue DRY: Centraliza todos los contextos en una función.
    """
    context = {}
    
    if request.user.is_authenticated:
        try:
            # Datos del carrito (servicios + mentorías)
            context['cart_count'] = UnifiedCartService.get_cart_count(request.user)
            context['cart_total'] = UnifiedCartService.get_cart_total(request.user)
            
            # Datos de wishlist (servicios + mentorías)
            context['wishlist_count'] = UnifiedWishlistService.get_wishlist_count(request.user)
            
        except Exception as e:
            # Valores por defecto en caso de error (KISS)
            context.update({
                'cart_count': 0,
                'cart_total': 0,
                'wishlist_count': 0,
            })
    else:
        # Valores para usuarios no autenticados
        context.update({
            'cart_count': 0,
            'cart_total': 0,
            'wishlist_count': 0,
        })
    
    return context