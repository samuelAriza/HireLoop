from django.views import View
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.conf import settings
import stripe
from cart.models import CartItem
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return JsonResponse({"error": "Cart is empty"}, status=400)

        line_items = []
        total_amount = 0

        for item in cart_items:
            price = item.content_object.get_price()
            total_amount += price * item.quantity
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(price * 100),
                    "product_data": {
                        "name": item.content_object.get_title(),
                    },
                },
                "quantity": item.quantity,
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=request.build_absolute_uri("/payments/success/"),
                cancel_url=request.build_absolute_uri("/payments/cancel/"),
            )

            # Guardamos un registro "pendiente" en nuestra DB
            Payment.objects.create(
                user=user,
                stripe_session_id=checkout_session.id,
                amount=total_amount,
                currency="usd",
                status="pending",
            )

            return redirect(checkout_session.url)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class PaymentSuccessView(View):
    def get(self, request):
        user = request.user

        # Vaciar carrito
        CartItem.objects.filter(user=user).delete()

        # Actualizar pago a 'succeeded'
        payment = Payment.objects.filter(user=user, status="pending").last()
        if payment:
            payment.status = "succeeded"
            payment.save()

        # Renderizar template de pago exitoso
        return render(request, "payments/success.html")