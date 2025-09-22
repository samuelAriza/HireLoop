from django.shortcuts import get_object_or_404, redirect
from core.mixins.views import ProfileRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from ..forms import MicroServiceForm
from ..models import MicroService, Category
from ..services.microservices_service import MicroServiceService
from core.mixins.search import SearchFilterMixin
from core.models import FreelancerProfile

class MicroServiceListView(SearchFilterMixin, ListView):
    model = MicroService
    template_name = 'microservices/microservices_list.html'
    context_object_name = 'microservices'
    service = MicroServiceService()
    search_fields = ["title", "description", "freelancer__user__email", "freelancer__user__username", "category__name"]
    category_field = "category__name"
    price_field = "price"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)
    
    def get_popular_categories(self):
        return Category.objects.values_list("name", flat=True).order_by("name")

class MicroServiceFreelancerListView(ProfileRequiredMixin, ListView):
    required_profile = 'freelancer'
    model = MicroService
    template_name = 'microservices/freelancer_microservices_list.html'
    context_object_name = 'microservices'
    service = MicroServiceService()
    
    def get_queryset(self):
        freelancer = get_object_or_404(FreelancerProfile, pk=self.kwargs["freelancer_id"])
        return self.service.list_freelancer_microservices(freelancer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        freelancer = get_object_or_404(FreelancerProfile, pk=self.kwargs["freelancer_id"])
        context["freelancer"] = freelancer
        context["is_freelancer"] = hasattr(self.request.user, 'freelancer_profile')
        return context

class MicroServiceCreateView(ProfileRequiredMixin, CreateView):
    required_profile = 'freelancer'
    model = MicroService
    form_class = MicroServiceForm
    template_name = 'microservices/create_microservice.html'
    success_url = reverse_lazy('microservices:microservices_freelancer_list')
    service = MicroServiceService()

    def form_valid(self, form):
        self.object = self.service.create_microservice(
            freelancer=self.request.user.freelancer_profile,
            data=form.cleaned_data
        )
        return redirect(
            reverse(
                'microservices:microservices_freelancer_list',
                kwargs={'freelancer_id': self.request.user.freelancer_profile.id}
            )
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

class MicroServiceUpdateView(ProfileRequiredMixin, UpdateView):
    required_profile = 'freelancer'
    model = MicroService
    form_class = MicroServiceForm
    template_name = 'microservices/create_microservice.html'
    success_url = reverse_lazy('microservices:microservices_freelancer_list')
    service = MicroServiceService()
    
    def form_valid(self, form):
        self.service.update_microservice(microservice=self.get_object(), data=form.cleaned_data)
        return redirect(
            reverse(
                'microservices:microservices_freelancer_list',
                kwargs={'freelancer_id': self.request.user.freelancer_profile.id}
            )
        )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

class MicroServiceDeleteView(ProfileRequiredMixin, DeleteView):
    required_profile = 'freelancer'
    model = MicroService
    success_url = reverse_lazy('microservices:microservices_list')
    service = MicroServiceService()
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.service.delete_microservice(microservice=obj)
        return super().delete(request, *args, **kwargs)