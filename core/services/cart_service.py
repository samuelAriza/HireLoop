"""
Unified Cart Service for HireLoop platform.

Handles cart operations for services and mentorships,
providing a unified interface for cart management.
"""

from typing import List, Dict, Any, Union
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .base import BaseService

User = get_user_model()


class UnifiedCartService(BaseService):
    """
    Unified service for managing cart items (services and mentorships).
    
    Handles adding, removing, and retrieving items from user's cart
    regardless of item type.
    """
    
    def __init__(self):
        """Initialize cart service."""
        super().__init__()
        self._errors = []
    
    def add_to_cart(self, user, item):
        """
        Add an item (service or mentorship) to cart.
        
        Args:
            user: User instance
            item: Service or MentorshipSession instance
            
        Returns:
            bool: True if added successfully
        """
        print(f"=== DEBUG: UnifiedCartService.add_to_cart ===")
        print(f"User: {user}")
        print(f"Item: {item}")
        print(f"Item type: {type(item)}")
        try:
            from services.models import Cart, CartItem
            from mentorship.models import MentorshipCartItem
            cart, _ = Cart.objects.get_or_create(user=user)
            if hasattr(item, 'freelancer'):  # Es un Servicio
                cart_item, created = CartItem.objects.get_or_create(cart=cart, service=item)
                return created
            elif hasattr(item, 'mentor'):  # Es una Mentoría
                cart_item, created = MentorshipCartItem.objects.get_or_create(cart=cart, mentorship=item)
                return created
            else:
                print("Unknown item type!")
                raise ValidationError("Unknown item type for cart")
        except Exception as e:
            print(f"Exception in add_to_cart: {str(e)}")
            import traceback
            traceback.print_exc()
            self._errors.append(f"Failed to add item to cart: {str(e)}")
            return False

    def remove_from_cart(self, user, item):
        """
        Remove an item from cart.
        
        Args:
            user: User instance
            item: Service or MentorshipSession instance
            
        Returns:
            bool: True if removed successfully
        """
        try:
            from services.models import Cart, CartItem
            from mentorship.models import MentorshipCartItem
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                return False
            if hasattr(item, 'freelancer'):  # Es un Servicio
                CartItem.objects.filter(cart=cart, service=item).delete()
            elif hasattr(item, 'mentor'):  # Es una Mentoría
                MentorshipCartItem.objects.filter(cart=cart, mentorship=item).delete()
            return True
        except Exception as e:
            self._errors.append(f"Failed to remove item from cart: {str(e)}")
            return False

    def is_in_cart(self, user, item):
        """
        Check if an item (service or mentorship) is in cart.
        
        Args:
            user: User instance
            item: Service or MentorshipSession instance
            
        Returns:
            bool: True if item is in cart
        """
        print(f"=== DEBUG: UnifiedCartService.is_in_cart ===")
        print(f"User: {user}")
        print(f"Item: {item}")
        print(f"Item type: {type(item)}")
        try:
            from services.models import Cart, CartItem
            from mentorship.models import MentorshipCartItem
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                return False
            if hasattr(item, 'freelancer'):
                return CartItem.objects.filter(cart=cart, service=item).exists()
            elif hasattr(item, 'mentor'):
                return MentorshipCartItem.objects.filter(cart=cart, mentorship=item).exists()
            else:
                return False
        except Exception as e:
            print(f"Exception in is_in_cart: {str(e)}")
            import traceback
            traceback.print_exc()
            self._errors.append(f"Failed to check if item is in cart: {str(e)}")
            return False

    def get_cart_items(self, user):
        """
        Get all cart items for a user (services and mentorships).
        
        Returns:
            dict: {'services': [...], 'mentorships': [...]}
        """
        print(f"=== DEBUG: UnifiedCartService.get_cart_items for user {user} ===")
        try:
            from services.models import Cart, CartItem
            from mentorship.models import MentorshipCartItem
            try:
                cart = Cart.objects.get(user=user)
                service_items = CartItem.objects.filter(cart=cart).select_related('service')
                services = [item.service for item in service_items]
                mentorship_items = MentorshipCartItem.objects.filter(cart=cart).select_related('mentorship')
                mentorships = [item.mentorship for item in mentorship_items]
            except Cart.DoesNotExist:
                services = []
                mentorships = []
            return {
                'services': services,
                'mentorships': mentorships
            }
        except Exception as e:
            print(f"Exception in get_cart_items: {str(e)}")
            import traceback
            traceback.print_exc()
            self._errors.append(f"Failed to get cart items: {str(e)}")
            return {'services': [], 'mentorships': []}
    
    def get_cart_total(self, user):
        """
        Calculate total price of all items in cart.
        
        Args:
            user: User instance
            
        Returns:
            float: Total price
        """
        try:
            cart_items = self.get_cart_items(user)
            total = 0
            
            # Add services total
            for service in cart_items['services']:
                total += float(service.price)
            
            # Add mentorships total  
            for mentorship in cart_items['mentorships']:
                total += float(mentorship.price * mentorship.duration_hours)
            
            return total
            
        except Exception as e:
            return 0
    
    def get_cart_count(self, user):
        """
        Get total number of items in cart.
        
        Args:
            user: User instance
            
        Returns:
            int: Number of items
        """
        try:
            cart_items = self.get_cart_items(user)
            return len(cart_items['services']) + len(cart_items['mentorships'])
            
        except Exception as e:
            return 0
    
    def clear_cart(self, user):
        """
        Remove all items from user's cart.
        
        Args:
            user: User instance
            
        Returns:
            bool: True if cleared successfully
        """
        try:
            from services.models import Cart, CartItem
            from mentorship.models import MentorshipCartItem
            cart = Cart.objects.filter(user=user).first()
            if cart:
                CartItem.objects.filter(cart=cart).delete()
                MentorshipCartItem.objects.filter(cart=cart).delete()
            return True
        except Exception as e:
            self._errors.append(f"Failed to clear cart: {str(e)}")
            return False
    
    @property
    def errors(self):
        """Get service errors."""
        return self._errors.copy()


# Legacy alias for backward compatibility
CartService = UnifiedCartService
