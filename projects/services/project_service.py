from typing import List, Optional
from ..models import Project, ProjectAssignment
from ..repositories.project_repository import ProjectRepository, ProjectAssignmentRepository

class ProjectService:
    def __init__(self, project_repo: ProjectRepository, assignment_repo: ProjectAssignmentRepository):
        self.project_repo = project_repo
        self.assignment_repo = assignment_repo
    
    def create_project(self, client_id, title, description, budget) -> Project:
        return self.project_repo.create(
            client_id=client_id,
            title=title,
            description=description,
            budget=budget
        )
    
    def get_project(self, project_id) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        return project
    
    def update_project(self, project_id, **kwargs) -> Project:
        project = self.get_project(project_id)
        return self.project_repo.update(project, **kwargs)
    
    def delete_project(self, project_id) -> bool:
        project = self.get_project(project_id)
        return self.project_repo.delete(project)

    def list_client_projects(self, client_id) -> List[Project]:
        return self.project_repo.list_by_client(client_id)
    
    def assign_freelancer(self, project_id, freelancer_id, role="", agreed_payment=0) -> ProjectAssignment:
        project = self.get_project(project_id)
        return self.assignment_repo.create(
            project=project,
            freelancer_id=freelancer_id,
            role=role,
            agreed_payment=agreed_payment
        )

    def list_projects(self) -> List[Project]:
        return self.project_repo.list_all()