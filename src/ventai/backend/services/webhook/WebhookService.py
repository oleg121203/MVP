"""
Webhook System for VentAI Enterprise
Handles outbound webhooks to external systems and integrations
"""
import asyncio
import aiohttp
import json
import hmac
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class WebhookEventType(Enum):
    """Types of webhook events"""
    PROJECT_CREATED = "project.created"
    PROJECT_UPDATED = "project.updated" 
    PROJECT_COMPLETED = "project.completed"
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"
    COST_EXCEEDED = "cost.exceeded"
    COST_OPTIMIZED = "cost.optimized"
    RISK_IDENTIFIED = "risk.identified"
    TASK_COMPLETED = "task.completed"
    MOBILE_SYNC = "mobile.sync"

class WebhookStatus(Enum):
    """Webhook delivery status"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"
    CANCELLED = "cancelled"

@dataclass
class WebhookPayload:
    """Webhook payload structure"""
    event_type: WebhookEventType
    event_id: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class WebhookEndpoint:
    """Webhook endpoint configuration"""
    id: str
    name: str
    url: str
    event_types: List[WebhookEventType]
    headers: Dict[str, str]
    secret_key: Optional[str] = None
    is_active: bool = True
    retry_count: int = 3
    timeout_seconds: int = 30

class WebhookDeliveryService:
    """Service for delivering webhooks to external endpoints"""
    
    def __init__(self):
        self.endpoints: Dict[str, WebhookEndpoint] = {}
        self.delivery_queue: asyncio.Queue = asyncio.Queue()
        self.is_processing = False
        
    def register_endpoint(self, endpoint: WebhookEndpoint):
        """Register a new webhook endpoint"""
        self.endpoints[endpoint.id] = endpoint
        logger.info(f"Registered webhook endpoint: {endpoint.name} ({endpoint.url})")
    
    def unregister_endpoint(self, endpoint_id: str):
        """Unregister a webhook endpoint"""
        if endpoint_id in self.endpoints:
            endpoint = self.endpoints.pop(endpoint_id)
            logger.info(f"Unregistered webhook endpoint: {endpoint.name}")
    
    async def send_webhook(self, payload: WebhookPayload) -> bool:
        """Send webhook to all registered endpoints"""
        if not self.endpoints:
            logger.warning("No webhook endpoints registered")
            return True
        
        # Find endpoints that should receive this event
        target_endpoints = [
            endpoint for endpoint in self.endpoints.values()
            if endpoint.is_active and payload.event_type in endpoint.event_types
        ]
        
        if not target_endpoints:
            logger.debug(f"No endpoints registered for event type: {payload.event_type.value}")
            return True
        
        # Send to all target endpoints
        tasks = []
        for endpoint in target_endpoints:
            task = asyncio.create_task(
                self._deliver_webhook(endpoint, payload)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check results
        success_count = sum(1 for result in results if result is True)
        total_count = len(results)
        
        logger.info(f"Webhook delivery: {success_count}/{total_count} successful")
        
        return success_count == total_count
    
    async def _deliver_webhook(self, endpoint: WebhookEndpoint, payload: WebhookPayload) -> bool:
        """Deliver webhook to a specific endpoint with retries"""
        attempt = 0
        max_attempts = endpoint.retry_count + 1
        
        while attempt < max_attempts:
            try:
                success = await self._make_webhook_request(endpoint, payload, attempt + 1)
                if success:
                    return True
                
                attempt += 1
                if attempt < max_attempts:
                    # Exponential backoff
                    delay = 2 ** attempt
                    logger.info(f"Retrying webhook delivery to {endpoint.name} in {delay}s...")
                    await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error delivering webhook to {endpoint.name}: {e}")
                attempt += 1
                
                if attempt < max_attempts:
                    delay = 2 ** attempt
                    await asyncio.sleep(delay)
        
        logger.error(f"Failed to deliver webhook to {endpoint.name} after {max_attempts} attempts")
        return False
    
    async def _make_webhook_request(self, endpoint: WebhookEndpoint, payload: WebhookPayload, attempt: int) -> bool:
        """Make the actual HTTP request to the webhook endpoint"""
        try:
            # Prepare the request payload
            webhook_data = {
                "event_type": payload.event_type.value,
                "event_id": payload.event_id,
                "timestamp": payload.timestamp.isoformat(),
                "data": payload.data,
                "metadata": payload.metadata or {}
            }
            
            # Add delivery metadata
            webhook_data["metadata"]["delivery_attempt"] = attempt
            webhook_data["metadata"]["source"] = "VentAI Enterprise"
            
            # Prepare headers
            headers = dict(endpoint.headers)
            headers["Content-Type"] = "application/json"
            headers["User-Agent"] = "VentAI-Webhook/1.0"
            
            # Add signature if secret key is provided
            if endpoint.secret_key:
                signature = self._generate_signature(
                    json.dumps(webhook_data, sort_keys=True),
                    endpoint.secret_key
                )
                headers["X-VentAI-Signature"] = signature
            
            # Make the request
            async with aiohttp.ClientSession() as session:
                start_time = datetime.now()
                
                async with session.post(
                    endpoint.url,
                    json=webhook_data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=endpoint.timeout_seconds)
                ) as response:
                    end_time = datetime.now()
                    response_time = (end_time - start_time).total_seconds() * 1000
                    
                    # Log the delivery
                    await self._log_webhook_delivery(
                        endpoint,
                        payload,
                        attempt,
                        response.status,
                        await response.text(),
                        response_time
                    )
                    
                    # Consider 2xx status codes as success
                    if 200 <= response.status < 300:
                        logger.info(f"Webhook delivered successfully to {endpoint.name} (status: {response.status})")
                        return True
                    else:
                        logger.warning(f"Webhook delivery failed to {endpoint.name} (status: {response.status})")
                        return False
                        
        except asyncio.TimeoutError:
            logger.error(f"Webhook request to {endpoint.name} timed out")
            return False
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error delivering webhook to {endpoint.name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error delivering webhook to {endpoint.name}: {e}")
            return False
    
    def _generate_signature(self, payload: str, secret: str) -> str:
        """Generate HMAC signature for webhook verification"""
        signature = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"
    
    async def _log_webhook_delivery(self, endpoint: WebhookEndpoint, payload: WebhookPayload, 
                                   attempt: int, status_code: int, response_body: str, 
                                   response_time: float):
        """Log webhook delivery for analytics and debugging"""
        # In a real implementation, this would write to the database
        log_data = {
            "endpoint_id": endpoint.id,
            "endpoint_name": endpoint.name,
            "event_type": payload.event_type.value,
            "event_id": payload.event_id,
            "attempt": attempt,
            "status_code": status_code,
            "response_time_ms": response_time,
            "success": 200 <= status_code < 300,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.debug(f"Webhook delivery log: {log_data}")
    
    async def start_processing(self):
        """Start processing webhook queue"""
        if self.is_processing:
            logger.warning("Webhook processing already started")
            return
        
        self.is_processing = True
        logger.info("Started webhook delivery processing")
        
        while self.is_processing:
            try:
                # Wait for webhooks in the queue
                payload = await asyncio.wait_for(self.delivery_queue.get(), timeout=1.0)
                await self.send_webhook(payload)
                self.delivery_queue.task_done()
                
            except asyncio.TimeoutError:
                # No webhooks in queue, continue loop
                continue
            except Exception as e:
                logger.error(f"Error processing webhook queue: {e}")
    
    async def stop_processing(self):
        """Stop processing webhook queue"""
        self.is_processing = False
        logger.info("Stopped webhook delivery processing")
    
    async def queue_webhook(self, payload: WebhookPayload):
        """Add webhook to delivery queue"""
        await self.delivery_queue.put(payload)
        logger.debug(f"Queued webhook: {payload.event_type.value}")

# Global webhook service instance
webhook_service = WebhookDeliveryService()

# Helper functions for common webhook events
async def send_project_created_webhook(project_data: Dict[str, Any]):
    """Send project created webhook"""
    payload = WebhookPayload(
        event_type=WebhookEventType.PROJECT_CREATED,
        event_id=f"project_created_{project_data.get('id', 'unknown')}_{int(datetime.now().timestamp())}",
        timestamp=datetime.now(),
        data=project_data
    )
    await webhook_service.queue_webhook(payload)

async def send_workflow_completed_webhook(workflow_data: Dict[str, Any]):
    """Send workflow completed webhook"""
    payload = WebhookPayload(
        event_type=WebhookEventType.WORKFLOW_COMPLETED,
        event_id=f"workflow_completed_{workflow_data.get('id', 'unknown')}_{int(datetime.now().timestamp())}",
        timestamp=datetime.now(),
        data=workflow_data
    )
    await webhook_service.queue_webhook(payload)

async def send_cost_alert_webhook(cost_data: Dict[str, Any], alert_type: str = "exceeded"):
    """Send cost alert webhook"""
    event_type = WebhookEventType.COST_EXCEEDED if alert_type == "exceeded" else WebhookEventType.COST_OPTIMIZED
    
    payload = WebhookPayload(
        event_type=event_type,
        event_id=f"cost_{alert_type}_{cost_data.get('project_id', 'unknown')}_{int(datetime.now().timestamp())}",
        timestamp=datetime.now(),
        data=cost_data
    )
    await webhook_service.queue_webhook(payload)

async def send_risk_identified_webhook(risk_data: Dict[str, Any]):
    """Send risk identified webhook"""
    payload = WebhookPayload(
        event_type=WebhookEventType.RISK_IDENTIFIED,
        event_id=f"risk_identified_{risk_data.get('project_id', 'unknown')}_{int(datetime.now().timestamp())}",
        timestamp=datetime.now(),
        data=risk_data
    )
    await webhook_service.queue_webhook(payload)

# Integration with workflow engine
async def setup_webhook_integration():
    """Setup webhook integration with workflow engine"""
    try:
        # Register sample endpoints (in production, these would come from database)
        sample_endpoints = [
            WebhookEndpoint(
                id="sample_project_webhook",
                name="Project Management Integration",
                url="https://api.example.com/ventai/webhooks",
                event_types=[
                    WebhookEventType.PROJECT_CREATED,
                    WebhookEventType.PROJECT_UPDATED,
                    WebhookEventType.PROJECT_COMPLETED
                ],
                headers={"Authorization": "Bearer sample_token"},
                secret_key="webhook_secret_123"
            ),
            WebhookEndpoint(
                id="sample_cost_webhook",
                name="Cost Management Integration",
                url="https://api.example.com/cost-alerts",
                event_types=[
                    WebhookEventType.COST_EXCEEDED,
                    WebhookEventType.COST_OPTIMIZED
                ],
                headers={"X-API-Key": "cost_api_key"},
                secret_key="cost_webhook_456"
            )
        ]
        
        for endpoint in sample_endpoints:
            webhook_service.register_endpoint(endpoint)
        
        # Start webhook processing
        asyncio.create_task(webhook_service.start_processing())
        
        logger.info("Webhook integration setup completed")
        
    except Exception as e:
        logger.error(f"Failed to setup webhook integration: {e}")
        raise
