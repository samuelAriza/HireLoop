import uuid
from django.urls import path
from .views.views import (
    MicroServiceListView,
    MicroServiceCreateView,
    MicroServiceUpdateView,
    MicroServiceDeleteView,
    MicroServiceFreelancerListView
)

app_name = 'microservices'

urlpatterns = [
    path('', MicroServiceListView.as_view(), name='microservices_list'),
    path('create/', MicroServiceCreateView.as_view(), name='microservices_create'),
    path('update/<uuid:pk>/', MicroServiceUpdateView.as_view(), name='microservices_update'),
    path('delete/<uuid:pk>/', MicroServiceDeleteView.as_view(), name='microservices_delete'),
    path('freelancer/<uuid:freelancer_id>/', MicroServiceFreelancerListView.as_view(), name='microservices_freelancer_list'),
]