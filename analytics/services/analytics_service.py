from typing import Dict, List, Any
from abc import ABC, abstractmethod

class AnalyticsServiceInterface(ABC):
    @abstractmethod
    def get_dashboard_data(self) -> Dict[str, Any]:
        pass

class MarketAnalyticsService(AnalyticsServiceInterface):
    def __init__(self, microservice_repository, cart_repository):
        self.microservice_repository = microservice_repository
        self.cart_repository = cart_repository
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        return {
            'category_distribution': self._get_category_distribution(),
            'price_analysis': self._get_price_analysis(),
            'delivery_time_stats': self._get_delivery_time_stats(),
            'top_freelancers': self._get_top_freelancers(),
            'popular_products': self._get_popular_products()
        }
    
    def _get_category_distribution(self) -> Dict[str, Any]:
        raw_data = self.microservice_repository.get_distribution_by_category()
        processed_data = []
        for item in raw_data:
            if item['total_services'] > 0:
                processed_data.append({
                    'category': item['name'],
                    'count': item['total_services'],
                    'percentage': round(item['percentage'], 2)
                })
        
        return {
            'data': processed_data,
            'chart_type': 'pie',
            'title': 'Distribución de Microservicios por Categoría'
        }
    
    def _get_price_analysis(self) -> Dict[str, Any]:
        raw_data = self.microservice_repository.get_price_distribution_by_category()
        
        processed_data = []
        for item in raw_data:
            processed_data.append({
                'category': item['name'],
                'avg_price': float(item['avg_price']) if item['avg_price'] else 0,
                'min_price': float(item['min_price']) if item['min_price'] else 0,
                'max_price': float(item['max_price']) if item['max_price'] else 0,
                'service_count': item['service_count']
            })
        
        return {
            'data': processed_data,
            'chart_type': 'box',
            'title': 'Distribución de Precios por Categoría'
        }
    
    def _get_delivery_time_stats(self) -> Dict[str, Any]:
        """Procesa estadísticas de tiempo de entrega"""
        raw_data = self.microservice_repository.get_delivery_time_stats()
        
        return {
            'general': {
                'avg_days': round(raw_data['general']['avg_delivery_time'] or 0, 1),
                'min_days': raw_data['general']['min_delivery_time'] or 0,
                'max_days': raw_data['general']['max_delivery_time'] or 0
            },
            'by_category': raw_data['by_category'],
            'chart_type': 'bar',
            'title': 'Tiempo de Entrega Promedio'
        }
    
    def _get_top_freelancers(self) -> Dict[str, Any]:
        raw_data = self.microservice_repository.get_most_active_freelancers()
        
        # Anonimizar datos
        processed_data = []
        for i, freelancer in enumerate(raw_data, 1):
            processed_data.append({
                'rank': i,
                'freelancer_id': f"Freelancer #{i}",  # Anonimizado
                'active_services': freelancer['active_services_count'],
                'total_services': freelancer['total_services_count']
            })
        
        return {
            'data': processed_data,
            'chart_type': 'bar',
            'title': 'Top 10 Freelancers Más Activos'
        }
    
    def _get_popular_products(self) -> Dict[str, Any]:
        raw_data = self.cart_repository.get_most_added_products()
        
        return {
            'microservices': raw_data['microservices'],
            'mentorships': raw_data['mentorships'],
            'chart_type': 'horizontal_bar',
            'title': 'Productos Más Agregados al Carrito'
        }
