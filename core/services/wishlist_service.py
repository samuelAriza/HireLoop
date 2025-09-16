"""
Unified Wishlist Service for HireLoop platform.

Handles wishlist operations for both services and mentorships,
providing a unified interface for wishlist management.
"""

from typing import List, Dict, Any, Union
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .base import BaseService

User = get_user_model()


class UnifiedWishlistService(BaseService):
    """
    Unified service for managing wishlist items (services and mentorships).
    
    Handles adding, removing, and retrieving items from user's wishlist
    regardless of item type.
    """
    
    def __init__(self):
        """Initialize wishlist service."""
        super().__init__()
        self._errors = []
    
    def add_to_wishlist(self, user, item):
        """
        Add an item (service or mentorship) to wishlist.
        
        Args:
            user: User instance
            item: Service or MentorshipSession instance
            
        Returns:
            bool: True if added successfully
        """
        try:
            # Determine item type and create appropriate wishlist item
            if hasattr(item, 'freelancer'):  # It's a Service
                from services.models import WishlistItem, Wishlist
                # Obtener o crear la wishlist del usuario
                wishlist, _ = Wishlist.objects.get_or_create(user=user)
                # Crear el item en la wishlist
                wishlist_item, created = WishlistItem.objects.get_or_create(
                    wishlist=wishlist,
                    service=item
                )
                return created
                
            elif hasattr(item, 'mentor'):  # It's a MentorshipSession
                from mentorship.models import MentorshipWishlistItem
                wishlist_item, created = MentorshipWishlistItem.objects.get_or_create(
                    user=user,
                    session=item
                )
                return created
                
            else:
                raise ValidationError("Unknown item type for wishlist")
                
        except Exception as e:
            self._errors.append(f"Failed to add item to wishlist: {str(e)}")
            return False
    
    def remove_from_wishlist(self, user, item):
        """
        Remove an item from wishlist.
        
        Args:
            user: User instance
            item: Service or MentorshipSession instance
            
        Returns:
            bool: True if removed successfully
        """
        try:
            if hasattr(item, 'freelancer'):  # It's a Service
                from services.models import WishlistItem, Wishlist
                try:
                    wishlist = Wishlist.objects.get(user=user)
                    WishlistItem.objects.filter(wishlist=wishlist, service=item).delete()
                except Wishlist.DoesNotExist:
                    pass
                
            elif hasattr(item, 'mentor'):  # It's a MentorshipSession
                from mentorship.models import MentorshipWishlistItem
                MentorshipWishlistItem.objects.filter(user=user, session=item).delete()
                
            return True
            
        except Exception as e:
            self._errors.append(f"Failed to remove item from wishlist: {str(e)}")
            return False
    
    def is_in_wishlist(self, user, item):
        """
        Check if an item is in user's wishlist.
        
        Args:
            user: User instance
            item: Service or MentorshipSession instance
            
        Returns:
            bool: True if item is in wishlist
        """
        try:
            if hasattr(item, 'freelancer'):  # It's a Service
                from services.models import WishlistItem, Wishlist
                try:
                    wishlist = Wishlist.objects.get(user=user)
                    return WishlistItem.objects.filter(wishlist=wishlist, service=item).exists()
                except Wishlist.DoesNotExist:
                    return False
                
            elif hasattr(item, 'mentor'):  # It's a MentorshipSession
                from mentorship.models import MentorshipWishlistItem
                return MentorshipWishlistItem.objects.filter(user=user, session=item).exists()
                
            return False
            
        except Exception as e:
            return False
    
    def get_wishlist_items(self, user):
        """
        Get all wishlist items for a user.
        
        Args:
            user: User instance
            
        Returns:
            dict: Dictionary with 'services' and 'mentorships' lists
        """
        try:
            services = []
            mentorships = []
            
            # Get services from wishlist
            try:
                from services.models import WishlistItem, Wishlist
                try:
                    wishlist = Wishlist.objects.get(user=user)
                    service_items = WishlistItem.objects.filter(wishlist=wishlist).select_related('service')
                    services = [item.service for item in service_items if item.service]
                except Wishlist.DoesNotExist:
                    services = []
            except ImportError:
                pass
            
            # Get mentorships from wishlist
            try:
                from mentorship.models import MentorshipWishlistItem
                mentorship_items = MentorshipWishlistItem.objects.filter(user=user).select_related('session')
                mentorships = [item.session for item in mentorship_items]
            except ImportError:
                pass
            
            return {
                'services': services,
                'mentorships': mentorships
            }
            
        except Exception as e:
            return {'services': [], 'mentorships': []}
    
    def get_wishlist_count(self, user):
        """
        Get total number of items in wishlist.
        
        Args:
            user: User instance
            
        Returns:
            int: Number of items
        """
        try:
            wishlist_items = self.get_wishlist_items(user)
            return len(wishlist_items['services']) + len(wishlist_items['mentorships'])
            
        except Exception as e:
            return 0
    
    def clear_wishlist(self, user):
        """
        Remove all items from user's wishlist.
        
        Args:
            user: User instance
            
        Returns:
            bool: True if cleared successfully
        """
        try:
            # Clear services
            try:
                from services.models import WishlistItem
                WishlistItem.objects.filter(user=user).delete()
            except ImportError:
                pass
            
            # Clear mentorships
            try:
                from mentorship.models import MentorshipWishlistItem
                MentorshipWishlistItem.objects.filter(user=user).delete()
            except ImportError:
                pass
            
            return True
            
        except Exception as e:
            self._errors.append(f"Failed to clear wishlist: {str(e)}")
            return False
    
    @property
    def errors(self):
        """Get service errors."""
        return self._errors.copy()


# Legacy alias for backward compatibility
WishlistService = UnifiedWishlistService