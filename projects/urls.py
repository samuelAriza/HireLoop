"""
Project URLs - RESTful URL Configuration

Following REST principles and clean URL design:
- Clear, intuitive URL structure
- Proper HTTP methods mapping
- Consistent naming conventions
- SEO-friendly URLs
"""

from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Proyectos públicos - Freelancers pueden ver y aplicar
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<uuid:project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # Gestión de proyectos para clientes - Siguiendo REST
    path('client/', views.ClientProjectListView.as_view(), name='client_projects'),
    path('create/', views.CreateProjectView.as_view(), name='create_project'),
    path('<uuid:project_id>/edit/', views.UpdateProjectView.as_view(), name='update_project'),
    path('<uuid:project_id>/delete/', views.DeleteProjectView.as_view(), name='delete_project'),
    
    # Gestión de aplicaciones
    path('<uuid:project_id>/applications/', views.ProjectApplicationsView.as_view(), name='project_applications'),
]