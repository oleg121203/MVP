import pytest
from fastapi.testclient import TestClient
from src.ventai.backend.main import app
import websockets
import asyncio
import json

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_websocket_connection():
    """Test basic WebSocket connection and message exchange"""
    async with websockets.connect("ws://localhost:8000/api/v1/analytics/ws/1") as ws:
        test_data = {"metric": "completion_rate", "value": 0.75}
        await ws.send(json.dumps(test_data))
        response = await ws.recv()
        assert json.loads(response) == {"status": "received", "project_id": 1}

@pytest.mark.asyncio
async def test_redis_integration(test_client):
    """Test WebSocket and Redis integration"""
    # Start WebSocket connection
    async with websockets.connect("ws://localhost:8000/api/v1/analytics/ws/1") as ws:
        # Send test data
        test_data = {"metric": "budget_utilization", "value": 0.9}
        await ws.send(json.dumps(test_data))
        
        # Verify Redis received the update
        response = test_client.get("/api/v1/analytics/projects/1")
        assert response.status_code == 200
        assert "budget_utilization" in response.json()["metrics"]
