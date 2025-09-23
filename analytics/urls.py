from django.urls import path
from .views import MarketDashboardView

app_name = "analytics"

urlpatterns = [
    path("dashboard/", MarketDashboardView.as_view(), name="market_dashboard"),
]