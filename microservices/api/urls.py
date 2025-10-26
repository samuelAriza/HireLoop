# microservices/api/urls.py
from django.urls import path
from .views import MicroServiceListAPIView, MicroServiceDetailAPIView

app_name = "microservices-api"

urlpatterns = [
    path("microservices/", MicroServiceListAPIView.as_view(), name="microservice-list"),
    path(
        "microservices/<uuid:id>/",
        MicroServiceDetailAPIView.as_view(),
        name="microservice-detail",
    ),
]
