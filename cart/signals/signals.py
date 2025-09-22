from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from cart.models import CartItem, WishlistItem
from mentorship_session.models import MentorshipSession
from microservices.models import MicroService

def cleanup_cart_and_wishlist(instance):
    ct = ContentType.objects.get_for_model(instance)
    CartItem.objects.filter(content_type=ct, object_id=instance.id).delete()
    WishlistItem.objects.filter(content_type=ct, object_id=instance.id).delete()

@receiver(post_delete, sender=MentorshipSession)
def mentorship_session_deleted(sender, instance, **kwargs):
    cleanup_cart_and_wishlist(instance)

@receiver(post_delete, sender=MicroService)
def microservice_deleted(sender, instance, **kwargs):
    cleanup_cart_and_wishlist(instance)
