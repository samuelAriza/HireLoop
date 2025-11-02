from django.shortcuts import get_object_or_404, redirect
from core.mixins.views import ProfileRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from ..forms import MicroServiceForm
from ..models import MicroService, Category
from ..services.microservices_service import MicroServiceService
from ..services.image_service import MicroserviceImageService
from core.mixins.search import SearchFilterMixin
from core.models import FreelancerProfile
from cart.services.cart_service import CartService, WishlistService


class MicroServiceListView(SearchFilterMixin, ListView):
    model = MicroService
    template_name = "microservices/microservices_list.html"
    context_object_name = "microservices"
    service = MicroServiceService()
    search_fields = [
        "title",
        "description",
        "freelancer__user__email",
        "freelancer__user__username",
        "category__name",
    ]
    category_field = "category__name"
    price_field = "price"
    paginate_by = 12
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)

    def get_popular_categories(self):
        return Category.objects.values_list("name", flat=True).order_by("name")


class MicroServiceFreelancerListView(ProfileRequiredMixin, ListView):
    required_profile = "freelancer"
    model = MicroService
    template_name = "microservices/freelancer_microservices_list.html"
    context_object_name = "microservices"
    service = MicroServiceService()
    paginate_by = 12
    ordering = ["-created_at"]

    def get_queryset(self):
        freelancer = get_object_or_404(
            FreelancerProfile, pk=self.kwargs["freelancer_id"]
        )
        return self.service.list_freelancer_microservices(freelancer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        freelancer = get_object_or_404(
            FreelancerProfile, pk=self.kwargs["freelancer_id"]
        )
        context["freelancer"] = freelancer
        context["is_freelancer"] = hasattr(self.request.user, "freelancer_profile")
        return context


class MicroServiceDetailView(DetailView):
    model = MicroService
    template_name = "microservices/microservice_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        item = self.object

        if user.is_authenticated:
            cart_service = CartService()
            wishlist_service = WishlistService()

            cart_items = cart_service.list_cart(user)
            wishlist_items = wishlist_service.list_wishlist(user)
            ct = ContentType.objects.get_for_model(item)

            cart_item = next(
                (
                    ci
                    for ci in cart_items
                    if ci.content_type_id == ct.id and ci.object_id == item.id
                ),
                None,
            )
            wishlist_item = next(
                (
                    wi
                    for wi in wishlist_items
                    if wi.content_type_id == ct.id and wi.object_id == item.id
                ),
                None,
            )

            context.update(
                {
                    "cart_item": cart_item,
                    "wishlist_item": wishlist_item,
                    "in_cart": bool(cart_item),
                    "in_wishlist": bool(wishlist_item),
                    "is_owner": hasattr(user, "freelancer_profile") 
                                 and item.freelancer == user.freelancer_profile,
                }
            )
        else:
            context.update(
                {
                    "cart_item": None,
                    "wishlist_item": None,
                    "in_cart": False,
                    "in_wishlist": False,
                    "is_owner": False,
                }
            )

        return context


class MicroServiceCreateView(ProfileRequiredMixin, CreateView):
    required_profile = "freelancer"
    model = MicroService
    form_class = MicroServiceForm
    template_name = "microservices/create_microservice.html"
    success_url = reverse_lazy("microservices:microservices_freelancer_list")
    service = MicroServiceService()
    image_service = MicroserviceImageService()

    def form_valid(self, form):
        self.object = self.service.create_microservice(
            freelancer=self.request.user.freelancer_profile, data=form.cleaned_data
        )

        image_file = self.request.FILES.get("image")
        if image_file:
            image_path = self.image_service.upload_microservice_image(
                microservice_id=self.object.id, image_file=image_file
            )
            self.object.image_path = image_path
            self.object.save()

        return redirect(
            reverse(
                "microservices:microservices_freelancer_list",
                kwargs={"freelancer_id": self.request.user.freelancer_profile.id},
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context


class MicroServiceUpdateView(ProfileRequiredMixin, UpdateView):
    required_profile = "freelancer"
    model = MicroService
    form_class = MicroServiceForm
    template_name = "microservices/create_microservice.html"
    success_url = reverse_lazy("microservices:microservices_freelancer_list")
    service = MicroServiceService()
    image_service = MicroserviceImageService()

    def form_valid(self, form):
        microservice = self.get_object()
        self.service.update_microservice(
            microservice=microservice, data=form.cleaned_data
        )

        image_file = self.request.FILES.get("image")
        if image_file:
            if microservice.image_path:
                self.image_service.delete_microservice_image(microservice.image_path)

            image_path = self.image_service.upload_microservice_image(
                microservice.id, image_file
            )
            microservice.image_path = image_path
            microservice.save()

        return redirect(
            reverse(
                "microservices:microservices_freelancer_list",
                kwargs={"freelancer_id": self.request.user.freelancer_profile.id},
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context


class MicroServiceDeleteView(ProfileRequiredMixin, DeleteView):
    required_profile = "freelancer"
    model = MicroService
    success_url = reverse_lazy("microservices:microservices_list")
    service = MicroServiceService()
    image_service = MicroserviceImageService()

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.image_path:
            self.image_service.delete_microservice_image(obj.image_path)

        self.service.delete_microservice(microservice=obj)
        return super().delete(request, *args, **kwargs)
