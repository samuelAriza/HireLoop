from typing import Optional
from .base import BaseValidator
from .email_validator import EmailValidator
from .username_validator import UsernameValidator

class ProfileDataValidator(BaseValidator):
    """Validador compuesto para datos de perfil - Composite Pattern"""
    
    def __init__(self):
        self.email_validator = EmailValidator()
        self.username_validator = UsernameValidator()
    
    def validate(self, data: dict) -> None:
        """Valida todos los datos de perfil"""
        self.email_validator.validate(data)
        self.username_validator.validate(data)
    
    def validate_user_data(self, data: dict, user_id: Optional[int] = None):
        """Método de conveniencia con user_id"""
        data_with_id = {**data, 'user_id': user_id}
        self.validate(data_with_id)