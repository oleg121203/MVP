import pytest
import subprocess
import time
import websockets
import json

@pytest.fixture(scope="module")
def server():
    # Start server in background
    process = subprocess.Popen([
        "source venv/bin/activate && uvicorn", 
        "ventai.backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])
    
    # Wait for server to start
    time.sleep(3)
    yield
    
    # Clean up
    process.terminate()

@pytest.mark.asyncio
async def test_websocket_connection(server):
    """Test basic WebSocket connection"""
    async with websockets.connect("ws://localhost:8000/api/v1/analytics/ws/1") as ws:
        assert ws.open
        await ws.close()

@pytest.mark.asyncio
async def test_websocket_message_exchange(server):
    """Test sending and receiving messages"""
    async with websockets.connect("ws://localhost:8000/api/v1/analytics/ws/1") as ws:
        test_msg = {"action": "subscribe", "metric": "completion_rate"}
        await ws.send(json.dumps(test_msg))
        response = await ws.recv()
        assert json.loads(response)["status"] == "subscribed"
