"""
Models package for HireLoop platform.

Contains all Django models organized by domain.
"""

# Import models to make them available at package level
from .user import User
from .profiles import FreelancerProfile, ClientProfile

# Make models available for imports
__all__ = [
    'User',
    'FreelancerProfile', 
    'ClientProfile',
]