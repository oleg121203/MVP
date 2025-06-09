import pytest
from fastapi.testclient import TestClient
from src.ventai.backend.main import app
import json

@pytest.fixture
def test_client():
    return TestClient(app)

def test_websocket_connection(test_client):
    """Test WebSocket connection establishment"""
    with test_client.websocket_connect("/api/v1/analytics/ws/1") as websocket:
        assert websocket.receive_text() == "Connected"

@pytest.mark.asyncio
async def test_websocket_message_handling(test_client):
    """Test WebSocket message handling"""
    with test_client.websocket_connect("/api/v1/analytics/ws/1") as websocket:
        test_msg = {"action": "subscribe", "metric": "completion_rate"}
        websocket.send_text(json.dumps(test_msg))
        response = json.loads(websocket.receive_text())
        assert response["status"] == "subscribed"
