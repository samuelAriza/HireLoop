from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from typing import Optional
from .base import BaseValidator

class UsernameValidator(BaseValidator):
    """Validador específico para usernames - SRP"""
    
    def validate(self, data: dict) -> None:
        if 'username' in data:
            self.validate_unique_username(data['username'], data.get('user_id'))
    
    @staticmethod
    def validate_unique_username(username: str, user_id: Optional[int] = None):
        """Valida que el username sea único"""
        User = get_user_model()
        query = User.objects.filter(username=username)
        if user_id:
            query = query.exclude(id=user_id)
        
        if query.exists():
            raise ValidationError("El nombre de usuario ya existe")