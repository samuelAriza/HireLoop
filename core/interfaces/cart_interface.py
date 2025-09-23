from abc import ABC, abstractmethod


class PurchasableInterface(ABC):
    """Interface for purchasable items following DIP."""

    @abstractmethod
    def get_price(self) -> float:
        """Return the price of the item."""
        pass

    @abstractmethod
    def get_title(self) -> str:
        """Return the title of the item."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Return the description of the item."""
        pass

    @abstractmethod
    def get_type(self) -> str:
        """Return the type of the item."""
        pass
