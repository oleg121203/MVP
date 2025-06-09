import sys
import os
from fastapi.testclient import TestClient

# Get absolute path to backend directory
backend_path = os.path.abspath('backend')
sys.path.insert(0, backend_path)

# Import app directly from main.py
from main import app

client = TestClient(app)

print("Testing API endpoints:")

# Test analytics endpoint
try:
    response = client.get("/api/v1/analytics/projects/1")
    print(f"GET /analytics/projects/1 - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response contains: {list(response.json().keys())}")
    print("Basic API test completed")
except Exception as e:
    print(f"Test failed: {str(e)}")
