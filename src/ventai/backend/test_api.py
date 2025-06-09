import pytest
from fastapi.testclient import TestClient

# Import app from package
from backend.main import app

client = TestClient(app)

@pytest.fixture
def test_client():
    yield client

def test_root_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "VentAI API is working"}

def test_analytics_endpoint(test_client):
    response = test_client.get("/api/v1/analytics/projects/1")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "insights" in data
