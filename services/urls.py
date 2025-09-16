from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # URLs principales de servicios
    path('', views.ServiceListView.as_view(), name='service_list'),
    path('<uuid:service_id>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    # URLs para freelancers
    path('freelancer/', views.FreelancerServiceListView.as_view(), name='freelancer_services'),
    
    # Cart URLs
    path('cart/', views.UnifiedCartView.as_view(), name='cart_view'),
    path('cart/add/<uuid:service_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<uuid:service_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    
    # URLs de la wishlist
    path('wishlist/', views.WishlistView.as_view(), name='wishlist_view'),
    path('wishlist/add/<uuid:service_id>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<uuid:service_id>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]