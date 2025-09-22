from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from core.mixins import ProfileRequiredMixin
from ..models import Project, ProjectAssignment, ProjectApplication
from ..repositories.project_repository import ProjectRepository, ProjectAssignmentRepository, ProjectApplicationRepository
from ..services.project_service import ProjectService
from ..forms.projects_form import ProjectCreateForm, ProjectUpdateForm, ProjectAssignmentForm, ProjectAssignmentUpdateForm, ProjectApplicationForm
from core.models import ClientProfile

project_service = ProjectService(
    project_repo=ProjectRepository(),
    assignment_repo=ProjectAssignmentRepository(),
    application_repo=ProjectApplicationRepository()
)

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return project_service.list_projects()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_owner_map = {}
        has_applied_map = {}

        for project in context['projects']:
            is_owner_map[project.id] = hasattr(user, "clientprofile") and project.client == user.clientprofile
            if hasattr(user, "freelancer_profile"):
                has_applied_map[project.id] = project.applications.filter(
                    freelancer=user.freelancer_profile
                ).exists()

        context['is_owner_map'] = is_owner_map
        context['has_applied_map'] = has_applied_map
        return context
    
class ProjectClientListView(ProfileRequiredMixin, ListView):
    required_profile = "client"
    model = Project
    template_name = 'projects/client_projects_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        client_profile = get_object_or_404(ClientProfile, pk=self.kwargs['client_id'])
        return project_service.list_client_projects(client_profile.id)

class ProjectCreateView(ProfileRequiredMixin, CreateView):
    required_profile = "client"
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:projects_client_list')

    def form_valid(self, form):
        client_profile = self.request.user.client_profile
        form.instance.client = client_profile  # Usa la FK directamente
        self.object = form.save()  # Guarda el proyecto

        return redirect(
            reverse(
                'projects:projects_client_list',
                kwargs={'client_id': client_profile.id}
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

class ProjectUpdateView(ProfileRequiredMixin, UpdateView):
    required_profile = "client"
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:projects_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

class ProjectDeleteView(ProfileRequiredMixin, DeleteView):
    required_profile = "client"
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:projects_list')

class ProjectAssignmentCreateView(ProfileRequiredMixin, CreateView):
    required_profile = "client"
    model = ProjectAssignment
    form_class = ProjectAssignmentForm
    template_name = "projects/assignment_form.html"

    def get_initial(self):
        initial = super().get_initial()
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        initial["project"] = project
        return initial

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        form.instance.project = project

        assignment = form.save()
        project.budget -= assignment.agreed_payment or 0
        project.save(update_fields=["budget"])

        return redirect(reverse("projects:project_detail", kwargs={"pk": project.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, pk=self.kwargs["project_id"])
        context["is_edit"] = False
        return context


class ProjectAssignmentUpdateView(ProfileRequiredMixin, UpdateView):
    required_profile = "client"
    model = ProjectAssignment
    form_class = ProjectAssignmentUpdateForm
    template_name = "projects/assignment_form.html"

    def form_valid(self, form):
        assignment = form.save(commit=False)
        project = assignment.project
        old_payment = ProjectAssignment.objects.get(id=assignment.id).agreed_payment or 0
        project.budget += old_payment
        project.budget -= assignment.agreed_payment or 0
        project.save(update_fields=["budget"])
        assignment.save()

        return redirect(reverse("projects:project_detail", kwargs={"pk": project.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.object.project
        context["is_edit"] = True
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        user = self.request.user
        context['is_open'] = project.status == Project.ProjectStatus.CREATED
        context['is_owner'] = hasattr(user, "client_profile") and project.client == user.client_profile
        context['is_freelancer'] = hasattr(user, "freelancer_profile")
        
        if context['is_freelancer']:
            has_applied = project.applications.filter(freelancer=user.freelancer_profile).exists()
            context['has_applied'] = has_applied
            
        if context['is_owner']:
            context['applications'] = project.applications.all()
            
        from ..forms.projects_form import ProjectApplicationForm
        context['application_form'] = ProjectApplicationForm()

        return context

class ProjectApplicationCreateView(ProfileRequiredMixin, CreateView):
    required_profile = "freelancer"
    model = ProjectApplication
    form_class = ProjectApplicationForm
    template_name = "projects/application_form.html"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        freelancer = self.request.user.freelancer_profile
        form.instance.project = project
        form.instance.freelancer = freelancer
        form.instance.status = ProjectApplication.ApplicationStatus.PENDING
        form.save()
        return redirect("projects:projects_list")

class ProjectApplicationAcceptView(ProfileRequiredMixin, View):
    required_profile = "client"

    def post(self, request, pk, *args, **kwargs):
        application = get_object_or_404(ProjectApplication, pk=pk)

        if application.project.client.user != request.user:
            return redirect('projects:projects_list')

        project = application.project

        application.status = ProjectApplication.ApplicationStatus.ACCEPTED
        application.save()

        if application.proposed_payment:
            project.budget -= application.proposed_payment
            project.save(update_fields=["budget"])

        return redirect('projects:project_detail', pk=project.pk)

class ProjectApplicationRejectView(ProfileRequiredMixin, View):
    required_profile = "client"

    def post(self, request, pk, *args, **kwargs):
        application = get_object_or_404(ProjectApplication, pk=pk)

        if application.project.client.user != request.user:
            return redirect('projects:projects_list')

        application.status = ProjectApplication.ApplicationStatus.REJECTED
        application.save()

        return redirect('projects:project_detail', pk=application.project.pk)
