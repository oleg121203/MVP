from fastapi import APIRouter, WebSocket, HTTPException
from typing import Dict, Any
import json
import asyncio
from datetime import datetime
import random

router = APIRouter()

# WebSocket endpoint for real-time data streaming
@router.websocket('/ws/data-stream')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Simulate real-time data streaming (replace with actual data source in production)
        while True:
            # In a real application, this data would come from a live source
            data = {
                'timestamp': datetime.now().isoformat(),
                'value': random.randint(50, 150)  # Simulated data value
            }
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(1)  # Send data every second
    except Exception as e:
        await websocket.close()
        raise HTTPException(status_code=500, detail=str(e))
