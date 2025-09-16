from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse

from .models import MentorshipSession
from core.services import UnifiedCartService, UnifiedWishlistService


class AddMentorshipToCartView(LoginRequiredMixin, View):
    """
    Vista para agregar mentorías al carrito.
    Aplica SRP: Solo maneja adición de mentorías al carrito.
    """
    
    def post(self, request, mentorship_id):
        try:
            mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
            
            # Usar el servicio unificado para agregar al carrito
            UnifiedCartService.add_to_cart(request.user, mentorship)
            
            messages.success(
                request, 
                f"'{mentorship.title}' agregado al carrito exitosamente"
            )
            
            # Si es una petición AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                cart_count = UnifiedCartService.get_cart_count(request.user)
                return JsonResponse({
                    'success': True,
                    'message': f"'{mentorship.title}' agregado al carrito",
                    'cart_count': cart_count
                })
            
        except Exception as e:
            messages.error(request, f"Error al agregar al carrito: {str(e)}")
            
            # Si es AJAX, devolver error en JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                })
        
        # Redirigir al detalle de la mentoría
        return redirect('mentorship:mentorship_detail', pk=mentorship_id)
    
    def get(self, request, mentorship_id):
        """Redirect GET requests to mentorship detail"""
        return redirect('mentorship:mentorship_detail', pk=mentorship_id)


class RemoveMentorshipFromCartView(LoginRequiredMixin, View):
    """
    Vista para remover mentorías del carrito.
    Aplica SRP: Solo maneja remoción de mentorías del carrito.
    """
    
    def post(self, request, mentorship_id):
        try:
            mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
            
            # Usar el servicio unificado para remover del carrito
            UnifiedCartService.remove_from_cart(request.user, mentorship)
            
            messages.success(
                request, 
                f"'{mentorship.title}' removido del carrito"
            )
            
            # Si es AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                cart_count = UnifiedCartService.get_cart_count(request.user)
                cart_total = UnifiedCartService.get_cart_total(request.user)
                return JsonResponse({
                    'success': True,
                    'message': f"'{mentorship.title}' removido del carrito",
                    'cart_count': cart_count,
                    'cart_total': str(cart_total)
                })
            
        except Exception as e:
            messages.error(request, f"Error al remover del carrito: {str(e)}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                })
        
        # Redirigir al carrito
        return redirect('services:cart_view')


class AddMentorshipToWishlistView(LoginRequiredMixin, View):
    """
    Vista para agregar mentorías a la wishlist.
    Aplica SRP: Solo maneja adición de mentorías a favoritos.
    """
    
    def post(self, request, mentorship_id):
        try:
            mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
            
            # Verificar si ya está en wishlist
            if UnifiedWishlistService.is_in_wishlist(request.user, mentorship):
                messages.info(
                    request, 
                    f"'{mentorship.title}' ya está en tus favoritos"
                )
            else:
                # Usar el servicio unificado para agregar a wishlist
                UnifiedWishlistService.add_to_wishlist(request.user, mentorship)
                
                messages.success(
                    request, 
                    f"'{mentorship.title}' agregado a favoritos exitosamente"
                )
            
            # Si es AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                wishlist_count = UnifiedWishlistService.get_wishlist_count(request.user)
                is_in_wishlist = UnifiedWishlistService.is_in_wishlist(request.user, mentorship)
                return JsonResponse({
                    'success': True,
                    'message': f"'{mentorship.title}' en favoritos",
                    'wishlist_count': wishlist_count,
                    'in_wishlist': is_in_wishlist
                })
            
        except Exception as e:
            messages.error(request, f"Error al agregar a favoritos: {str(e)}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                })
        
        return redirect('mentorship:mentorship_detail', pk=mentorship_id)

    def get(self, request, mentorship_id):
        """Redirect GET requests to mentorship detail"""
        return redirect('mentorship:mentorship_detail', pk=mentorship_id)


class RemoveMentorshipFromWishlistView(LoginRequiredMixin, View):
    """
    Vista para remover mentorías de la wishlist.
    Aplica SRP: Solo maneja remoción de mentorías de favoritos.
    """
    
    def post(self, request, mentorship_id):
        try:
            mentorship = get_object_or_404(MentorshipSession, id=mentorship_id)
            
            # Usar el servicio unificado para remover de wishlist
            UnifiedWishlistService.remove_from_wishlist(request.user, mentorship)
            
            messages.success(
                request, 
                f"'{mentorship.title}' removido de favoritos"
            )
            
            # Si es AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                wishlist_count = UnifiedWishlistService.get_wishlist_count(request.user)
                return JsonResponse({
                    'success': True,
                    'message': f"'{mentorship.title}' removido de favoritos",
                    'wishlist_count': wishlist_count
                })
            
        except Exception as e:
            messages.error(request, f"Error al remover de favoritos: {str(e)}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                })
        
        # Redirigir a la wishlist
        return redirect('services:wishlist_view')