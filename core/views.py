from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from .forms import RegisterForm, LoginForm, FreelancerProfileForm, ClientProfileForm, ServiceForm
from .services import FreelancerProfileService, ClientProfileService, ServiceManagementService, ProjectManagementService
from .services.service_management import ServiceManagementService

class UserRegisterView(FormView):
    """Vista de registro simplificada"""
    template_name = 'core/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('services:service_list')

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
            messages.success(self.request, "¡Registro exitoso! Bienvenido a HireLoop.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.form_invalid(form)

class UserLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = LoginForm
    
    def get_success_url(self):
        # Redirect to home page after login
        return reverse_lazy('services:service_list')
    
    def form_valid(self, form):
        # Manually login the user to ensure session is created
        login(self.request, form.get_user())
        messages.success(self.request, f"¡Bienvenido de vuelta, {form.get_user().username}!")
        return redirect(self.get_success_url())

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('core:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Has cerrado sesión exitosamente.")
        return super().dispatch(request, *args, **kwargs)

class MultiProfileDetailView(LoginRequiredMixin, View):
    """
    Vista para mostrar perfiles múltiples del usuario.
    Sigue SRP: Solo maneja visualización de perfiles.
    """
    template_name = 'core/multi_profile_detail.html'
    
    def get(self, request, *args, **kwargs):
        """Manejar solicitudes GET"""
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        """Manejar actualizaciones de perfil"""
        profile_type = request.POST.get('profile_type')
        
        if profile_type == 'freelancer':
            return self._handle_freelancer_update(request)
        elif profile_type == 'client':
            return self._handle_client_update(request)
        else:
            messages.error(request, "Tipo de perfil no válido")
            
        return redirect('core:multi_profile_detail')
    
    def _handle_freelancer_update(self, request):
        """Maneja actualización del perfil freelancer"""
        if not hasattr(request.user, 'freelancerprofile'):
            messages.error(request, "No tienes perfil de freelancer para editar")
            return redirect('core:multi_profile_detail')
            
        try:
            freelancer_profile = request.user.freelancerprofile
            
            # Obtener datos del formulario
            bio = request.POST.get('bio', '').strip()
            skills_str = request.POST.get('skills', '').strip()
            
            # Procesar skills: convertir string separado por comas a lista
            if skills_str:
                skills_list = [skill.strip() for skill in skills_str.split(',') if skill.strip()]
            else:
                skills_list = []
            
            # Actualizar usando el servicio
            freelancer_service = FreelancerProfileService()

            success = freelancer_service.update_freelancer_profile(
                request.user,
                {
                    'bio': bio,
                    'skills': skills_list
                }
            )
            if success:
                messages.success(request, "Perfil de freelancer actualizado exitosamente!")
            else:
                error_messages = getattr(freelancer_service, '_errors', ['Error actualizando el perfil'])
                for error in error_messages:
                    messages.error(request, error)
            
        except Exception as e:
            messages.error(request, f"Error actualizando perfil: {str(e)}")
                    
        return redirect('core:multi_profile_detail')
    
    def _handle_client_update(self, request):
        """Maneja actualización del perfil cliente"""
        if not hasattr(request.user, 'clientprofile'):
            messages.error(request, "No tienes perfil de cliente para editar")
            return redirect('core:multi_profile_detail')
            
        try:
            client_profile = request.user.clientprofile
            
            # Obtener datos del formulario
            company = request.POST.get('company', '').strip()
            billing_email = request.POST.get('billing_email', '').strip()
            
            # Actualizar usando el servicio con instancia
            client_service = ClientProfileService()
            success = client_service.update_client_profile(
                request.user,
                {
                    'company': company,
                    'billing_email': billing_email
                }
            )
            
            if success:
                messages.success(request, "Perfil de cliente actualizado exitosamente!")
            else:
                error_messages = getattr(client_service, '_errors', ['Error actualizando el perfil'])
                for error in error_messages:
                    messages.error(request, error)
            
        except Exception as e:
            messages.error(request, f"Error actualizando perfil: {str(e)}")
                    
        return redirect('core:multi_profile_detail')
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        
        # Verificar perfiles existentes usando las propiedades del modelo User
        has_freelancer = user.has_freelancer_profile
        has_client = user.has_client_profile
        
        # Obtener perfiles existentes
        profiles = {}
        if has_freelancer:
            profiles['freelancer'] = user.freelancerprofile
        if has_client:
            profiles['client'] = user.clientprofile
        
        # Determinar roles activos
        user_roles = []
        if has_freelancer:
            user_roles.append('freelancer')
        if has_client:
            user_roles.append('client')
        
        # Determinar rol primario (para tabs activos)
        primary_role = 'freelancer' if has_freelancer else 'client' if has_client else None
        
        # Preparar formularios para edición SIN usar instance
        freelancer_form = None
        client_form = None
        
        if has_freelancer:
            # Convertir la lista de skills a string separado por comas para el formulario
            skills_str = ', '.join(user.freelancerprofile.skills) if user.freelancerprofile.skills else ''
            freelancer_form = FreelancerProfileForm(initial={
                'skills': skills_str,
                'bio': user.freelancerprofile.bio or '',
            })
        else:
            freelancer_form = FreelancerProfileForm()
            
        if has_client:
            client_form = ClientProfileForm(initial={
                'company': user.clientprofile.company or '',
                'billing_email': user.clientprofile.billing_email or '',
            })
        else:
            client_form = ClientProfileForm()
        
        context = {
            'user_profile': user,
            'profiles': profiles,
            'user_roles': user_roles,
            'has_freelancer': has_freelancer,
            'has_client': has_client,
            'primary_role': primary_role,
            'freelancer_form': freelancer_form,
            'client_form': client_form,
        }
        
        return context

class CreateProfileView(LoginRequiredMixin, FormView):
    """
    Vista para crear nuevos perfiles (freelancer o cliente).
    Sigue SRP: Solo maneja creación de perfiles.
    """
    template_name = 'core/create_profile.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Verificar que el usuario no tenga ya este tipo de perfil"""
        profile_type = kwargs.get('profile_type')
        
        # Verificar si ya tiene el perfil
        if profile_type == 'freelancer' and request.user.has_freelancer_profile:
            messages.info(request, "Ya tienes un perfil de freelancer.")
            return redirect('core:multi_profile_detail')
        elif profile_type == 'client' and request.user.has_client_profile:
            messages.info(request, "Ya tienes un perfil de cliente.")
            return redirect('core:multi_profile_detail')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_class(self):
        profile_type = self.kwargs.get('profile_type')
        if profile_type == 'freelancer':
            return FreelancerProfileForm
        elif profile_type == 'client':
            return ClientProfileForm
        else:
            raise Http404("Tipo de perfil no válido")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_type'] = self.kwargs.get('profile_type')
        return context
    
    def form_valid(self, form):
        profile_type = self.kwargs.get('profile_type')
        
        # Verificar nuevamente antes de crear (por seguridad)
        if profile_type == 'freelancer' and self.request.user.has_freelancer_profile:
            messages.error(self.request, "Ya tienes un perfil de freelancer.")
            return redirect('core:multi_profile_detail')
        elif profile_type == 'client' and self.request.user.has_client_profile:
            messages.error(self.request, "Ya tienes un perfil de cliente.")
            return redirect('core:multi_profile_detail')
        
        try:
            # Crear el perfil usando el servicio
            if profile_type == 'freelancer':
                freelancer_service = FreelancerProfileService()
                profile = freelancer_service.create_freelancer_profile(
                    self.request.user, 
                    form.cleaned_data
                )
            elif profile_type == 'client':
                client_service = ClientProfileService()
                profile = client_service.create_client_profile(
                    self.request.user, 
                    form.cleaned_data
                )
            else:
                raise ValueError("Invalid profile type")
            
            # Si el perfil ya existía, mostrar mensaje y redireccionar
            if not profile:
                messages.info(self.request, f"Ya tienes un perfil de {profile_type}.")
                return redirect('core:multi_profile_detail')
            
            messages.success(
                self.request, 
                f"¡Perfil de {profile_type} creado exitosamente!"
            )
            return redirect('core:multi_profile_detail')
            
        except Exception as e:
            messages.error(self.request, f"Error creando perfil: {str(e)}")
            return self.form_invalid(form)

class FreelancerServicesView(LoginRequiredMixin, ListView):
    """Vista para listar servicios del freelancer actual"""
    template_name = 'core/freelancer_services.html'
    context_object_name = 'services'
    paginate_by = 10
    
    def get_queryset(self):
        """Obtiene los servicios del freelancer actual"""
        if not self.request.user.has_freelancer_profile:
            return []
        
        try:
            service_management = ServiceManagementService()
            return service_management.get_freelancer_services(self.request.user)
        except Exception:
            # Fallback to empty list if service not available
            return []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_freelancer'] = self.request.user.has_freelancer_profile
        return context

class CreateServiceView(LoginRequiredMixin, FormView):
    """Vista para crear nuevos servicios"""
    template_name = 'core/create_service.html'
    form_class = ServiceForm
    
    def dispatch(self, request, *args, **kwargs):
        """Verificar que el usuario sea freelancer"""
        if not request.user.has_freelancer_profile:
            messages.error(request, "Solo los freelancers pueden crear servicios.")
            return redirect('core:multi_profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        try:
            service_management = ServiceManagementService()
            service = service_management.create_service(
                self.request.user, 
                form.cleaned_data
            )
            messages.success(
                self.request, 
                f"¡Servicio '{service.title}' creado exitosamente!"
            )
            return redirect('core:freelancer_services')
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class UpdateServiceView(LoginRequiredMixin, FormView):
    """Vista para actualizar servicios existentes"""
    template_name = 'core/update_service.html'
    form_class = ServiceForm
    
    def get_service(self):
        """Obtiene el servicio a editar"""
        service_id = self.kwargs.get('service_id')
        try:
            from services.models import Service
            return get_object_or_404(Service, id=service_id, freelancer__user=self.request.user)
        except:
            raise Http404("Servicio no encontrado")
    
    def get_initial(self):
        """Datos iniciales del formulario"""
        service = self.get_service()
        return {
            'title': service.title,
            'description': service.description,
            'price': service.price,
            'delivery_time': service.delivery_time,
            'category': service.category,
            'is_active': service.active,  # Mapear active -> is_active para el formulario
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = self.get_service()
        return context
    
    def form_valid(self, form):
        try:
            service = self.get_service()
            service_management = ServiceManagementService()
            service_management.update_service(
                service,
                self.request.user, 
                form.cleaned_data
            )
            messages.success(
                self.request, 
                f"¡Servicio '{service.title}' actualizado exitosamente!"
            )
            return redirect('core:freelancer_services')
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class DeleteServiceView(LoginRequiredMixin, DetailView):
    """Vista para eliminar servicios"""
    template_name = 'core/delete_service.html'
    
    def get_service(self):
        """Obtiene el servicio a eliminar"""
        service_id = self.kwargs.get('service_id')
        try:
            from services.models import Service
            return get_object_or_404(Service, id=service_id, freelancer__user=self.request.user)
        except:
            raise Http404("Servicio no encontrado")
    
    def get_object(self):
        return self.get_service()
    
    def post(self, request, *args, **kwargs):
        """Maneja la eliminación del servicio"""
        try:
            service = self.get_service()
            service_title = service.title
            service_management = ServiceManagementService()
            service_management.delete_service(service, request.user)
            messages.success(request, f"Servicio '{service_title}' eliminado exitosamente.")
            return redirect('core:freelancer_services')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('core:freelancer_services')

class FreelancerProjectsView(LoginRequiredMixin, TemplateView):
    """Vista para que freelancers vean sus proyectos y aplicaciones"""
    template_name = 'core/freelancer_projects.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_freelancer_profile:
            messages.error(request, "Solo los freelancers pueden acceder a esta sección")
            return redirect('core:multi_profile_detail')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            from core.services import FreelancerProjectService
            
            # Obtener aplicaciones del freelancer
            context['applications'] = FreelancerProjectService.get_freelancer_applications(
                self.request.user
            )
            
            # Obtener proyectos asignados
            context['assigned_projects'] = FreelancerProjectService.get_freelancer_assigned_projects(
                self.request.user
            )
            
            # Estadísticas rápidas
            applications = context['applications']
            context['stats'] = {
                'total_applications': applications.count(),
                'pending_applications': applications.filter(status='PENDING').count(),
                'accepted_applications': applications.filter(status='ACCEPTED').count(),
                'rejected_applications': applications.filter(status='REJECTED').count(),
                'assigned_projects_count': context['assigned_projects'].count(),
            }
            
        except ImportError:
            # If FreelancerProjectService doesn't exist, provide empty data
            context['applications'] = []
            context['assigned_projects'] = []
            context['stats'] = {
                'total_applications': 0,
                'pending_applications': 0,
                'accepted_applications': 0,
                'rejected_applications': 0,
                'assigned_projects_count': 0,
            }
        
        return context
