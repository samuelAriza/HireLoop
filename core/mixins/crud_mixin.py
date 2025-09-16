from django.core.exceptions import PermissionDenied

class CRUDMixin:
    """Mixin para operaciones CRUD básicas - DRY"""
    
    def _validate_ownership(self, resource, user, error_message: str):
        """Validación de propiedad reutilizable"""
        if not self._is_owner(resource, user):
            raise PermissionDenied(error_message)
    
    def _is_owner(self, resource, user) -> bool:
        """Determina si el usuario es propietario del recurso"""
        if hasattr(resource, 'user'):
            return resource.user == user
        elif hasattr(resource, 'freelancer'):
            return resource.freelancer.user == user
        elif hasattr(resource, 'client'):
            return resource.client.user == user
        return False