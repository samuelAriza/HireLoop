from django.test import TestCase
from unittest.mock import Mock, patch
from decimal import Decimal
from microservices.services.microservices_service import MicroServiceService
from microservices.models import MicroService
from core.models import FreelancerProfile

class MicroServiceServiceTest(TestCase):
    """Unit tests for MicroServiceService business logic"""
    
    def setUp(self):
        """Setup mocked repository and service"""
        self.mock_repository = Mock()
        self.service = MicroServiceService(repository=self.mock_repository)
        
        # Mock freelancer
        self.mock_freelancer = Mock(spec=FreelancerProfile)
        self.mock_freelancer.id = "123e4567-e89b-12d3-a456-426614174000"
        
    def test_create_microservice_calls_repository_with_correct_data(self):
        """Test that create_microservice passes correct data to repository"""
        # Arrange
        test_data = {
            'title': 'Test Service',
            'description': 'Test Description',
            'price': Decimal('99.99'),
            'delivery_time': 5
        }
        expected_microservice = Mock(spec=MicroService)
        self.mock_repository.create.return_value = expected_microservice
        
        # Act
        result = self.service.create_microservice(
            freelancer=self.mock_freelancer,
            data=test_data
        )
        
        # Assert
        self.mock_repository.create.assert_called_once_with(
            freelancer=self.mock_freelancer,
            **test_data
        )
        self.assertEqual(result, expected_microservice)
        
    def test_deactivate_microservice_calls_repository_deactivate(self):
        """Test that deactivate_microservice delegates to repository"""
        # Arrange
        mock_microservice = Mock(spec=MicroService)
        mock_microservice.is_active = True
        deactivated_microservice = Mock(spec=MicroService)
        deactivated_microservice.is_active = False
        self.mock_repository.deactivate.return_value = deactivated_microservice
        
        # Act
        result = self.service.deactivate_microservice(mock_microservice)
        
        # Assert
        self.mock_repository.deactivate.assert_called_once_with(mock_microservice)
        self.assertEqual(result, deactivated_microservice)