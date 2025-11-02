from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from core.mixins.views import ProfileRequiredMixin
from core.mixins.search import SearchFilterMixin
from core.models import FreelancerProfile
from ..forms import MicroServiceForm
from ..models import MicroService, Category
from ..services.microservices_service import MicroServiceService
from ..services.image_service import MicroserviceImageService
from cart.services.cart_service import CartService, WishlistService


microservice_service = MicroServiceService()
image_service = MicroserviceImageService()


class MicroServiceListView(SearchFilterMixin, ListView):
    model = MicroService
    template_name = "microservices/microservices_list.html"
    context_object_name = "microservices"
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
        """Return only active microservices."""
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optional: Add popular categories if needed in template
        context["popular_categories"] = Category.objects.values_list("name", flat=True).order_by("name")
        return context


class MicroServiceFreelancerListView(ProfileRequiredMixin, ListView):
    required_profile = "freelancer"
    model = MicroService
    template_name = "microservices/freelancer_microservices_list.html"
    context_object_name = "microservices"
    paginate_by = 12
    ordering = ["-created_at"]

    def get_queryset(self):
        """List all microservices for the specified freelancer."""
        freelancer = get_object_or_404(FreelancerProfile, pk=self.kwargs["freelancer_id"])
        return microservice_service.list_freelancer_microservices(freelancer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        freelancer = get_object_or_404(FreelancerProfile, pk=self.kwargs["freelancer_id"])
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

        is_owner = (
            user.is_authenticated
            and hasattr(user, "freelancer_profile")
            and item.freelancer == user.freelancer_profile
        )
        context["is_owner"] = is_owner

        if user.is_authenticated:
            cart_service = CartService()
            wishlist_service = WishlistService()

            cart_items = cart_service.list_cart(user)
            wishlist_items = wishlist_service.list_wishlist(user)
            ct = ContentType.objects.get_for_model(item)

            cart_item = next(
                (ci for ci in cart_items if ci.content_type_id == ct.id and ci.object_id == item.id),
                None,
            )
            wishlist_item = next(
                (wi for wi in wishlist_items if wi.content_type_id == ct.id and wi.object_id == item.id),
                None,
            )

            context.update(
                {
                    "cart_item": cart_item,
                    "wishlist_item": wishlist_item,
                    "in_cart": bool(cart_item),
                    "in_wishlist": bool(wishlist_item),
                }
            )
        else:
            context.update(
                {
                    "cart_item": None,
                    "wishlist_item": None,
                    "in_cart": False,
                    "in_wishlist": False,
                }
            )

        return context


class MicroServiceCreateView(ProfileRequiredMixin, CreateView):
    required_profile = "freelancer"
    model = MicroService
    form_class = MicroServiceForm
    template_name = "microservices/create_microservice.html"

    def form_valid(self, form):
        """Create microservice and handle image upload."""
        freelancer = self.request.user.freelancer_profile
        microservice = microservice_service.create_microservice(
            freelancer=freelancer, data=form.cleaned_data
        )

        image_file = self.request.FILES.get("image")
        if image_file:
            image_path = image_service.upload_microservice_image(
                microservice_id=microservice.id, image_file=image_file
            )
            microservice.image_path = image_path
            microservice.save()

        return redirect(
            reverse(
                "microservices:microservices_freelancer_list",
                kwargs={"freelancer_id": freelancer.id},
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

    def get_queryset(self):
        """Ensure only owned microservices can be updated."""
        return super().get_queryset().filter(freelancer=self.request.user.freelancer_profile)

    def form_valid(self, form):
        """Update microservice and handle image replacement."""
        microservice = self.get_object()
        microservice_service.update_microservice(microservice=microservice, data=form.cleaned_data)

        image_file = self.request.FILES.get("image")
        if image_file:
            if microservice.image_path:
                image_service.delete_microservice_image(microservice.image_path)

            image_path = image_service.upload_microservice_image(
                microservice_id=microservice.id, image_file=image_file
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
    template_name = "microservices/microservice_confirm_delete.html"

    def get_queryset(self):
        """Ensure only owned microservices can be deleted."""
        return super().get_queryset().filter(freelancer=self.request.user.freelancer_profile)

    def delete(self, request, *args, **kwargs):
        """Delete microservice and associated image."""
        microservice = self.get_object()

        if microservice.image_path:
            image_service.delete_microservice_image(microservice.image_path)

        microservice_service.delete_microservice(microservice=microservice)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """Redirect to freelancer's microservices list."""
        return reverse(
            "microservices:microservices_freelancer_list",
            kwargs={"freelancer_id": self.request.user.freelancer_profile.id},
        )