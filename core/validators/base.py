from typing import Protocol
from abc import ABC, abstractmethod

class ValidatorProtocol(Protocol):
    """Protocol para validadores - ISP"""
    def validate(self, data: dict) -> None: ...

class BaseValidator(ABC):
    """Clase base para validadores"""
    
    @abstractmethod
    def validate(self, data: dict) -> None:
        pass