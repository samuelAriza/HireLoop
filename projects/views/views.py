from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from core.mixins import ProfileRequiredMixin
from ..models import Project
from ..repositories.project_repository import ProjectRepository, ProjectAssignmentRepository
from ..services.project_service import ProjectService
from ..forms.projects_form import ProjectCreateForm, ProjectUpdateForm, ProjectAssignmentForm, ProjectAssignmentUpdateForm
from core.models import ClientProfile

project_service = ProjectService(
    project_repo=ProjectRepository(),
    assignment_repo=ProjectAssignmentRepository()
)

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return project_service.list_projects()
    
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