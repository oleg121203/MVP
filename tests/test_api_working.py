import sys
import os
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

# Now import from the installed package
from ventai.backend.main import app

client = TestClient(app)

def test_analytics_endpoint():
    """Basic test for analytics endpoint"""
    response = client.get("/api/v1/analytics/projects/1")
    assert response.status_code in [200, 404]  # Accept either valid response or not found
    if response.status_code == 200:
        data = response.json()
        assert "metrics" in data
        assert "insights" in data

if __name__ == "__main__":
    test_analytics_endpoint()
    print("Test completed successfully")
