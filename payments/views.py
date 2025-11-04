import logging
from decimal import Decimal
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, Http404
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import stripe
from cart.models import CartItem
from .models import Payment

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


class CreateCheckoutSessionView(View):
    """
    Creates a Stripe Checkout Session for the user's cart.
    Validates cart contents and creates a pending Payment record.
    """

    def post(self, request, *args, **kwargs):
        user = request.user

        # Ensure user is authenticated
        if not user.is_authenticated:
            return JsonResponse({"error": _("Authentication required.")}, status=401)

        # Fetch cart items with related content objects
        cart_items = CartItem.objects.filter(user=user).select_related("content_type")

        if not cart_items.exists():
            return JsonResponse({"error": _("Your cart is empty.")}, status=400)

        line_items = []
        total_amount = Decimal("0.00")

        for item in cart_items:
            try:
                obj = item.content_object
                if not obj:
                    logger.warning(f"CartItem {item.id} has no content_object.")
                    continue

                price = Decimal(obj.get_price())
                quantity = item.quantity
                item_total = price * quantity
                total_amount += item_total

                line_items.append({
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(price * 100),  # Convert to cents
                        "product_data": {
                            "name": obj.get_title()[:255],
                            "description": (obj.get_description() or "")[:500],
                            "images": [obj.get_image_path()] if hasattr(obj, "get_image_path") and obj.get_image_path() else [],
                        },
                    },
                    "quantity": quantity,
                })
            except Exception as e:
                logger.error(f"Error processing cart item {item.id}: {e}")
                return JsonResponse({"error": _("Invalid item in cart.")}, status=400)

        if total_amount <= 0:
            return JsonResponse({"error": _("Cart total must be greater than zero.")}, status=400)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=request.build_absolute_uri(reverse("payments:success")),
                cancel_url=request.build_absolute_uri(reverse("payments:cancel")),
                client_reference_id=str(user.id),
                metadata={
                    "user_id": str(user.id),
                    "cart_items": ",".join(str(ci.id) for ci in cart_items),
                },
                expires_at=int((settings.SESSION_COOKIE_AGE or 1800) + __import__("time").time()),
            )

            # Create pending payment record
            Payment.objects.create(
                user=user,
                stripe_session_id=checkout_session.id,
                stripe_payment_intent=checkout_session.payment_intent,
                amount=total_amount,
                currency="usd",
                status=Payment.PaymentStatus.PENDING,
            )

            logger.info(f"Checkout session created for user {user.id}: {checkout_session.id}")
            return redirect(checkout_session.url, permanent=False)

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error for user {user.id}: {e}")
            return JsonResponse({"error": str(e.user_message or e)}, status=400)
        except Exception as e:
            logger.exception(f"Unexpected error creating checkout session for user {user.id}")
            return JsonResponse({"error": _("Payment processing failed. Please try again.")}, status=500)


class PaymentSuccessView(View):
    """
    Handles successful payment return.
    Clears cart, updates payment status, and shows success page.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        session_id = request.GET.get("session_id")

        if not user.is_authenticated:
            messages.error(request, _("You must be logged in to view this page."))
            return redirect("core:login")

        # Retrieve the checkout session to verify
        if session_id:
            try:
                checkout_session = stripe.checkout.Session.retrieve(
                    session_id,
                    expand=["payment_intent"],
                )
                if checkout_session.payment_status != "paid":
                    messages.error(request, _("Payment was not completed."))
                    return redirect("cart:cart_detail")
            except stripe.error.StripeError as e:
                logger.error(f"Failed to retrieve Stripe session {session_id}: {e}")
                messages.error(request, _("Could not verify payment. Please contact support."))
                return redirect("cart:cart_detail")
        else:
            # Fallback: find latest pending payment
            payment = Payment.objects.filter(
                user=user, status=Payment.PaymentStatus.PENDING
            ).order_by("-created_at").first()
            if not payment:
                messages.info(request, _("No pending payment found."))
                return redirect("core:home")

            try:
                checkout_session = stripe.checkout.Session.retrieve(
                    payment.stripe_session_id,
                    expand=["payment_intent"],
                )
            except stripe.error.StripeError:
                checkout_session = None

        # Clear the user's cart
        deleted_count, _ = CartItem.objects.filter(user=user).delete()
        if deleted_count > 0:
            logger.info(f"Cleared {deleted_count} cart items for user {user.id}")

        # Update payment status if still pending
        payment = Payment.objects.filter(
            user=user, status=Payment.PaymentStatus.PENDING
        ).order_by("-created_at").first()

        if payment and (not checkout_session or checkout_session.payment_status == "paid"):
            payment.status = Payment.PaymentStatus.SUCCEEDED
            if checkout_session and checkout_session.payment_intent:
                payment.stripe_payment_intent = checkout_session.payment_intent.id
            payment.save()
            messages.success(request, _("Payment successful! Your order is confirmed."))

        return render(request, "payments/success.html")


class PaymentCancelView(View):
    """
    Handles canceled payment return.
    Shows cancellation message and preserves cart.
    """

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("core:login")

        # Optional: mark pending payment as canceled
        payment = Payment.objects.filter(
            user=user, status=Payment.PaymentStatus.PENDING
        ).order_by("-created_at").first()

        if payment:
            payment.status = Payment.PaymentStatus.CANCELED
            payment.save()

        messages.warning(request, _("Payment was canceled. Your cart has been preserved."))
        return render(request, "payments/cancel.html")