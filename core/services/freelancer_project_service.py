from .base import BaseService

class FreelancerProjectService(BaseService):
    """Servicio específico para operaciones de proyectos desde perspectiva freelancer"""
    
    def get_freelancer_applications(self, user):
        """Obtiene aplicaciones del freelancer"""
        if not hasattr(user, 'freelancerprofile'):
            return []
        
        try:
            from projects.models import ProjectApplication
            return ProjectApplication.objects.filter(
                freelancer=user.freelancerprofile
            ).select_related(
                'project', 
                'project__client__user'
            ).order_by('-created_at')
        except Exception as e:
            self.logger.error(f"Error getting freelancer applications: {str(e)}")
            return []
    
    def get_freelancer_assigned_projects(self, user):
        """Obtiene proyectos asignados al freelancer"""
        if not hasattr(user, 'freelancerprofile'):
            return []
        
        try:
            from projects.models import Project
            return Project.objects.filter(
                assigned_freelancer=user.freelancerprofile
            ).select_related('client__user').order_by('-updated_at')
        except Exception as e:
            self.logger.error(f"Error getting assigned projects: {str(e)}")
            return []