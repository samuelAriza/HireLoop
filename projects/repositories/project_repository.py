from typing import Optional, List
from ..models import Project, ProjectAssignment
from core.repositories.base_repository import BaseRepository

class ProjectRepository(BaseRepository):
    def create(self, **kwargs) -> Project:
        return Project.objects.create(**kwargs)
    
    def get_by_id(self, entity_id) -> Optional[Project]:
        return Project.objects.filter(id=entity_id).first()
    
    def update(self, entity: Project, **kwargs) -> Project:
        for key, value in kwargs.items():
            setattr(entity, key, value)
        entity.save()
        return entity
    
    def delete(self, entity: Project) -> bool:
        deleted, _ = entity.delete()
        return deleted > 0
    
    def list_by_client(self, client_id) -> List[Project]:
        return Project.objects.filter(client_id=client_id).all()
    
    def list_all(self) -> List[Project]:
        return Project.objects.all()

class ProjectAssignmentRepository(BaseRepository):
    def create(self, **kwargs) -> ProjectAssignment:
        return ProjectAssignment.objects.create(**kwargs)
    
    def get_by_id(self, entity_id) -> Optional[ProjectAssignment]:
        return ProjectAssignment.objects.filter(id=entity_id).first()
    
    def update(self, entity: ProjectAssignment, **kwargs) -> ProjectAssignment:
        for key, value in kwargs.items():
            setattr(entity, key, value)
        entity.save()
        return entity
    
    def delete(self, entity: ProjectAssignment) -> bool:
        deleted, _ = entity.delete()
        return deleted > 0
    
    def list_by_project(self, project_id) -> List[ProjectAssignment]:
        return ProjectAssignment.objects.filter(project_id=project_id).all()