from typing import List
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from ..models import Project, ProjectAssignment, ProjectApplication
from ..repositories.project_repository import (
    ProjectRepository,
    ProjectAssignmentRepository,
    ProjectApplicationRepository,
)


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        assignment_repo: ProjectAssignmentRepository,
        application_repo: ProjectApplicationRepository,
    ):
        self.project_repo = project_repo
        self.assignment_repo = assignment_repo
        self.application_repo = application_repo

    def apply_to_project(
        self, project_id, freelancer_id, cover_letter, proposed_payment
    ):
        project = self.get_project(project_id)

        existing = (
            self.application_repo.list_by_project(project.id)
            .filter(freelancer_id=freelancer_id, status__in=["PENDING", "ACCEPTED"])
            .first()
        )
        if existing:
            raise ValueError(_("Already applied to this project."))

        return self.application_repo.create(
            project=project,
            freelancer_id=freelancer_id,
            cover_letter=cover_letter,
            proposed_payment=proposed_payment,
        )

    def review_application(self, application_id, accept: bool):
        application = self.application_repo.get_by_id(application_id)
        if not application:
            raise ValueError(_("Application not found"))

        if accept:
            application.status = ProjectApplication.ApplicationStatus.ACCEPTED
            self.assignment_repo.create(
                project=application.project,
                freelancer=application.freelancer,
                role="",
                agreed_payment=application.proposed_payment,
                status=ProjectAssignment.ProjectAssignmentStatus.ACCEPTED,
            )
            application.project.budget -= application.proposed_payment
            application.project.save(update_fields=["budget"])
        else:
            application.status = ProjectApplication.ApplicationStatus.REJECTED

        return self.application_repo.update(application)

    def create_project(self, client_id, title, description, budget) -> Project:
        return self.project_repo.create(
            client_id=client_id, title=title, description=description, budget=budget
        )

    def get_project(self, project_id) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(_("Project not found"))
        return project

    def update_project(self, project_id, **kwargs) -> Project:
        project = self.get_project(project_id)
        return self.project_repo.update(project, **kwargs)

    def delete_project(self, project_id) -> bool:
        project = self.get_project(project_id)
        return self.project_repo.delete(project)

    def list_client_projects(self, client_id) -> List[Project]:
        return self.project_repo.list_by_client(client_id)

    def assign_freelancer(
        self, project_id, freelancer_id, role="", agreed_payment=0
    ) -> ProjectAssignment:
        project = self.get_project(project_id)
        return self.assignment_repo.create(
            project=project,
            freelancer_id=freelancer_id,
            role=role,
            agreed_payment=agreed_payment,
        )

    def list_projects(self) -> List[Project]:
        return self.project_repo.list_all()

    def register_interest(self, project_id, freelancer_id, role=""):
        """
        Freelancer se postula a un proyecto.
        """
        project = self.get_project(project_id)
        # evita duplicados
        existing = (
            self.assignment_repo.list_by_project(project.id)
            .filter(freelancer_id=freelancer_id)
            .first()
        )
        if existing:
            raise ValueError(
                _("Freelancer already registered or assigned to this project.")
            )

        return self.assignment_repo.create(
            project=project,
            freelancer_id=freelancer_id,
            role=role,
            status=ProjectAssignment.ProjectAssignmentStatus.INVITED,
        )

    @transaction.atomic
    def accept_assignment(self, assignment_id, agreed_payment: float):
        """
        Cliente acepta al freelancer y asigna el pago.
        """
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            raise ValueError(_("Assignment not found"))

        project = assignment.project

        if project.budget < agreed_payment:
            raise ValueError(_("Not enough budget for this assignment"))

        # Actualizar asignación
        assignment.agreed_payment = agreed_payment
        assignment.status = ProjectAssignment.ProjectAssignmentStatus.ACCEPTED
        self.assignment_repo.update(assignment)

        # Descontar del presupuesto
        project.budget -= agreed_payment
        self.project_repo.update(project, budget=project.budget)

        return assignment

    def reject_assignment(self, assignment_id):
        """
        Cliente rechaza al freelancer.
        """
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment:
            raise ValueError(_("Assignment not found"))

        assignment.status = ProjectAssignment.ProjectAssignmentStatus.REJECTED
        return self.assignment_repo.update(assignment)

    def list_assignments(self, project_id):
        """
        Ver freelancers asignados a un proyecto.
        """
        return self.assignment_repo.list_by_project(project_id)