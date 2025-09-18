from django.urls import path
from .views import (
    service_list_view,
)
app_name = 'services'

urlpatterns = [
    path('services/', service_list_view, name='service_list'),
]