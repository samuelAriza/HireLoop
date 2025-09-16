from django.urls import path
from .views import (
    UserRegisterView, UserLoginView, UserLogoutView,
    MultiProfileDetailView, CreateProfileView,
    FreelancerServicesView, CreateServiceView, UpdateServiceView, DeleteServiceView,
    FreelancerProjectsView
)

app_name = 'core'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', MultiProfileDetailView.as_view(), name='multi_profile_detail'),
    path('profile/create/<str:profile_type>/', CreateProfileView.as_view(), name='create_profile'),
    path('services/', FreelancerServicesView.as_view(), name='freelancer_services'),
    path('services/create/', CreateServiceView.as_view(), name='create_service'),
    path('services/<uuid:service_id>/edit/', UpdateServiceView.as_view(), name='update_service'),
    path('services/<uuid:service_id>/delete/', DeleteServiceView.as_view(), name='delete_service'),
    path('freelancer/projects/', FreelancerProjectsView.as_view(), name='freelancer_projects'),
    path('profile/freelancer/update/', MultiProfileDetailView.as_view(), name='freelancer_profile_update'),
    path('profile/client/update/', MultiProfileDetailView.as_view(), name='client_profile_update'),
]