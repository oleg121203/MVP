from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import json
import pandas as pd
import tempfile
from datetime import datetime
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from ..services.analytics import ProjectAnalyticsEngine
import redis
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])

@router.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: int):
    await websocket.accept()
    await websocket.send_text("Connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "subscribe":
                response = {"status": "subscribed", "metric": message["metric"]}
                await websocket.send_text(json.dumps(response))
            else:
                await sio.emit('analytics_update', {
                    'project_id': project_id,
                    'data': message
                })
    except WebSocketDisconnect:
        print(f"Client disconnected for project {project_id}")

@router.get("/projects/{project_id}")
async def get_project_analytics(project_id: int):
    return {
        "metrics": {
            "completion_rate": 0.75,
            "budget_compliance": 0.9
        },
        "insights": "Test insights"
    }

@router.get('/export/{project_id}/pdf')
async def export_pdf(project_id: int):
    """Generate PDF report"""
    # In a real implementation, this would generate an actual PDF
    temp_path = f"/tmp/ventai_report_{project_id}.pdf"
    with open(temp_path, 'w') as f:
        f.write(f"PDF Report for Project {project_id}")
    return FileResponse(temp_path, filename=f"project_{project_id}_report.pdf")

@router.get('/export/{project_id}/csv')
async def export_csv(project_id: int):
    """Generate CSV report"""
    df = pd.DataFrame({
        'Metric': ['Completion Rate', 'Budget Utilization', 'Time Efficiency'],
        'Value': [0.75, 0.85, 1.2]  # Example values
    })
    
    temp_path = f"/tmp/ventai_report_{project_id}.csv"
    df.to_csv(temp_path, index=False)
    return FileResponse(temp_path, filename=f"project_{project_id}_report.csv")

@router.get('/export/{project_id}/excel')
async def export_excel(project_id: int):
    """Generate Excel report"""
    df = pd.DataFrame({
        'Metric': ['Completion Rate', 'Budget Utilization', 'Time Efficiency'],
        'Value': [0.75, 0.85, 1.2]  # Example values
    })
    
    temp_path = f"/tmp/ventai_report_{project_id}.xlsx"
    df.to_excel(temp_path, index=False)
    return FileResponse(temp_path, filename=f"project_{project_id}_report.xlsx")

@router.websocket("/ws/projects/{project_id}/metrics")
async def websocket_metrics(websocket: WebSocket, project_id: int):
    await websocket.accept()
    redis_client = redis.Redis(host='localhost', port=6380, db=0)
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f'project:{project_id}:metrics')
    
    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_text(message['data'].decode('utf-8'))
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pubsub.close()
        await websocket.close()
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        pubsub.close()
        await websocket.close(code=1011)
