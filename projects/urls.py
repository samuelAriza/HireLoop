from .views.views import (
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectClientListView,
    ProjectAssignmentCreateView,
    ProjectAssignmentUpdateView,
    ProjectDetailView,
    ProjectApplicationCreateView,
    ProjectApplicationAcceptView,
    ProjectApplicationRejectView,
)

from django.urls import path

app_name = "projects"

urlpatterns = [
    path("", ProjectListView.as_view(), name="projects_list"),
    path("create/", ProjectCreateView.as_view(), name="project_create"),
    path("update/<uuid:pk>/", ProjectUpdateView.as_view(), name="project_update"),
    path("delete/<uuid:pk>/", ProjectDeleteView.as_view(), name="project_delete"),
    path(
        "client/<uuid:client_id>/",
        ProjectClientListView.as_view(),
        name="projects_client_list",
    ),
    path(
        "<uuid:project_id>/assignments/create/",
        ProjectAssignmentCreateView.as_view(),
        name="assignment_create",
    ),
    path(
        "assignments/<uuid:pk>/update/",
        ProjectAssignmentUpdateView.as_view(),
        name="assignment_update",
    ),
    path("<uuid:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path(
        "<uuid:project_id>/apply/",
        ProjectApplicationCreateView.as_view(),
        name="application_create",
    ),
    path(
        "applications/<uuid:pk>/accept/",
        ProjectApplicationAcceptView.as_view(),
        name="application_accept",
    ),
    path(
        "applications/<uuid:pk>/reject/",
        ProjectApplicationRejectView.as_view(),
        name="application_reject",
    ),
]
