from django.urls import path
from .api_views import MicroServiceListAPIView, MicroServiceDetailAPIView

app_name = "microservices"

urlpatterns = [
    path("microservices/", MicroServiceListAPIView.as_view(), name="microservice-list"),
    path("microservices/<uuid:id>/", MicroServiceDetailAPIView.as_view(), name="microservice-detail"),
]
