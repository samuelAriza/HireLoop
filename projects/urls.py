from .views.views import (
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectClientListView
)
from django.urls import path
import uuid

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('update/<uuid:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('delete/<uuid:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('client/<uuid:client_id>/', ProjectClientListView.as_view(), name='projects_client_list'),
]