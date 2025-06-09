import sys
import os
from fastapi.testclient import TestClient

# Set up Python path
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('backend'))

# Import app directly
from backend.main import app

client = TestClient(app)

print("Verifying API endpoints:")

# Test root endpoint
try:
    response = client.get("/")
    print(f"Root endpoint status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("√ Root endpoint working")
except Exception as e:
    print(f"X Root endpoint failed: {str(e)}")

# Test analytics endpoint
try:
    response = client.get("/api/v1/analytics/projects/1")
    print(f"Analytics endpoint status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response contains: {list(data.keys())}")
        assert "metrics" in data
        assert "insights" in data
        print("√ Analytics endpoint working")
except Exception as e:
    print(f"X Analytics endpoint failed: {str(e)}")
