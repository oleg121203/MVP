from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("Testing analytics endpoints from backend directory...")

# Test analytics endpoint
response = client.get("/api/v1/analytics/projects/1")
print(f"Analytics endpoint status: {response.status_code}")
if response.status_code == 200:
    print("Response contains:", list(response.json().keys()))

print("Basic endpoint testing complete")
