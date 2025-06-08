"""
Integration Tests Configuration
Setup for integration tests that test component interactions
"""

import os
import sys
import pytest
import asyncio
import httpx
from typing import AsyncGenerator

# Add backend source to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src'))

# Test URLs
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
MCP_URL = "http://localhost:8001"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def backend_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Async HTTP client for backend API testing"""
    async with httpx.AsyncClient(base_url=BACKEND_URL) as client:
        yield client

@pytest.fixture(scope="session")
async def mcp_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Async HTTP client for MCP service testing"""
    async with httpx.AsyncClient(base_url=MCP_URL) as client:
        yield client

@pytest.fixture
async def authenticated_user(backend_client):
    """Create and authenticate a test user"""
    user_data = {
        "email": "integration_test@ventai.app",
        "password": "testpassword123",
        "first_name": "Integration",
        "last_name": "Test"
    }
    
    # Register user
    response = await backend_client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = await backend_client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    
    # Return authenticated client
    headers = {"Authorization": f"Bearer {token}"}
    return backend_client, headers, user_data

@pytest.fixture
def sample_project_data():
    """Sample project data for integration tests"""
    return {
        "name": "Integration Test Project",
        "description": "Test project for integration testing",
        "building_type": "office",
        "total_area": 1000.0,
        "floors": 3,
        "location": "Kyiv, Ukraine"
    }

@pytest.fixture
def wait_for_services():
    """Wait for all services to be ready"""
    import time
    import requests
    
    def wait_for_service(url, timeout=60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    return True
            except:
                pass
            time.sleep(2)
        return False
    
    # Wait for all services
    services = [BACKEND_URL, MCP_URL]
    for service_url in services:
        if not wait_for_service(service_url):
            pytest.skip(f"Service {service_url} is not available")
    
    return True

class IntegrationTestBase:
    """Base class for integration tests"""
    
    def setup_method(self):
        """Setup before each test method"""
        self.test_data = {}
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Cleanup test data if needed
        pass
