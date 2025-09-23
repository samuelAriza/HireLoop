from django.urls import path
from .views.views import (
    MentorshipSessionListView,
    MentorshipSessionFreelancerListView,
    MentorshipSessionCreateView,
    MentorshipSessionUpdateView,
    MentorshipSessionDeleteView,
    MentorshipSessionDetailView,
)

app_name = "mentorship_session"

urlpatterns = [
    path("", MentorshipSessionListView.as_view(), name="session_list"),
    path(
        "freelancer/<uuid:freelancer_id>/",
        MentorshipSessionFreelancerListView.as_view(),
        name="sessions_freelancer_list",
    ),
    path("create/", MentorshipSessionCreateView.as_view(), name="session_create"),
    path(
        "update/<uuid:pk>/",
        MentorshipSessionUpdateView.as_view(),
        name="session_update",
    ),
    path(
        "delete/<uuid:pk>/",
        MentorshipSessionDeleteView.as_view(),
        name="session_delete",
    ),
    path(
        "detail/<uuid:pk>/",
        MentorshipSessionDetailView.as_view(),
        name="session_detail",
    ),
]
