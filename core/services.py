from typing import Optional, Union, List, Protocol, Dict, Any
from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ABSTRACTIONS & PROTOCOLS (DIP)
# ============================================================================

class ProfileRepositoryProtocol(Protocol):
    """Protocol para repositorios de perfiles - DIP"""
    def get_by_user(self, user) -> Optional[Any]: ...
    def create(self, user, data: dict) -> Any: ...
    def update(self, profile, data: dict) -> Any: ...
    def delete(self, profile) -> bool: ...


class ValidatorProtocol(Protocol):
    """Protocol para validadores - DIP & ISP"""
    def validate(self, data: dict) -> None: ...


class NotificationServiceProtocol(Protocol):
    """Protocol para notificaciones - DIP"""
    def notify(self, event_type: str, data: dict) -> None: ...


# ============================================================================
# BASE CLASSES & MIXINS (LSP)
# ============================================================================

class BaseService(ABC):
    """Clase base para todos los servicios - Template Method Pattern"""
    
    def __init__(self, logger_name: Optional[str] = None):
        self.logger = logging.getLogger(logger_name or self.__class__.__name__)
    
    def execute_with_transaction(self, operation, *args, **kwargs):
        """Template method para operaciones transaccionales"""
        try:
            with transaction.atomic():
                return operation(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error in {operation.__name__}: {str(e)}")
            raise


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


# ============================================================================
# VALIDATORS (SRP & ISP)
# ============================================================================

class EmailValidator:
    """Validador específico para emails - SRP"""
    
    @staticmethod
    def validate_unique_email(email: str, user_id: Optional[int] = None):
        """Valida que el email sea único"""
        User = get_user_model()
        query = User.objects.filter(email=email)
        if user_id:
            query = query.exclude(id=user_id)
        
        if query.exists():
            raise ValidationError("El email ya está en uso")


class UsernameValidator:
    """Validador específico para usernames - SRP"""
    
    @staticmethod
    def validate_unique_username(username: str, user_id: Optional[int] = None):
        """Valida que el username sea único"""
        User = get_user_model()
        query = User.objects.filter(username=username)
        if user_id:
            query = query.exclude(id=user_id)
        
        if query.exists():
            raise ValidationError("El nombre de usuario ya existe")


class ProfileDataValidator:
    """Validador compuesto para datos de perfil - Composite Pattern"""
    
    def __init__(self):
        self.email_validator = EmailValidator()
        self.username_validator = UsernameValidator()
    
    def validate_user_data(self, data: dict, user_id: Optional[int] = None):
        """Valida datos de usuario"""
        if 'email' in data:
            self.email_validator.validate_unique_email(data['email'], user_id)
        
        if 'username' in data:
            self.username_validator.validate_unique_username(data['username'], user_id)


# ============================================================================
# REPOSITORIES (SRP & DIP)
# ============================================================================

class FreelancerProfileRepository:
    """Repositorio específico para FreelancerProfile - SRP"""
    
    def get_by_user(self, user):
        try:
            return user.freelancerprofile
        except AttributeError:
            return None
    
    def create(self, user, data: dict = None):
        from .models import FreelancerProfile
        return FreelancerProfile.objects.create(
            user=user,
            skills=data.get('skills', []) if data else [],
            bio=data.get('bio', '') if data else ''
        )
    
    def update(self, profile, data: dict):
        if 'skills' in data:
            skills = data['skills']
            if isinstance(skills, list):
                profile.skills = skills
            elif isinstance(skills, str):
                profile.skills = [s.strip() for s in skills.split(',') if s.strip()]
        
        if 'bio' in data:
            profile.bio = data['bio']
        
        profile.save()
        return profile
    
    def delete(self, profile) -> bool:
        profile.delete()
        return True


class ClientProfileRepository:
    """Repositorio específico para ClientProfile - SRP"""
    
    def get_by_user(self, user):
        try:
            return user.clientprofile
        except AttributeError:
            return None
    
    def create(self, user, data: dict = None):
        from .models import ClientProfile
        return ClientProfile.objects.create(
            user=user,
            company=data.get('company', '') if data else '',
            billing_email=data.get('billing_email', '') if data else ''
        )
    
    def update(self, profile, data: dict):
        if 'company' in data:
            profile.company = data['company']
        
        if 'billing_email' in data:
            # Validación específica para billing_email
            billing_email = data['billing_email']
            if billing_email:
                EmailValidator.validate_unique_email(billing_email, profile.user.id)
            profile.billing_email = billing_email
        
        profile.save()
        return profile
    
    def delete(self, profile) -> bool:
        profile.delete()
        return True


# ============================================================================
# FACTORIES (OCP & DIP)
# ============================================================================

class ProfileRepositoryFactory:
    """Factory para repositorios de perfiles - OCP"""
    
    _repositories = {
        'freelancer': FreelancerProfileRepository,
        'client': ClientProfileRepository,
    }
    
    @classmethod
    def get_repository(cls, profile_type: str) -> ProfileRepositoryProtocol:
        """Factory method mejorado - OCP"""
        repository_class = cls._repositories.get(profile_type.lower())
        if not repository_class:
            raise ValueError(f"Tipo de perfil no soportado: {profile_type}")
        return repository_class()
    
    @classmethod
    def register_repository(cls, profile_type: str, repository_class):
        """Permite registrar nuevos repositorios sin modificar el código - OCP"""
        cls._repositories[profile_type.lower()] = repository_class


class ServiceFactory:
    """Factory para diferentes tipos de servicios de negocio - OCP"""
    
    _services = {}
    
    @classmethod
    def get_service(cls, service_type: str):
        """Factory method extensible"""
        service_class = cls._services.get(service_type)
        if not service_class:
            raise ValueError(f"Servicio no registrado: {service_type}")
        return service_class()
    
    @classmethod
    def register_service(cls, service_type: str, service_class):
        """Registro dinámico de servicios - OCP"""
        cls._services[service_type] = service_class


# ============================================================================
# DOMAIN SERVICES (SRP)
# ============================================================================

class UserProfileService(BaseService, CRUDMixin):
    """Servicio para gestión unificada de perfiles de usuario - SRP"""
    
    def __init__(self, validator: Optional[ProfileDataValidator] = None):
        super().__init__()
        self.validator = validator or ProfileDataValidator()
    
    def create_profile(self, user, profile_type: str, data: dict = None) -> Optional[Any]:
        """Crea un perfil del tipo especificado"""
        if not user or not profile_type:
            raise ValidationError("Usuario y tipo de perfil son requeridos")
        
        repository = ProfileRepositoryFactory.get_repository(profile_type)
        
        # Verificar si ya existe
        existing_profile = repository.get_by_user(user)
        if existing_profile:
            self.logger.info(f"{profile_type.title()}Profile already exists for user {user.username}")
            return None
        
        def create_operation():
            profile = repository.create(user, data)
            self.logger.info(f"{profile_type.title()}Profile created for user {user.username}")
            return profile
        
        return self.execute_with_transaction(create_operation)
    
    def update_profile(self, user, profile_type: str, data: dict):
        """Actualiza un perfil existente"""
        repository = ProfileRepositoryFactory.get_repository(profile_type)
        profile = repository.get_by_user(user)
        
        if not profile:
            raise ValidationError(f"El usuario no tiene perfil de {profile_type}")
        
        def update_operation():
            # Validar datos de usuario
            self.validator.validate_user_data(data, user.id)
            
            # Actualizar datos del usuario
            self._update_user_data(user, data)
            
            # Actualizar datos específicos del perfil
            updated_profile = repository.update(profile, data)
            
            self.logger.info(f"{profile_type.title()}Profile updated for user {user.username}")
            return updated_profile
        
        return self.execute_with_transaction(update_operation)
    
    def get_profile(self, user, profile_type: str):
        """Obtiene un perfil específico"""
        repository = ProfileRepositoryFactory.get_repository(profile_type)
        return repository.get_by_user(user)
    
    def get_all_profiles(self, user) -> Dict[str, Any]:
        """Obtiene todos los perfiles del usuario"""
        profiles = {}
        
        for profile_type in ['freelancer', 'client']:
            try:
                profile = self.get_profile(user, profile_type)
                if profile:
                    profiles[profile_type] = profile
            except Exception as e:
                self.logger.error(f"Error getting {profile_type} profile: {str(e)}")
        
        return profiles
    
    def _update_user_data(self, user, data: dict):
        """Actualiza datos básicos del usuario"""
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        
        if 'username' in data or 'email' in data:
            user.save()


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


class ProjectManagementService(BaseService, CRUDMixin):
    """Servicio para gestión de proyectos - SRP"""
    
    def create_project(self, user, project_data: dict):
        """Crea un nuevo proyecto"""
        self._validate_client_permission(user, "crear proyectos")
        
        def create_operation():
            from projects.models import Project
            
            project = Project.objects.create(
                client=user.clientprofile,
                title=project_data.get('title'),
                description=project_data.get('description'),
                budget=project_data.get('budget'),
                deadline=project_data.get('deadline'),
                state='OPEN'
            )
            return project
        
        return self.execute_with_transaction(create_operation)
    
    def update_project(self, project, user, project_data: dict):
        """Actualiza un proyecto"""
        self._validate_ownership(project, user, "Solo el cliente propietario puede actualizar este proyecto")
        
        def update_operation():
            allowed_fields = ['title', 'description', 'budget', 'deadline', 'state']
            
            for field in allowed_fields:
                if field in project_data:
                    setattr(project, field, project_data[field])
            
            project.save()
            return project
        
        return self.execute_with_transaction(update_operation)
    
    def delete_project(self, project, user):
        """Elimina un proyecto"""
        self._validate_ownership(project, user, "Solo el cliente propietario puede eliminar este proyecto")
        
        def delete_operation():
            project.delete()
        
        self.execute_with_transaction(delete_operation)
    
    def get_client_projects(self, user):
        """Obtiene proyectos del cliente"""
        if not self._has_client_profile(user):
            return []
        
        try:
            from projects.models import Project
            return Project.objects.filter(
                client=user.clientprofile
            ).order_by('-created_at')
        except Exception:
            return []
    
    def get_available_projects(self, limit: Optional[int] = None):
        """Obtiene proyectos disponibles"""
        try:
            from projects.models import Project
            queryset = Project.objects.filter(
                state='OPEN'
            ).select_related('client__user').order_by('-created_at')
            
            return queryset[:limit] if limit else queryset
        except Exception:
            return []
    
    def _validate_client_permission(self, user, action: str):
        """Valida permisos de cliente"""
        if not self._has_client_profile(user):
            raise PermissionDenied(f"Solo los clientes pueden {action}")
    
    def _has_client_profile(self, user) -> bool:
        """Verifica si el usuario tiene perfil de cliente"""
        return hasattr(user, 'clientprofile') and user.clientprofile is not None


# ============================================================================
# SPECIALIZED SERVICES (SRP & ISP)
# ============================================================================

class CartService(BaseService):
    """Servicio específico para operaciones de carrito - SRP"""
    
    def add_to_cart(self, user, service):
        """Agrega un servicio al carrito"""
        self._validate_service_for_cart(user, service)
        
        def add_operation():
            cart = self._get_or_create_cart(user)
            return cart.add_service(service)
        
        return self.execute_with_transaction(add_operation)
    
    def remove_from_cart(self, user, service):
        """Remueve un servicio del carrito"""
        cart = self._get_or_create_cart(user)
        cart.remove_service(service)
    
    def get_cart_items(self, user):
        """Obtiene items del carrito"""
        cart = self._get_or_create_cart(user)
        return cart.items.select_related('service', 'service__freelancer__user').all()
    
    def get_cart_total(self, user):
        """Obtiene total del carrito"""
        cart = self._get_or_create_cart(user)
        return cart.total_price
    
    def clear_cart(self, user):
        """Vacía el carrito"""
        cart = self._get_or_create_cart(user)
        cart.clear()
    
    def _get_or_create_cart(self, user):
        """Obtiene o crea carrito"""
        from services.models import Cart
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    
    def _validate_service_for_cart(self, user, service):
        """Valida que el servicio se pueda agregar al carrito"""
        if not service.active:
            raise ValidationError("No se pueden agregar servicios inactivos al carrito")
        
        if hasattr(user, 'freelancerprofile') and service.freelancer == user.freelancerprofile:
            raise ValidationError("No puedes agregar tus propios servicios al carrito")


class WishlistService(BaseService):
    """Servicio específico para lista de deseos - SRP"""
    
    def add_to_wishlist(self, user, service):
        """Agrega servicio a wishlist"""
        if not service.active:
            raise ValidationError("No se pueden agregar servicios inactivos a la wishlist")
        
        wishlist = self._get_or_create_wishlist(user)
        return wishlist.add_service(service)
    
    def remove_from_wishlist(self, user, service):
        """Remueve servicio de wishlist"""
        wishlist = self._get_or_create_wishlist(user)
        wishlist.remove_service(service)
    
    def get_wishlist_items(self, user):
        """Obtiene items de wishlist"""
        wishlist = self._get_or_create_wishlist(user)
        return wishlist.items.select_related('service', 'service__freelancer__user').all()
    
    def is_in_wishlist(self, user, service) -> bool:
        """Verifica si está en wishlist"""
        try:
            from services.models import WishlistItem
            wishlist = self._get_or_create_wishlist(user)
            return WishlistItem.objects.filter(wishlist=wishlist, service=service).exists()
        except Exception:
            return False
    
    def _get_or_create_wishlist(self, user):
        """Obtiene o crea wishlist"""
        from services.models import Wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        return wishlist


class MentorshipService(BaseService, CRUDMixin):
    """Servicio específico para mentorías - SRP"""
    
    def create_mentorship(self, user, data: dict):
        """Crea una mentoría"""
        if not hasattr(user, 'freelancerprofile'):
            raise ValidationError("Solo los freelancers pueden crear mentorías")
        
        def create_operation():
            from mentorship.models import MentorshipSession
            
            mentorship = MentorshipSession.objects.create(
                mentor=user.freelancerprofile,
                title=data['title'],
                description=data['description'],
                category=data['category'],
                price=data['price'],
                duration_hours=data['duration_hours'],
                notes=data.get('notes', '')
            )
            return mentorship
        
        return self.execute_with_transaction(create_operation)
    
    def book_mentorship(self, mentorship, user):
        """Reserva una mentoría"""
        if not hasattr(user, 'freelancerprofile'):
            raise ValidationError("Solo los freelancers pueden reservar mentorías")
        
        if mentorship.mentor == user.freelancerprofile:
            raise ValidationError("No puedes reservar tu propia mentoría")
        
        if not mentorship.is_available:
            raise ValidationError("Esta mentoría no está disponible")
        
        def book_operation():
            mentorship.book_session(user.freelancerprofile)
            return mentorship
        
        return self.execute_with_transaction(book_operation)
    
    def get_available_mentorships(self):
        """Obtiene mentorías disponibles"""
        from mentorship.models import MentorshipSession
        return MentorshipSession.objects.filter(
            status=MentorshipSession.AVAILABLE,
            mentee__isnull=True
        ).select_related('mentor__user').order_by('-created_at')


# ============================================================================
# FAÇADE SERVICES (Façade Pattern)
# ============================================================================

class UserServiceFacade:
    """Façade que unifica todos los servicios relacionados con usuarios"""
    
    def __init__(self):
        self.profile_service = UserProfileService()
        self.service_management = ServiceManagementService()
        self.project_management = ProjectManagementService()
        self.cart_service = CartService()
        self.wishlist_service = WishlistService()
        self.mentorship_service = MentorshipService()
    
    # Delegación a servicios específicos
    def create_profile(self, user, profile_type: str, data: dict = None):
        return self.profile_service.create_profile(user, profile_type, data)
    
    def update_profile(self, user, profile_type: str, data: dict):
        return self.profile_service.update_profile(user, profile_type, data)
    
    def get_user_dashboard_data(self, user) -> dict:
        """Método de conveniencia que agrupa datos del dashboard"""
        return {
            'profiles': self.profile_service.get_all_profiles(user),
            'services': self.service_management.get_freelancer_services(user),
            'projects': self.project_management.get_client_projects(user),
            'cart_items': self.cart_service.get_cart_items(user),
            'wishlist_items': self.wishlist_service.get_wishlist_items(user),
        }


# ============================================================================
# REGISTRATION (OCP)
# ============================================================================

# Registrar servicios en la factory para extensibilidad
ServiceFactory.register_service('profile', UserProfileService)
ServiceFactory.register_service('service_management', ServiceManagementService)
ServiceFactory.register_service('project_management', ProjectManagementService)
ServiceFactory.register_service('cart', CartService)
ServiceFactory.register_service('wishlist', WishlistService)
ServiceFactory.register_service('mentorship', MentorshipService)