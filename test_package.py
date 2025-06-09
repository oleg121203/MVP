import pytest
from fastapi.testclient import TestClient

# Import from installed package
from ventai.backend.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "VentAI API is working"}

def test_analytics_endpoint():
    response = client.get("/api/v1/analytics/projects/1")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "insights" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
