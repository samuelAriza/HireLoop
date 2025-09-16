from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.db.models import Q

from .models import Project, ProjectApplication
from core.forms import ProjectForm, ProjectApplicationForm
from core.services import ProjectManagementService


class ProjectListView(ListView):
    """
    Vista para listar todos los proyectos abiertos.
    Sigue SRP: Solo maneja listado de proyectos.
    Aplica KISS: Vista simple con paginación.
    """
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        """Obtiene proyectos filtrados por búsqueda"""
        queryset = Project.objects.filter(state='OPEN').select_related('client__user')
        
        # Obtener parámetros de búsqueda
        search_query = self.request.GET.get('search', '')
        min_budget = self.request.GET.get('min_budget', '')
        max_budget = self.request.GET.get('max_budget', '')
        
        # Aplicar filtros
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(client__user__username__icontains=search_query) |
                Q(client__user__first_name__icontains=search_query) |
                Q(client__user__last_name__icontains=search_query)
            )
            
        if min_budget:
            try:
                queryset = queryset.filter(budget__gte=float(min_budget))
            except ValueError:
                pass
                
        if max_budget:
            try:
                queryset = queryset.filter(budget__lte=float(max_budget))
            except ValueError:
                pass
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pasar filtros actuales al template
        context['current_filters'] = {
            'search': self.request.GET.get('search', ''),
            'min_budget': self.request.GET.get('min_budget', ''),
            'max_budget': self.request.GET.get('max_budget', ''),
        }
        
        # Verificar si hay filtros aplicados
        context['has_filters'] = any(context['current_filters'].values())
        
        return context


class ProjectDetailView(DetailView):
    """
    Vista de detalle de proyecto con funcionalidad de aplicación.
    Sigue SRP: Solo maneja visualización y aplicación a proyectos.
    """
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Verificar si el freelancer ya aplicó
        if self.request.user.is_authenticated and self.request.user.has_freelancer_profile:
            has_applied = ProjectApplication.objects.filter(
                project=project,
                freelancer=self.request.user.freelancerprofile
            ).exists()
            context['has_applied'] = has_applied
            context['application_form'] = ProjectApplicationForm()
        
        context['is_owner'] = (
            self.request.user.is_authenticated and 
            self.request.user.has_client_profile and 
            project.client.user == self.request.user
        )
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Manejar aplicación a proyecto"""
        project = self.get_object()
        
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para aplicar a proyectos")
            return redirect('core:login')
        
        if not request.user.has_freelancer_profile:
            messages.error(request, "Solo los freelancers pueden aplicar a proyectos")
            return redirect('projects:project_detail', project_id=project.id)
        
        form = ProjectApplicationForm(request.POST)
        if form.is_valid():
            try:
                ProjectManagementService.apply_to_project(
                    project, 
                    request.user, 
                    form.cleaned_data.get('message', '')
                )
                messages.success(request, "¡Has aplicado exitosamente al proyecto!")
            except Exception as e:
                messages.error(request, str(e))
        
        return redirect('projects:project_detail', project_id=project.id)


class ClientProjectListView(LoginRequiredMixin, ListView):
    """
    Vista para que los clientes gestionen sus proyectos.
    Sigue SRP: Solo maneja listado de proyectos del cliente.
    """
    template_name = 'projects/client_project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_client_profile:
            messages.error(request, "Solo los clientes pueden acceder a esta sección")
            return redirect('core:multi_profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return ProjectManagementService.get_client_projects(self.request.user)


class CreateProjectView(LoginRequiredMixin, FormView):
    """
    Vista para crear nuevos proyectos.
    Sigue SRP: Solo maneja creación de proyectos.
    """
    template_name = 'projects/create_project.html'
    form_class = ProjectForm
    success_url = reverse_lazy('projects:client_projects')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_client_profile:
            messages.error(request, "Solo los clientes pueden crear proyectos")
            return redirect('core:multi_profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        try:
            project = ProjectManagementService.create_project(
                self.request.user,
                form.cleaned_data
            )
            messages.success(
                self.request, 
                f"¡Proyecto '{project.title}' creado exitosamente!"
            )
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class UpdateProjectView(LoginRequiredMixin, FormView):
    """
    Vista para actualizar proyectos existentes.
    Sigue SRP: Solo maneja edición de proyectos.
    """
    template_name = 'projects/update_project.html'
    form_class = ProjectForm
    
    def get_project(self):
        project_id = self.kwargs.get('project_id')
        return get_object_or_404(Project, id=project_id)
    
    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()
        if not request.user.has_client_profile or project.client.user != request.user:
            raise PermissionDenied("Solo el propietario puede editar este proyecto")
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        project = self.get_project()
        return {
            'title': project.title,
            'description': project.description,
            'budget': project.budget,
            'deadline': project.deadline,
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        return context
    
    def form_valid(self, form):
        try:
            project = self.get_project()
            ProjectManagementService.update_project(
                project,
                self.request.user,
                form.cleaned_data
            )
            messages.success(
                self.request, 
                f"¡Proyecto '{project.title}' actualizado exitosamente!"
            )
            return redirect('projects:client_projects')
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class DeleteProjectView(LoginRequiredMixin, DetailView):
    """
    Vista para eliminar proyectos.
    Sigue SRP: Solo maneja eliminación de proyectos.
    """
    template_name = 'projects/delete_project.html'
    model = Project
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'
    
    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if not request.user.has_client_profile or project.client.user != request.user:
            raise PermissionDenied("Solo el propietario puede eliminar este proyecto")
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            project = self.get_object()
            project_title = project.title
            ProjectManagementService.delete_project(project, request.user)
            messages.success(request, f"Proyecto '{project_title}' eliminado exitosamente")
            return redirect('projects:client_projects')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('projects:client_projects')


class ProjectApplicationsView(LoginRequiredMixin, DetailView):
    """
    Vista para que los clientes gestionen aplicaciones a sus proyectos.
    Sigue SRP: Solo maneja visualización y gestión de aplicaciones.
    """
    template_name = 'projects/project_applications.html'
    model = Project
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'
    
    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if not request.user.has_client_profile or project.client.user != request.user:
            raise PermissionDenied("Solo el propietario puede ver las aplicaciones")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['applications'] = ProjectManagementService.get_project_applications(
            project, self.request.user
        )
        return context
    
    def post(self, request, *args, **kwargs):
        """Manejar aceptación/rechazo de aplicaciones"""
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')
        
        if not application_id or action not in ['ACCEPT', 'REJECT']:
            messages.error(request, "Acción no válida")
            return redirect('projects:project_applications', project_id=self.get_object().id)
        
        try:
            application = get_object_or_404(ProjectApplication, id=application_id)
            ProjectManagementService.manage_application(
                application, request.user, action
            )
            
            action_text = "aceptada" if action == 'ACCEPT' else "rechazada"
            messages.success(
                request, 
                f"Aplicación de {application.freelancer.user.username} {action_text}"
            )
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('projects:project_applications', project_id=self.get_object().id)