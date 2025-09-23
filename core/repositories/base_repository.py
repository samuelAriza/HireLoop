from abc import ABC, abstractmethod
from typing import Optional, Any

"""
ABC = Abstract Base Class
The BaseRepository class defines a contract for repository implementations.
This allows for different data storage mechanisms (e.g., SQL, NoSQL, in-memory)
to be used interchangeably without changing the business logic that depends on them.
This adheres to the Dependency Inversion Principle (DIP) by depending on abstractions
rather than concrete implementations.
"""


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
