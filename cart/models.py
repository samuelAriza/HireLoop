import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items",
        verbose_name=_("user")
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("content type"))
    object_id = models.UUIDField(verbose_name=_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_("added at"))

    class Meta:
        unique_together = ("user", "content_type", "object_id")
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def __str__(self):
        return _("%(content_object)s (x%(quantity)d)") % {
            "content_object": self.content_object,
            "quantity": self.quantity
        }

    def items_quantity(self):
        return self.quantity

    items_quantity.short_description = _("items quantity")


class WishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
        verbose_name=_("user")
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("content type"))
    object_id = models.UUIDField(verbose_name=_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_("added at"))

    class Meta:
        unique_together = ("user", "content_type", "object_id")
        verbose_name = _("Wishlist Item")
        verbose_name_plural = _("Wishlist Items")

    def __str__(self):
        return _("%(content_object)s") % {"content_object": self.content_object}