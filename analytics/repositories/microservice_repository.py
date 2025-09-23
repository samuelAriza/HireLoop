from django.db.models import Count, Avg, Q, Min, Max
from django.db.models.query import QuerySet
from typing import List, Dict, Any
from microservices.models import MicroService, Category
from .base_repository import BaseRepository

class MicroServiceRepository(BaseRepository):
    def get_all(self) -> QuerySet:
        return MicroService.objects.filter(is_active=True)
    
    def get_distribution_by_category(self) -> List[Dict[str, Any]]:
        return (
            Category.objects
            .annotate(
                total_services=Count('microservices', filter=Q(microservices__is_active=True)),
                percentage=Count('microservices', filter=Q(microservices__is_active=True)) * 100.0 / 
                          MicroService.objects.filter(is_active=True).count()
            )
            .values('name', 'total_services', 'percentage')
            .order_by('-total_services')
        )
    
    def get_price_distribution_by_category(self) -> List[Dict[str, Any]]:
        return (
            Category.objects
            .filter(microservices__is_active=True)
            .annotate(
                avg_price=Avg('microservices__price'),
                min_price=Min('microservices__price'),
                max_price=Max('microservices__price'),
                service_count=Count('microservices', filter=Q(microservices__is_active=True))
            )
            .values('name', 'avg_price', 'min_price', 'max_price', 'service_count')
            .order_by('-avg_price')
        )
    
    def get_delivery_time_stats(self) -> Dict[str, Any]:
        general_stats = (
            MicroService.objects
            .filter(is_active=True)
            .aggregate(
                avg_delivery_time=Avg('delivery_time'),
                min_delivery_time=Min('delivery_time'),
                max_delivery_time=Max('delivery_time')
            )
        )

        category_stats = (
            Category.objects
            .filter(microservices__is_active=True)
            .annotate(
                avg_delivery_time=Avg('microservices__delivery_time'),
                service_count=Count('microservices', filter=Q(microservices__is_active=True))
            )
            .values('name', 'avg_delivery_time', 'service_count')
            .order_by('avg_delivery_time')
        )
        
        return {
            'general': general_stats,
            'by_category': list(category_stats)
        }
    
    def get_most_active_freelancers(self, limit: int = 10) -> List[Dict[str, Any]]:
        from django.db.models import Count
        from core.models import FreelancerProfile
        
        return (
            FreelancerProfile.objects
            .annotate(
                active_services_count=Count('microservices', filter=Q(microservices__is_active=True)),
                total_services_count=Count('microservices')
            )
            .filter(active_services_count__gt=0)
            .values(
                'id',  # Solo el ID para anonimidad
                'active_services_count',
                'total_services_count'
            )
            .order_by('-active_services_count')[:limit]
        )