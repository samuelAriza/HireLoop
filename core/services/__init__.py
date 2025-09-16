"""
Core Services Module

This module provides centralized business logic services for the HireLoop platform.
All services follow SOLID principles and Clean Architecture patterns.
"""

# Import all services for easy access
from .mentorship_service import MentorshipService
from .cart_service import UnifiedCartService
from .wishlist_service import UnifiedWishlistService

from .service_management import ServiceManagementService
from .profile_service import FreelancerProfileService, ClientProfileService
from .project_service import ProjectManagementService


# Legacy aliases for backward compatibility
from .cart_service import CartService
from .wishlist_service import WishlistService

__all__ = [
    'MentorshipService',
    'UnifiedCartService', 
    'UnifiedWishlistService',
    'CartService',  # Legacy alias
    'WishlistService',  # Legacy alias
    'FreelancerProfileService',
    'ClientProfileService',
    'ServiceManagementService',
    'ProjectManagementService',
]