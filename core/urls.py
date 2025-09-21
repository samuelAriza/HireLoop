from django.urls import path

# Importaciones directas para evitar circularidad
from core.views.auth_views import UserRegisterView, UserLoginView, UserLogoutView
from core.views.profile_views import (
    ProfileDetailView,
    FreelancerProfileCreateView,
    ClientProfileCreateView,
    PublicProfileDetailView,
)
from core.views.image_views import ProfileImageUpdateView, ProfileImageDeleteView
from core.views.portfolio_views import (
    PortfolioCreateView,
)

app_name = 'core'

urlpatterns = [
    # Authentication
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # Profile management
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/freelancer/create/', FreelancerProfileCreateView.as_view(), name='freelancer_profile_create'),
    path('profile/client/create/', ClientProfileCreateView.as_view(), name='client_profile_create'),
    
    # Profile image management
    path('profile/image/update/', ProfileImageUpdateView.as_view(), name='profile_image_update'),
    path('profile/image/delete/', ProfileImageDeleteView.as_view(), name='profile_image_delete'),
    
    # Portfolio management
    path('portfolio/create/', PortfolioCreateView.as_view(), name='portfolio_create'),

    path('profile/public/<str:username>/', PublicProfileDetailView.as_view(), name='public_profile_detail'),

]