from typing import Optional, Any, Dict
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Clase base para repositorios - Template Method Pattern"""
    
    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[Any]:
        pass
    
    @abstractmethod
    def create(self, data: dict) -> Any:
        pass
    
    @abstractmethod
    def update(self, instance, data: dict) -> Any:
        pass
    
    @abstractmethod
    def delete(self, instance) -> bool:
        pass
    
    def exists(self, **filters) -> bool:
        """Método común para verificar existencia"""
        return self.model.objects.filter(**filters).exists()