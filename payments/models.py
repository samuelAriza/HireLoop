import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Payment(models.Model):
    """
    Represents a payment transaction processed via Stripe.
    Tracks payment status, amount, and Stripe identifiers.
    """

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        SUCCEEDED = "succeeded", _("Succeeded")
        FAILED = "failed", _("Failed")
        CANCELED = "canceled", _("Canceled")
        REQUIRES_PAYMENT_METHOD = "requires_payment_method", _("Requires Payment Method")
        REQUIRES_CONFIRMATION = "requires_confirmation", _("Requires Confirmation")
        REQUIRES_ACTION = "requires_action", _("Requires Action")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("User"),
        help_text=_("The user who initiated this payment.")
    )
    stripe_session_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Stripe Checkout Session ID"),
        help_text=_("Unique identifier for the Stripe Checkout Session.")
    )
    stripe_payment_intent = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Stripe Payment Intent ID"),
        help_text=_("Payment Intent ID if using Payment Intents API.")
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name=_("Amount"),
        help_text=_("Total amount in the currency's smallest unit (e.g., cents for USD).")
    )
    currency = models.CharField(
        max_length=10,
        default="usd",
        verbose_name=_("Currency"),
        help_text=_("ISO 4217 currency code (e.g., usd, eur).")
    )
    status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name=_("Status"),
        help_text=_("Current status of the payment.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("When the payment record was created.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Last time the payment status was updated.")
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["stripe_session_id"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return _(
            "Payment {id} - {status} (${amount} {currency})"
        ).format(
            id=str(self.id)[:8],
            status=self.get_status_display(),
            amount=self.amount,
            currency=self.currency.upper(),
        )

    def is_successful(self) -> bool:
        """Check if payment was successfully completed."""
        return self.status == self.PaymentStatus.SUCCEEDED

    def is_canceled(self) -> bool:
        """Check if payment was canceled."""
        return self.status == self.PaymentStatus.CANCELED

    def is_failed(self) -> bool:
        """Check if payment failed."""
        return self.status == self.PaymentStatus.FAILED