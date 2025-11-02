from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import View
from ..forms.item_portfolio_forms import ItemPortfolioForm, PortfolioImageForm
from ..models import ItemPortfolio, FreelancerProfile
from ..services.portfolio_service import PortfolioService


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = ItemPortfolio
    form_class = ItemPortfolioForm
    template_name = "core/create_portfolio.html"
    success_url = reverse_lazy("core:profile_detail")

    def form_valid(self, form):
        freelancer_profile = get_object_or_404(
            FreelancerProfile, user=self.request.user
        )
        service = PortfolioService()

        try:
            service.add_item(
                freelancer=freelancer_profile,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                url_demo=form.cleaned_data.get("url_demo"),
                image=form.cleaned_data.get("image"),
            )
            messages.success(self.request, "Portfolio item created successfully!")
        except ValueError as e:
            messages.error(self.request, f"Error creating portfolio item: {str(e)}")
            return self.form_invalid(form)

        return redirect(self.success_url)


class PortfolioImageUpdateView(LoginRequiredMixin, View):
    """View for updating portfolio item image following DIP."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolio_service = PortfolioService()

    def post(self, request, portfolio_id, *args, **kwargs):
        """Handle portfolio image update."""
        # Get portfolio item and verify ownership
        portfolio_item = get_object_or_404(ItemPortfolio, id=portfolio_id)

        if not hasattr(request.user, "freelancer_profile"):
            messages.error(request, "You must have a freelancer profile.")
            return redirect("core:profile_detail")

        if portfolio_item.freelancer != request.user.freelancer_profile:
            messages.error(request, "You don't have permission to edit this item.")
            return redirect("core:profile_detail")

        form = PortfolioImageForm(request.POST, request.FILES, instance=portfolio_item)

        if form.is_valid():
            image_file = form.cleaned_data.get("image")
            if image_file:
                success = self.portfolio_service.update_portfolio_image(
                    portfolio_item, image_file
                )

                if success:
                    messages.success(
                        request, "Portfolio item image updated successfully!"
                    )
                else:
                    messages.error(request, "Failed to update portfolio item image.")
            else:
                messages.error(request, "No image file provided.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return redirect("core:profile_detail")


class PortfolioImageDeleteView(LoginRequiredMixin, View):
    """View for deleting portfolio item image."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolio_service = PortfolioService()

    def post(self, request, portfolio_id, *args, **kwargs):
        """Handle portfolio image deletion."""
        # Get portfolio item and verify ownership
        portfolio_item = get_object_or_404(ItemPortfolio, id=portfolio_id)

        if not hasattr(request.user, "freelancer_profile"):
            messages.error(request, "You must have a freelancer profile.")
            return redirect("core:profile_detail")

        if portfolio_item.freelancer != request.user.freelancer_profile:
            messages.error(request, "You don't have permission to edit this item.")
            return redirect("core:profile_detail")

        success = self.portfolio_service.delete_portfolio_image(portfolio_item)

        if success:
            messages.success(request, "Portfolio item image deleted successfully!")
        else:
            messages.error(request, "Failed to delete portfolio item image.")

        return redirect("core:profile_detail")

