from abc import ABC, abstractmethod
from django.db.models import QuerySet

class BaseRepository(ABC):
    @abstractmethod
    def get_all(self) -> QuerySet:
        pass