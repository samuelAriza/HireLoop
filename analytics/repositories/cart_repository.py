from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from typing import List, Dict, Any
from cart.models import CartItem
from .base_repository import BaseRepository
from microservices.models import MicroService
from mentorship_session.models import MentorshipSession
class CartRepository(BaseRepository):
    def get_all(self) -> QuerySet:
        return CartItem.objects.all()
    
    def get_most_added_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        microservice_content_type = ContentType.objects.get_for_model(MicroService)
        microservices_in_cart = (
            CartItem.objects
            .filter(content_type=microservice_content_type)
            .values('object_id', 'content_type')
            .annotate(
                times_added=Count('id'),
                total_quantity=Count('quantity')
            )
            .order_by('-times_added')[:limit]
        )
        
        mentorship_content_type = ContentType.objects.get_for_model(MentorshipSession)
        mentorships_in_cart = (
            CartItem.objects
            .filter(content_type=mentorship_content_type)
            .values('object_id', 'content_type')
            .annotate(
                times_added=Count('id'),
                total_quantity=Count('quantity')
            )
            .order_by('-times_added')[:limit]
        )
        
        return {
            'microservices': list(microservices_in_cart),
            'mentorships': list(mentorships_in_cart)
        }