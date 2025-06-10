"""
Webhook API Endpoints for VentAI Enterprise
Provides REST API for managing webhook endpoints and external integrations
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import logging

from ventai.backend.services.webhook.WebhookService import (
    webhook_service, 
    WebhookEndpoint, 
    WebhookEventType,
    WebhookPayload,
    send_project_created_webhook,
    send_workflow_completed_webhook,
    send_cost_alert_webhook,
    send_risk_identified_webhook
)

logger = logging.getLogger(__name__)

# API Router
webhook_router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

# Request/Response Models
class CreateWebhookRequest(BaseModel):
    name: str
    url: HttpUrl
    event_types: List[str]
    headers: Optional[Dict[str, str]] = {}
    secret_key: Optional[str] = None
    retry_count: Optional[int] = 3
    timeout_seconds: Optional[int] = 30

class UpdateWebhookRequest(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    event_types: Optional[List[str]] = None
    headers: Optional[Dict[str, str]] = None
    secret_key: Optional[str] = None
    is_active: Optional[bool] = None
    retry_count: Optional[int] = None
    timeout_seconds: Optional[int] = None

class WebhookResponse(BaseModel):
    id: str
    name: str
    url: str
    event_types: List[str]
    is_active: bool
    retry_count: int
    timeout_seconds: int
    created_at: str

class TestWebhookRequest(BaseModel):
    endpoint_id: str
    event_type: str
    test_data: Dict[str, Any]

class WebhookStatsResponse(BaseModel):
    total_endpoints: int
    active_endpoints: int
    total_deliveries: int
    successful_deliveries: int
    failed_deliveries: int
    average_response_time: float

@webhook_router.post("/endpoints", response_model=Dict[str, Any])
async def create_webhook_endpoint(request: CreateWebhookRequest):
    """Create a new webhook endpoint"""
    try:
        # Validate event types
        valid_event_types = [event.value for event in WebhookEventType]
        invalid_events = [event for event in request.event_types if event not in valid_event_types]
        
        if invalid_events:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid event types: {invalid_events}. Valid types: {valid_event_types}"
            )
        
        # Convert event type strings to enums
        event_enums = [WebhookEventType(event) for event in request.event_types]
        
        # Create webhook endpoint
        endpoint_id = str(uuid.uuid4())
        endpoint = WebhookEndpoint(
            id=endpoint_id,
            name=request.name,
            url=str(request.url),
            event_types=event_enums,
            headers=request.headers or {},
            secret_key=request.secret_key,
            retry_count=request.retry_count or 3,
            timeout_seconds=request.timeout_seconds or 30
        )
        
        # Register with webhook service
        webhook_service.register_endpoint(endpoint)
        
        return {
            "success": True,
            "message": "Webhook endpoint created successfully",
            "endpoint_id": endpoint_id,
            "endpoint": {
                "id": endpoint.id,
                "name": endpoint.name,
                "url": endpoint.url,
                "event_types": [event.value for event in endpoint.event_types],
                "is_active": endpoint.is_active,
                "created_at": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create webhook endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create webhook endpoint: {str(e)}")

@webhook_router.get("/endpoints", response_model=List[WebhookResponse])
async def list_webhook_endpoints():
    """List all registered webhook endpoints"""
    try:
        endpoints = []
        for endpoint in webhook_service.endpoints.values():
            endpoints.append(WebhookResponse(
                id=endpoint.id,
                name=endpoint.name,
                url=endpoint.url,
                event_types=[event.value for event in endpoint.event_types],
                is_active=endpoint.is_active,
                retry_count=endpoint.retry_count,
                timeout_seconds=endpoint.timeout_seconds,
                created_at=datetime.now().isoformat()  # In real app, would come from database
            ))
        
        return endpoints
        
    except Exception as e:
        logger.error(f"Failed to list webhook endpoints: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list webhook endpoints: {str(e)}")

@webhook_router.get("/endpoints/{endpoint_id}", response_model=WebhookResponse)
async def get_webhook_endpoint(endpoint_id: str):
    """Get details of a specific webhook endpoint"""
    try:
        if endpoint_id not in webhook_service.endpoints:
            raise HTTPException(status_code=404, detail="Webhook endpoint not found")
        
        endpoint = webhook_service.endpoints[endpoint_id]
        
        return WebhookResponse(
            id=endpoint.id,
            name=endpoint.name,
            url=endpoint.url,
            event_types=[event.value for event in endpoint.event_types],
            is_active=endpoint.is_active,
            retry_count=endpoint.retry_count,
            timeout_seconds=endpoint.timeout_seconds,
            created_at=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get webhook endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get webhook endpoint: {str(e)}")

@webhook_router.put("/endpoints/{endpoint_id}", response_model=Dict[str, Any])
async def update_webhook_endpoint(endpoint_id: str, request: UpdateWebhookRequest):
    """Update an existing webhook endpoint"""
    try:
        if endpoint_id not in webhook_service.endpoints:
            raise HTTPException(status_code=404, detail="Webhook endpoint not found")
        
        endpoint = webhook_service.endpoints[endpoint_id]
        
        # Update fields if provided
        if request.name is not None:
            endpoint.name = request.name
        if request.url is not None:
            endpoint.url = str(request.url)
        if request.event_types is not None:
            # Validate event types
            valid_event_types = [event.value for event in WebhookEventType]
            invalid_events = [event for event in request.event_types if event not in valid_event_types]
            
            if invalid_events:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid event types: {invalid_events}. Valid types: {valid_event_types}"
                )
            
            endpoint.event_types = [WebhookEventType(event) for event in request.event_types]
        
        if request.headers is not None:
            endpoint.headers = request.headers
        if request.secret_key is not None:
            endpoint.secret_key = request.secret_key
        if request.is_active is not None:
            endpoint.is_active = request.is_active
        if request.retry_count is not None:
            endpoint.retry_count = request.retry_count
        if request.timeout_seconds is not None:
            endpoint.timeout_seconds = request.timeout_seconds
        
        return {
            "success": True,
            "message": "Webhook endpoint updated successfully",
            "endpoint": {
                "id": endpoint.id,
                "name": endpoint.name,
                "url": endpoint.url,
                "event_types": [event.value for event in endpoint.event_types],
                "is_active": endpoint.is_active
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update webhook endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update webhook endpoint: {str(e)}")

@webhook_router.delete("/endpoints/{endpoint_id}", response_model=Dict[str, Any])
async def delete_webhook_endpoint(endpoint_id: str):
    """Delete a webhook endpoint"""
    try:
        if endpoint_id not in webhook_service.endpoints:
            raise HTTPException(status_code=404, detail="Webhook endpoint not found")
        
        webhook_service.unregister_endpoint(endpoint_id)
        
        return {
            "success": True,
            "message": "Webhook endpoint deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete webhook endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete webhook endpoint: {str(e)}")

@webhook_router.post("/test", response_model=Dict[str, Any])
async def test_webhook_endpoint(request: TestWebhookRequest, background_tasks: BackgroundTasks):
    """Send a test webhook to a specific endpoint"""
    try:
        if request.endpoint_id not in webhook_service.endpoints:
            raise HTTPException(status_code=404, detail="Webhook endpoint not found")
        
        # Validate event type
        try:
            event_type = WebhookEventType(request.event_type)
        except ValueError:
            valid_event_types = [event.value for event in WebhookEventType]
            raise HTTPException(
                status_code=400,
                detail=f"Invalid event type: {request.event_type}. Valid types: {valid_event_types}"
            )
        
        # Create test payload
        test_payload = WebhookPayload(
            event_type=event_type,
            event_id=f"test_{request.endpoint_id}_{int(datetime.now().timestamp())}",
            timestamp=datetime.now(),
            data=request.test_data,
            metadata={"test": True, "source": "webhook_api_test"}
        )
        
        # Send webhook in background
        background_tasks.add_task(webhook_service.send_webhook, test_payload)
        
        return {
            "success": True,
            "message": "Test webhook queued for delivery",
            "event_id": test_payload.event_id,
            "event_type": test_payload.event_type.value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to send test webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send test webhook: {str(e)}")

@webhook_router.get("/events/types", response_model=List[str])
async def get_webhook_event_types():
    """Get list of available webhook event types"""
    try:
        return [event.value for event in WebhookEventType]
    except Exception as e:
        logger.error(f"Failed to get event types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get event types: {str(e)}")

@webhook_router.get("/stats", response_model=WebhookStatsResponse)
async def get_webhook_statistics():
    """Get webhook delivery statistics"""
    try:
        # In a real implementation, these stats would come from the database
        total_endpoints = len(webhook_service.endpoints)
        active_endpoints = len([ep for ep in webhook_service.endpoints.values() if ep.is_active])
        
        # Mock statistics for now
        stats = WebhookStatsResponse(
            total_endpoints=total_endpoints,
            active_endpoints=active_endpoints,
            total_deliveries=0,  # Would be calculated from webhook_logs table
            successful_deliveries=0,
            failed_deliveries=0,
            average_response_time=0.0
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get webhook statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get webhook statistics: {str(e)}")

@webhook_router.post("/events/project-created", response_model=Dict[str, Any])
async def trigger_project_created_webhook(project_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """Manually trigger a project created webhook (for testing)"""
    try:
        background_tasks.add_task(send_project_created_webhook, project_data)
        
        return {
            "success": True,
            "message": "Project created webhook triggered",
            "project_id": project_data.get("id", "unknown")
        }
        
    except Exception as e:
        logger.error(f"Failed to trigger project created webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger webhook: {str(e)}")

@webhook_router.post("/events/workflow-completed", response_model=Dict[str, Any])
async def trigger_workflow_completed_webhook(workflow_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """Manually trigger a workflow completed webhook (for testing)"""
    try:
        background_tasks.add_task(send_workflow_completed_webhook, workflow_data)
        
        return {
            "success": True,
            "message": "Workflow completed webhook triggered",
            "workflow_id": workflow_data.get("id", "unknown")
        }
        
    except Exception as e:
        logger.error(f"Failed to trigger workflow completed webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger webhook: {str(e)}")

@webhook_router.post("/events/cost-alert", response_model=Dict[str, Any])
async def trigger_cost_alert_webhook(cost_data: Dict[str, Any], alert_type: str = "exceeded", background_tasks: BackgroundTasks = BackgroundTasks()):
    """Manually trigger a cost alert webhook (for testing)"""
    try:
        if alert_type not in ["exceeded", "optimized"]:
            raise HTTPException(status_code=400, detail="alert_type must be 'exceeded' or 'optimized'")
        
        background_tasks.add_task(send_cost_alert_webhook, cost_data, alert_type)
        
        return {
            "success": True,
            "message": f"Cost {alert_type} webhook triggered",
            "project_id": cost_data.get("project_id", "unknown"),
            "alert_type": alert_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger cost alert webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger webhook: {str(e)}")

@webhook_router.get("/health", response_model=Dict[str, Any])
async def webhook_health_check():
    """Health check for webhook service"""
    try:
        total_endpoints = len(webhook_service.endpoints)
        active_endpoints = len([ep for ep in webhook_service.endpoints.values() if ep.is_active])
        is_processing = webhook_service.is_processing
        
        return {
            "status": "healthy",
            "total_endpoints": total_endpoints,
            "active_endpoints": active_endpoints,
            "is_processing": is_processing,
            "queue_size": webhook_service.delivery_queue.qsize(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Webhook health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Helper function to include router in main app
def include_webhook_routes(app):
    """Include webhook routes in FastAPI app"""
    app.include_router(webhook_router)
