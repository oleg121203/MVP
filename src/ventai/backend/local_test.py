import os
import sys
from fastapi.testclient import TestClient

# Import app directly from this directory
from main import app

client = TestClient(app)

print("Testing API endpoints from backend directory:")

# Test analytics endpoint
try:
    response = client.get("/api/v1/analytics/projects/1")
    print(f"GET /analytics/projects/1 - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response contains: {list(response.json().keys())}")
except Exception as e:
    print(f"Test failed: {str(e)}")

print("Test complete")
