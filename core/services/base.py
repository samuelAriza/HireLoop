from typing import Optional, Protocol, Dict, Any
from abc import ABC, abstractmethod
from django.db import transaction
import logging

# ============================================================================
# PROTOCOLS (DIP)
# ============================================================================

class RepositoryProtocol(Protocol):
    """Protocol base para repositorios"""
    def get_by_id(self, id: Any) -> Optional[Any]: ...
    def create(self, data: dict) -> Any: ...
    def update(self, instance, data: dict) -> Any: ...
    def delete(self, instance) -> bool: ...

class ValidatorProtocol(Protocol):
    """Protocol base para validadores"""
    def validate(self, data: dict) -> None: ...

class NotificationServiceProtocol(Protocol):
    """Protocol para notificaciones"""
    def notify(self, event_type: str, data: dict) -> None: ...

# ============================================================================
# BASE CLASSES
# ============================================================================

class BaseService(ABC):
    """Clase base para todos los servicios - Template Method Pattern"""
    
    def __init__(self, logger_name: Optional[str] = None):
        self.logger = logging.getLogger(logger_name or self.__class__.__name__)
    
    def execute_with_transaction(self, operation, *args, **kwargs):
        """Template method para operaciones transaccionales"""
        try:
            with transaction.atomic():
                return operation(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error in {operation.__name__}: {str(e)}")
            raise