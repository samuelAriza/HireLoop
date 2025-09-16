"""
Mentorship URLs - RESTful URL Configuration

Following REST principles and clean URL design:
- Clear, intuitive URL structure
- Proper HTTP methods mapping
- Consistent naming conventions
- SEO-friendly URLs
"""

from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'mentorship'

# Main mentorship URLs
urlpatterns = [
    # URLs principales - Todas las vistas CRUD
    path('', views.MentorshipListView.as_view(), name='mentorship_list'),
    path('sessions/', views.MentorshipListView.as_view(), name='session_list'),  # Alias para compatibilidad
    path('mentors/', TemplateView.as_view(template_name='mentorship/mentor_list.html'), name='mentor_list'),
    path('mentor-dashboard/', TemplateView.as_view(template_name='mentorship/mentor_dashboard.html'), name='mentor_dashboard'),
    path('mentee-dashboard/', TemplateView.as_view(template_name='mentorship/mentee_dashboard.html'), name='mentee_dashboard'),
    
    path('<uuid:pk>/', views.MentorshipDetailView.as_view(), name='mentorship_detail'),
    path('create/', views.CreateMentorshipView.as_view(), name='create_mentorship'),
    
    # Gestión de mentorías del freelancer - Vistas CRUD completas  
    path('my-mentorships/', views.FreelancerMentorshipsView.as_view(), name='freelancer_mentorships'),
    path('<uuid:pk>/edit/', views.UpdateMentorshipView.as_view(), name='mentorship_update'),
    path('<uuid:pk>/delete/', views.DeleteMentorshipView.as_view(), name='mentorship_delete'),
    
    # URLs para cambio de estado
    path('<uuid:mentorship_id>/status/', views.MentorshipStatusView.as_view(), name='mentorship_status'),
    
    # URLs del carrito y wishlist
    path('<uuid:mentorship_id>/add-to-cart/', views.AddMentorshipToCartView.as_view(), name='add_to_cart'),
    path('<uuid:mentorship_id>/remove-from-cart/', views.RemoveMentorshipFromCartView.as_view(), name='remove_from_cart'),
    path('<uuid:mentorship_id>/add-to-wishlist/', views.AddMentorshipToWishlistView.as_view(), name='add_to_wishlist'),
    path('<uuid:mentorship_id>/remove-from-wishlist/', views.RemoveMentorshipFromWishlistView.as_view(), name='remove_from_wishlist'),
    
    # Cart and Wishlist URLs
    path('add-to-cart/<int:mentorship_id>/', views.AddMentorshipToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:mentorship_id>/', views.RemoveMentorshipFromCartView.as_view(), name='remove_from_cart'),
    path('add-to-wishlist/<int:mentorship_id>/', views.AddMentorshipToWishlistView.as_view(), name='add_to_wishlist'),
    path('remove-from-wishlist/<int:mentorship_id>/', views.RemoveMentorshipFromWishlistView.as_view(), name='remove_from_wishlist'),
    
    # Update and delete URLs
    path('update/<uuid:mentorship_id>/', views.UpdateMentorshipView.as_view(), name='update_mentorship'),
    path('delete/<uuid:mentorship_id>/', views.DeleteMentorshipView.as_view(), name='delete_mentorship'),
    path('status/<uuid:mentorship_id>/', views.MentorshipStatusView.as_view(), name='mentorship_status'),
]