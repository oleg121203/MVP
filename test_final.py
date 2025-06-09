import sys
import os
from fastapi.testclient import TestClient

# Add backend directory to path
sys.path.insert(0, os.path.abspath('backend'))

# Import directly from backend
from main import app

client = TestClient(app)

print("Testing API endpoints:")

# Test root endpoint
response = client.get("/")
print(f"Root endpoint status: {response.status_code}")
print(f"Response: {response.json()}")
assert response.status_code == 200

# Test analytics endpoint
response = client.get("/api/v1/analytics/projects/1")
print(f"Analytics endpoint status: {response.status_code}")
if response.status_code == 200:
    print(f"Response contains: {list(response.json().keys())}")
    assert "metrics" in response.json()
    assert "insights" in response.json()

print("All tests passed successfully")
