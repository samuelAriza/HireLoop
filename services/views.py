from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

def service_list_view(request):
    return render(request, 'services/list_services.html')