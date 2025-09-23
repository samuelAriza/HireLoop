from django.views.generic import TemplateView

class MarketDashboardView(TemplateView):
    template_name = "analytics/market_dashboard.html"