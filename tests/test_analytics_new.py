import pytest
from fastapi.testclient import TestClient

from ventai.backend.main import app

client = TestClient(app)

def test_analytics_endpoint():
    response = client.get("/api/v1/analytics/projects/1")
    assert response.status_code in [200, 404]  # Basic smoke test
    if response.status_code == 200:
        assert "metrics" in response.json()
        assert "insights" in response.json()
