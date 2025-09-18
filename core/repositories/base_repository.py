from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class BaseRepository(ABC):
    """
    Base repository interface following Dependency Inversion Principle.
    """
    
    @abstractmethod
    def create(self, **kwargs) -> Any:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: Any) -> Optional[Any]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def update(self, entity: Any, **kwargs) -> Any:
        """Update an entity."""
        pass
    
    @abstractmethod
    def delete(self, entity: Any) -> bool:
        """Delete an entity."""
        pass