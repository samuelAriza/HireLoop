from django.http import HttpResponse
from django.urls import path
from .views import CreateCheckoutSessionView, PaymentSuccessView

app_name = "payments"

urlpatterns = [
    path("create-checkout-session/", CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path("success/", PaymentSuccessView.as_view(), name="payment-success"),
    path("cancel/", lambda request: HttpResponse("Pago cancelado."), name="payment-cancel"),
]
