from fastapi.testclient import TestClient
import sys
import os

# Get absolute path to backend directory
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, backend_path)

# Now import the app
from main import app

client = TestClient(app)

# Test analytics endpoint
print("Testing analytics endpoints...")

# Test analytics endpoint
response = client.get("/api/v1/analytics/projects/1")
print(f"Analytics endpoint status: {response.status_code}")
if response.status_code == 200:
    print("Response contains:", list(response.json().keys()))

# Test metrics endpoint
response = client.get("/api/v1/analytics/projects/1/metrics")
print(f"Metrics endpoint status: {response.status_code}")

# Test insights endpoint
response = client.get("/api/v1/analytics/projects/1/insights")
print(f"Insights endpoint status: {response.status_code}")
