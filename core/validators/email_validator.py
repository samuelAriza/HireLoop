from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from typing import Optional
from .base import BaseValidator

class EmailValidator(BaseValidator):
    """Validador específico para emails - SRP"""
    
    def validate(self, data: dict) -> None:
        if 'email' in data:
            self.validate_unique_email(data['email'], data.get('user_id'))
    
    @staticmethod
    def validate_unique_email(email: str, user_id: Optional[int] = None):
        """Valida que el email sea único"""
        User = get_user_model()
        query = User.objects.filter(email=email)
        if user_id:
            query = query.exclude(id=user_id)
        
        if query.exists():
            raise ValidationError("El email ya está en uso")