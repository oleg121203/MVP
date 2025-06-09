import pytest
from fastapi.testclient import TestClient
from src.ventai.backend.main import app
import websockets
import asyncio

client = TestClient(app)

@pytest.mark.asyncio
async def test_websocket_metrics():
    """Test WebSocket connection for real-time metrics"""
    async with websockets.connect(
        "ws://localhost:8000/api/v1/analytics/ws/projects/1/metrics"
    ) as websocket:
        # Test connection establishment
        assert websocket.open
        
        # Test message handling (would need mock Redis in practice)
        await websocket.send("test")
        response = await websocket.recv()
        assert isinstance(response, str)
