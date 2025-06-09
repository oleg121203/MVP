import sys
import os
from fastapi.testclient import TestClient

# Add backend directory to path
sys.path.append(os.path.abspath('backend'))

from main import app

client = TestClient(app)

# Test analytics endpoint
response = client.get("/api/v1/analytics/projects/1")
print(f"Analytics endpoint status: {response.status_code}")
if response.status_code == 200:
    print("Response contains:", list(response.json().keys()))
