import sys
import os
from fastapi.testclient import TestClient

# Get absolute path to backend directory
backend_dir = os.path.abspath('backend')
sys.path.insert(0, backend_dir)

# Import directly from files
from main import app  # This imports from backend/main.py

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
    data = response.json()
    print(f"Response contains: {list(data.keys())}")
    assert "metrics" in data
    assert "insights" in data

print("All tests completed successfully")
