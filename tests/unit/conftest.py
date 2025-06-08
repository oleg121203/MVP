"""
Unit Tests Configuration
Common utilities and fixtures for unit tests
"""

import os
import sys
import pytest
import tempfile
from unittest.mock import Mock, patch

# Add backend source to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

# Test configuration
TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_REDIS_URL = "redis://localhost:6379/1"

@pytest.fixture(scope="session")
def test_settings():
    """Test settings fixture"""
    return {
        'DATABASE_URL': TEST_DATABASE_URL,
        'REDIS_URL': TEST_REDIS_URL,
        'SECRET_KEY': 'test-secret-key',
        'TESTING': True,
        'DEBUG': True,
    }

@pytest.fixture
def mock_database():
    """Mock database connection"""
    with patch('backend.database.get_connection') as mock_conn:
        mock_conn.return_value = Mock()
        yield mock_conn

@pytest.fixture
def mock_redis():
    """Mock Redis connection"""
    with patch('redis.Redis') as mock_redis:
        mock_instance = Mock()
        mock_redis.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def temp_file():
    """Temporary file fixture"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        yield tmp.name
    os.unlink(tmp.name)

@pytest.fixture
def sample_hvac_data():
    """Sample HVAC calculation data"""
    return {
        'room_area': 50.0,
        'ceiling_height': 3.0,
        'occupancy': 10,
        'air_changes': 6,
        'temperature_indoor': 22.0,
        'temperature_outdoor': -10.0,
        'humidity': 45.0,
    }

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        'email': 'test@ventai.app',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'engineer',
    }

class TestBase:
    """Base test class with common utilities"""
    
    def setup_method(self):
        """Setup before each test method"""
        self.temp_files = []
    
    def teardown_method(self):
        """Cleanup after each test method"""
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                os.unlink(file_path)
    
    def create_temp_file(self, content=""):
        """Create a temporary file with content"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(content)
            self.temp_files.append(tmp.name)
            return tmp.name
