import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_analytics_endpoint():
    """Basic smoke test for analytics endpoint"""
    response = client.get("/api/v1/analytics/projects/1")
    assert response.status_code in [200, 404]  # Accept either response
    if response.status_code == 200:
        data = response.json()
        assert "metrics" in data
        assert "insights" in data
