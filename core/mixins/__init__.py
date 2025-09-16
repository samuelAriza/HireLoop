"""
Mixins package for HireLoop platform.

Provides reusable view mixins for authentication, permissions, and access control.
All mixins follow SOLID principles and can be easily combined.
"""

# Import mixins from their respective modules
from .access_control import (
    FreelancerRequiredMixin,
    FreelancerOrOwnerRequiredMixin
)
from .crud_mixin import CRUDMixin

# Make mixins available at package level
__all__ = [
    'FreelancerRequiredMixin',
    'FreelancerOrOwnerRequiredMixin',
    'CRUDMixin',
]