from django.test import TestCase
from unittest.mock import Mock, patch
import uuid
from core.services.portfolio_service import PortfolioService
from core.models import ItemPortfolio, FreelancerProfile


class PortfolioServiceTest(TestCase):
    """Unit tests for PortfolioService business logic"""
    
    def setUp(self):
        """Setup mocked repository and service"""
        self.mock_repository = Mock()
        self.service = PortfolioService(repository=self.mock_repository)
        
    def test_update_portfolio_modifies_fields_correctly(self):
        """Test that update_portfolio modifies only provided fields"""
        # Arrange
        mock_portfolio = Mock(spec=ItemPortfolio)
        mock_portfolio.title = "Old Title"
        mock_portfolio.description = "Old Description"
        mock_portfolio.url_demo = "http://old-url.com"
        mock_portfolio.save = Mock()
        
        update_data = {
            'title': 'New Title',
            'description': 'New Description'
        }
        
        # Act
        result = self.service.update_portfolio(mock_portfolio, update_data)
        
        # Assert
        self.assertEqual(mock_portfolio.title, 'New Title')
        self.assertEqual(mock_portfolio.description, 'New Description')
        self.assertEqual(mock_portfolio.url_demo, 'http://old-url.com')  # unchanged
        mock_portfolio.save.assert_called_once()
        self.assertTrue(result)
        
    def test_update_portfolio_handles_exception(self):
        """Test that update_portfolio handles exceptions gracefully"""
        # Arrange
        mock_portfolio = Mock(spec=ItemPortfolio)
        mock_portfolio.save.side_effect = Exception("Database error")
        
        update_data = {'title': 'New Title'}
        
        # Act
        with patch('builtins.print') as mock_print:
            result = self.service.update_portfolio(mock_portfolio, update_data)
        
        # Assert
        self.assertFalse(result)
        mock_print.assert_called()
        
    def test_delete_portfolio_returns_true_on_success(self):
        """Test that delete_portfolio returns True when deletion succeeds"""
        # Arrange
        mock_portfolio = Mock(spec=ItemPortfolio)
        mock_portfolio.delete = Mock()
        
        # Act
        result = self.service.delete_portfolio(mock_portfolio)
        
        # Assert
        mock_portfolio.delete.assert_called_once()
        self.assertTrue(result)
        
    def test_delete_portfolio_returns_false_on_exception(self):
        """Test that delete_portfolio returns False when exception occurs"""
        # Arrange
        mock_portfolio = Mock(spec=ItemPortfolio)
        mock_portfolio.delete.side_effect = Exception("Cannot delete")
        
        # Act
        with patch('builtins.print') as mock_print:
            result = self.service.delete_portfolio(mock_portfolio)
        
        # Assert
        self.assertFalse(result)
        mock_print.assert_called()