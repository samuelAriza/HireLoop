from django.core.exceptions import PermissionDenied, ValidationError
from .base import BaseService
from ..mixins.crud_mixin import CRUDMixin

class ServiceManagementService(BaseService, CRUDMixin):
    """Servicio para gestión de servicios de freelancer - SRP"""
    
    def create_service(self, user, service_data: dict):
        """Crea un nuevo servicio"""
        self._validate_freelancer_permission(user, "crear servicios")
        
        def create_operation():
            from services.models import Service
            
            service = Service.objects.create(
                freelancer=user.freelancerprofile,
                title=service_data.get('title'),
                description=service_data.get('description'),
                price=service_data.get('price'),
                delivery_time=service_data.get('delivery_time', 7),
                category=service_data.get('category', 'OTHER'),
                active=service_data.get('is_active', True)
            )
            
            self.logger.info(f"Service created: {service.title} by {user.username}")
            return service
        
        return self.execute_with_transaction(create_operation)
    
    def update_service(self, service, user, service_data: dict):
        """Actualiza un servicio existente"""
        self._validate_ownership(service, user, "No tienes permiso para editar este servicio")
        
        def update_operation():
            allowed_fields = ['title', 'description', 'price', 'delivery_time', 'category']
            
            for field in allowed_fields:
                if field in service_data:
                    setattr(service, field, service_data[field])
            
            if 'is_active' in service_data:
                service.active = service_data['is_active']
            
            service.save()
            self.logger.info(f"Service updated: {service.title} by {user.username}")
            return service
        
        return self.execute_with_transaction(update_operation)
    
    def delete_service(self, service, user) -> bool:
        """Elimina un servicio"""
        self._validate_ownership(service, user, "No tienes permiso para eliminar este servicio")
        
        def delete_operation():
            service_title = service.title
            service.delete()
            self.logger.info(f"Service deleted: {service_title} by {user.username}")
            return True
        
        return self.execute_with_transaction(delete_operation)
    
    def get_freelancer_services(self, user):
        """Obtiene servicios del freelancer"""
        if not self._has_freelancer_profile(user):
            return []
        
        try:
            from services.models import Service
            return Service.objects.filter(
                freelancer=user.freelancerprofile
            ).order_by('-created_at')
        except Exception as e:
            self.logger.error(f"Error getting services for user {user.username}: {str(e)}")
            return []
    
    def get_active_services(self, limit: int = 20):
        """Obtiene servicios activos públicos"""
        try:
            from services.models import Service
            return Service.objects.filter(
                active=True
            ).select_related('freelancer__user').order_by('-created_at')[:limit]
        except Exception as e:
            self.logger.error(f"Error getting active services: {str(e)}")
            return []
    
    def _validate_freelancer_permission(self, user, action: str):
        """Valida permisos de freelancer"""
        if not self._has_freelancer_profile(user):
            raise PermissionDenied(f"Solo los freelancers pueden {action}")
    
    def _has_freelancer_profile(self, user) -> bool:
        """Verifica si el usuario tiene perfil de freelancer"""
        return hasattr(user, 'freelancerprofile') and user.freelancerprofile is not None