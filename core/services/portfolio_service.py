import uuid
from typing import List, Optional, Dict, Any
from core.models import ItemPortfolio, FreelancerProfile
from core.repositories.portfolio_repository import PortfolioRepository

class PortfolioService:
    """
    Portfolio Service following Single Responsibility Principle.
    """
    
    def __init__(self, repository: Optional[PortfolioRepository] = None):
        #DIP injection of repository
        self.repository = repository or PortfolioRepository()
        
    def add_item(self, freelancer: FreelancerProfile, title: str, description: str, url_demo: Optional[str] = None) -> ItemPortfolio:
        '''
        Add a new portfolio item for a freelancer
        '''
        return self.repository.create(freelancer=freelancer, title=title, description=description, url_demo=url_demo)
    
    def list_items(self, freelancer_profile):
        """List all portfolio items for a freelancer."""
        return self.repository.list_by_freelancer(freelancer_profile)

    def get_item(self, item_id) -> Optional[ItemPortfolio]:
        """Get a specific portfolio item by ID."""
        print(f"DEBUG PortfolioService.get_item - ID: {item_id}, type: {type(item_id)}")
        if isinstance(item_id, str):
            try:
                item_id = uuid.UUID(item_id)
            except ValueError:
                print(f"DEBUG PortfolioService.get_item - Invalid UUID: {item_id}")
                return None
        
        result = self.repository.get_by_id(item_id)
        print(f"DEBUG PortfolioService.get_item - Result: {result}")
        return result
    
    def update_item(self, item_id: uuid.UUID, **kwargs) -> Optional[ItemPortfolio]:
        """Update a portfolio item by ID."""
        item = self.repository.get_by_id(item_id)
        if not item:
            return None
        return self.repository.update(item, **kwargs)
    
    def remove_item(self, item_id: uuid.UUID) -> bool:
        """Remove a portfolio item by ID."""
        item = self.repository.get_by_id(item_id)
        if not item:
            return False
        return self.repository.delete(item)
    
    def update_portfolio(self, portfolio_instance, update_data: Dict[str, Any]) -> bool:
        """Update an existing portfolio item instance."""
        print("-"*100)
        try:
            for field, value in update_data.items():
                if hasattr(portfolio_instance, field) and value is not None:
                    setattr(portfolio_instance, field, value)
            
            portfolio_instance.save()
            return True
            
        except Exception as e:
            print(f"Error updating portfolio: {e}")
            return False

    def delete_portfolio(self, portfolio_instance) -> bool:
        """Delete a portfolio item instance."""
        try:
            portfolio_instance.delete()
            return True
            
        except Exception as e:
            print(f"Error deleting portfolio: {e}")
            return False