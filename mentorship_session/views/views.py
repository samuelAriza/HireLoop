from django.db.models import F, ExpressionWrapper, DecimalField
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
from core.mixins.views import ProfileRequiredMixin
from core.mixins.search import SearchFilterMixin
from core.models import FreelancerProfile
from ..models import MentorshipSession
from ..forms.mentorship_form import (
    MentorshipSessionCreateForm,
    MentorshipSessionUpdateForm,
)
from ..repositories.mentorship_repository import MentorshipRepository
from ..services.mentorship_service import MentorshipService
from ..services.image_service import MentorshipImageService
from cart.services.cart_service import CartService, WishlistService

mentorship_service = MentorshipService(repository=MentorshipRepository())


class MentorshipSessionListView(SearchFilterMixin, ListView):
    model = MentorshipSession
    template_name = "mentorship_session/mentorship_sessions_list.html"
    context_object_name = "sessions"
    search_fields = ["topic", "mentor__user__email", "mentee__user__email"]
    category_field = None
    price_field = "price"
    paginate_by = 12
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            price=ExpressionWrapper(
                F("duration_minutes") * MentorshipSession.PRICE_PER_MINUTE,
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session_content_type_id"] = ContentType.objects.get_for_model(
            MentorshipSession
        ).id
        return context


class MentorshipSessionFreelancerListView(ProfileRequiredMixin, ListView):
    required_profile = "freelancer"
    model = MentorshipSession
    template_name = "mentorship_session/freelancer_mentorship_session.html"
    context_object_name = "sessions"
    paginate_by = 12
    ordering = ["-created_at"]

    def get_queryset(self):
        freelancer = get_object_or_404(
            FreelancerProfile, pk=self.kwargs["freelancer_id"]
        )
        return mentorship_service.list_mentor_sessions(mentor_id=freelancer.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        freelancer = get_object_or_404(
            FreelancerProfile, pk=self.kwargs["freelancer_id"]
        )
        context["freelancer"] = freelancer
        context["is_freelancer"] = hasattr(self.request.user, "freelancer_profile")
        return context


class MentorshipSessionDetailView(DetailView):
    model = MentorshipSession
    template_name = "mentorship_session/mentorship_session_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        item = self.object
        context["is_owner"] = item.mentor.user == user

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


class MentorshipSessionCreateView(ProfileRequiredMixin, CreateView):
    required_profile = "freelancer"
    model = MentorshipSession
    form_class = MentorshipSessionCreateForm
    template_name = "mentorship_session/create_mentorship_session.html"
    img_service = MentorshipImageService()

    def form_valid(self, form):
        freelancer = self.request.user.freelancer_profile
        session = mentorship_service.create_session(
            topic=form.cleaned_data["topic"],
            start_time=form.cleaned_data["start_time"],
            duration_minutes=form.cleaned_data["duration_minutes"],
            mentor_id=freelancer.id,
        )

        self.object = session

        image_file = self.request.FILES.get("image")
        if image_file:
            path = self.img_service.upload_mentorship_image(
                mentorship_id=session.id, image_file=image_file
            )
            self.object.image_path = path
            self.object.save()

        return redirect(
            reverse(
                "mentorship_session:sessions_freelancer_list",
                kwargs={"freelancer_id": freelancer.id},
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context


class MentorshipSessionUpdateView(ProfileRequiredMixin, UpdateView):
    required_profile = "freelancer"
    model = MentorshipSession
    form_class = MentorshipSessionUpdateForm
    template_name = "mentorship_session/create_mentorship_session.html"

    def form_valid(self, form):
        session = self.get_object()
        mentorship_service.update_session(
            session_id=session.id,
            topic=form.cleaned_data["topic"],
            start_time=form.cleaned_data["start_time"],
            duration_minutes=form.cleaned_data["duration_minutes"],
            mentor_id=session.mentor.id,
            status=form.cleaned_data["status"],
        )
        image_file = self.request.FILES.get("image")
        if image_file:
            if session.image_path:
                self.img_service.delete_mentorship_image(session.image_path)

            path = self.img_service.upload_mentorship_image(
                mentorship_id=session.id, image_file=image_file
            )
            session.image_path = path

        session.save()
        return redirect(
            reverse(
                "mentorship_session:sessions_freelancer_list",
                kwargs={"freelancer_id": self.request.user.freelancer_profile.id},
            )
        )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context


class MentorshipSessionDeleteView(ProfileRequiredMixin, DeleteView):
    required_profile = "freelancer"
    model = MentorshipSession
    template_name = "mentorship_session/mentorship_session_confirm_delete.html"
    success_url = reverse_lazy("mentorship_session:session_list")

    def delete(self, request, *args, **kwargs):
        session = self.get_object()
        mentorship_service.delete_session(session.id)
        return super().delete(request, *args, **kwargs)
