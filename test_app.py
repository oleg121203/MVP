import sys
import os
from fastapi.testclient import TestClient

# Import app directly from backend/main.py
sys.path.insert(0, os.path.abspath('.'))
from backend.main import app

client = TestClient(app)

print("Testing API endpoints:")

# Test analytics endpoint
response = client.get("/api/v1/analytics/projects/1")
print(f"GET /analytics/projects/1 - Status: {response.status_code}")
if response.status_code == 200:
    print(f"Response keys: {list(response.json().keys())}")

print("Basic API testing complete")
