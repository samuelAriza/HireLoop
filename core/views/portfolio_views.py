from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from ..forms.item_portfolio_forms import ItemPortfolioForm
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
        service.add_item(
            freelancer=freelancer_profile,
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            url_demo=form.cleaned_data.get("url_demo"),
        )
        return redirect(self.success_url)
