from django.core.exceptions import PermissionDenied, ValidationError
from typing import Optional
from .base import BaseService
from ..mixins.crud_mixin import CRUDMixin

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
            
            self.logger.info(f"Project created: {project.title} by {user.username}")
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
            self.logger.info(f"Project updated: {project.title} by {user.username}")
            return project
        
        return self.execute_with_transaction(update_operation)
    
    def delete_project(self, project, user):
        """Elimina un proyecto"""
        self._validate_ownership(project, user, "Solo el cliente propietario puede eliminar este proyecto")
        
        def delete_operation():
            project_title = project.title
            project.delete()
            self.logger.info(f"Project deleted: {project_title} by {user.username}")
        
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
        except Exception as e:
            self.logger.error(f"Error getting projects for client {user.username}: {str(e)}")
            return []
    
    def get_available_projects(self, limit: Optional[int] = None):
        """Obtiene proyectos disponibles"""
        try:
            from projects.models import Project
            queryset = Project.objects.filter(
                state='OPEN'
            ).select_related('client__user').order_by('-created_at')
            
            return queryset[:limit] if limit else queryset
        except Exception as e:
            self.logger.error(f"Error getting available projects: {str(e)}")
            return []
    
    def apply_to_project(self, project, user, application_data: dict = None):
        """Permite a un freelancer aplicar a un proyecto"""
        self._validate_freelancer_permission(user, "aplicar a proyectos")
        
        if project.state != 'OPEN':
            raise ValidationError("Este proyecto no está disponible para aplicaciones")
        
        def apply_operation():
            from projects.models import ProjectApplication
            
            # Verificar si ya aplicó
            existing_application = ProjectApplication.objects.filter(
                project=project,
                freelancer=user.freelancerprofile
            ).first()
            
            if existing_application:
                raise ValidationError("Ya has aplicado a este proyecto")
            
            application = ProjectApplication.objects.create(
                project=project,
                freelancer=user.freelancerprofile,
                cover_letter=application_data.get('cover_letter', '') if application_data else '',
                proposed_budget=application_data.get('proposed_budget') if application_data else None,
                status='PENDING'
            )
            
            self.logger.info(f"Application submitted: {user.username} to project {project.title}")
            return application
        
        return self.execute_with_transaction(apply_operation)
    
    def get_freelancer_applications(self, user):
        """Obtiene aplicaciones del freelancer"""
        if not self._has_freelancer_profile(user):
            return []
        
        try:
            from projects.models import ProjectApplication
            return ProjectApplication.objects.filter(
                freelancer=user.freelancerprofile
            ).select_related('project', 'project__client__user').order_by('-created_at')
        except Exception as e:
            self.logger.error(f"Error getting applications for freelancer {user.username}: {str(e)}")
            return []
    
    def get_freelancer_assigned_projects(self, user):
        """Obtiene proyectos asignados al freelancer"""
        if not self._has_freelancer_profile(user):
            return []
        
        try:
            from projects.models import Project
            return Project.objects.filter(
                assigned_freelancer=user.freelancerprofile,
                state__in=['IN_PROGRESS', 'COMPLETED']
            ).select_related('client__user').order_by('-created_at')
        except Exception as e:
            self.logger.error(f"Error getting assigned projects for freelancer {user.username}: {str(e)}")
            return []
    
    def _validate_client_permission(self, user, action: str):
        """Valida permisos de cliente"""
        if not self._has_client_profile(user):
            raise PermissionDenied(f"Solo los clientes pueden {action}")
    
    def _validate_freelancer_permission(self, user, action: str):
        """Valida permisos de freelancer"""
        if not self._has_freelancer_profile(user):
            raise PermissionDenied(f"Solo los freelancers pueden {action}")
    
    def _has_client_profile(self, user) -> bool:
        """Verifica si el usuario tiene perfil de cliente"""
        return hasattr(user, 'clientprofile') and user.clientprofile is not None
    
    def _has_freelancer_profile(self, user) -> bool:
        """Verifica si el usuario tiene perfil de freelancer"""
        return hasattr(user, 'freelancerprofile') and user.freelancerprofile is not None