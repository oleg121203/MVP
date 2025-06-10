"""
Mobile API Gateway for VentAI Field Operations
Provides optimized API endpoints for mobile applications and field work
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import asyncio

from ventai.backend.services.ai.AIProjectManager import ai_project_manager
from ventai.backend.services.workflow.WorkflowEngine import workflow_engine

logger = logging.getLogger(__name__)

# Mobile API Router
mobile_router = APIRouter(prefix="/api/mobile", tags=["mobile"])

# Mobile-specific models
class MobileAuthRequest(BaseModel):
    username: str
    password: str
    device_id: str
    device_type: str  # ios, android
    app_version: str

class MobileAuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    user_profile: Dict[str, Any]

class ProjectSummary(BaseModel):
    id: str
    name: str
    status: str
    progress: float
    priority: str
    last_updated: str
    next_action: str

class FieldTaskUpdate(BaseModel):
    task_id: str
    status: str
    progress: float
    notes: str
    location: Optional[Dict[str, float]] = None  # lat, lng
    photos: Optional[List[str]] = None
    timestamp: str

class OfflineSync(BaseModel):
    device_id: str
    last_sync: str
    pending_updates: List[Dict[str, Any]]
    data_size_mb: float

# Authentication dependency for mobile
async def get_mobile_user(authorization: str = Header(None)):
    """Validate mobile user authentication"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    # TODO: Implement actual JWT token validation
    # For now, return mock user data
    return {
        "user_id": "mobile_user_001",
        "username": "field_technician",
        "role": "technician",
        "permissions": ["view_projects", "update_tasks", "upload_photos"]
    }

@mobile_router.post("/auth/login", response_model=MobileAuthResponse)
async def mobile_login(request: MobileAuthRequest):
    """Mobile-optimized authentication"""
    try:
        # TODO: Implement actual authentication logic
        # For now, return mock response
        
        if request.username == "demo" and request.password == "demo123":
            return MobileAuthResponse(
                access_token="mock_mobile_token_123456",
                refresh_token="mock_refresh_token_789012",
                expires_in=3600,
                user_profile={
                    "id": "user_001",
                    "username": request.username,
                    "full_name": "Demo Technician",
                    "role": "field_technician",
                    "avatar_url": "/api/avatars/demo_user.jpg",
                    "last_login": datetime.now().isoformat(),
                    "device_registered": True
                }
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    except Exception as e:
        logger.error(f"Mobile login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Authentication failed")

@mobile_router.get("/projects/summary", response_model=List[ProjectSummary])
async def get_mobile_project_summary(user=Depends(get_mobile_user)):
    """Get mobile-optimized project summary"""
    try:
        # TODO: Fetch actual projects from database
        # For now, return mock data optimized for mobile
        
        projects = [
            ProjectSummary(
                id="PROJ-001",
                name="Downtown Office HVAC",
                status="in_progress",
                progress=65.5,
                priority="high",
                last_updated=datetime.now().isoformat(),
                next_action="Install ductwork on 3rd floor"
            ),
            ProjectSummary(
                id="PROJ-002", 
                name="Residential Complex - Phase 2",
                status="planning",
                progress=25.0,
                priority="medium",
                last_updated=datetime.now().isoformat(),
                next_action="Complete load calculations"
            ),
            ProjectSummary(
                id="PROJ-003",
                name="Hospital Emergency Repair",
                status="critical",
                progress=15.0,
                priority="critical",
                last_updated=datetime.now().isoformat(),
                next_action="Replace failed compressor unit"
            )
        ]
        
        return projects
    
    except Exception as e:
        logger.error(f"Error fetching mobile project summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch projects")

@mobile_router.get("/projects/{project_id}/tasks", response_model=Dict[str, Any])
async def get_project_tasks_mobile(project_id: str, user=Depends(get_mobile_user)):
    """Get mobile-optimized project tasks"""
    try:
        # TODO: Fetch actual tasks from database
        # Return mobile-friendly task list
        
        tasks = {
            "project_id": project_id,
            "project_name": "Downtown Office HVAC",
            "tasks": [
                {
                    "id": "TASK-001",
                    "title": "Site Assessment",
                    "description": "Complete initial site survey and measurements",
                    "status": "completed",
                    "priority": "high",
                    "assigned_to": user["username"],
                    "due_date": "2025-06-12T09:00:00Z",
                    "estimated_hours": 4,
                    "location": {
                        "address": "123 Business Center Dr",
                        "coordinates": {"lat": 40.7128, "lng": -74.0060}
                    },
                    "checklist": [
                        {"item": "Measure existing ductwork", "completed": True},
                        {"item": "Photograph equipment", "completed": True},
                        {"item": "Check electrical connections", "completed": True}
                    ]
                },
                {
                    "id": "TASK-002",
                    "title": "Equipment Installation",
                    "description": "Install new HVAC units on floors 2-4",
                    "status": "in_progress",
                    "priority": "high",
                    "assigned_to": user["username"],
                    "due_date": "2025-06-15T17:00:00Z",
                    "estimated_hours": 16,
                    "location": {
                        "address": "123 Business Center Dr",
                        "coordinates": {"lat": 40.7128, "lng": -74.0060}
                    },
                    "checklist": [
                        {"item": "Floor 2 unit installation", "completed": True},
                        {"item": "Floor 3 unit installation", "completed": False},
                        {"item": "Floor 4 unit installation", "completed": False},
                        {"item": "System connectivity check", "completed": False}
                    ]
                }
            ],
            "summary": {
                "total_tasks": 2,
                "completed": 1,
                "in_progress": 1,
                "pending": 0,
                "completion_percentage": 50.0
            }
        }
        
        return tasks
    
    except Exception as e:
        logger.error(f"Error fetching project tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch project tasks")

@mobile_router.post("/tasks/update", response_model=Dict[str, Any])
async def update_task_from_field(update: FieldTaskUpdate, user=Depends(get_mobile_user)):
    """Update task status from field work"""
    try:
        # TODO: Implement actual task update logic
        
        # Validate task update
        if update.progress < 0 or update.progress > 100:
            raise HTTPException(status_code=400, detail="Progress must be between 0 and 100")
        
        # Process photos if provided
        photo_urls = []
        if update.photos:
            # TODO: Implement actual photo upload/storage
            photo_urls = [f"/api/photos/{update.task_id}_{i}.jpg" for i in range(len(update.photos))]
        
        # Create update record
        task_update = {
            "task_id": update.task_id,
            "updated_by": user["username"],
            "update_timestamp": datetime.now().isoformat(),
            "previous_status": "in_progress",  # TODO: Get actual previous status
            "new_status": update.status,
            "progress_change": update.progress,
            "notes": update.notes,
            "location_logged": update.location is not None,
            "photos_count": len(update.photos) if update.photos else 0,
            "photo_urls": photo_urls
        }
        
        # TODO: Save to database and trigger workflows if needed
        
        return {
            "success": True,
            "message": "Task updated successfully",
            "update_id": f"UPDATE_{int(datetime.now().timestamp())}",
            "task_update": task_update,
            "next_actions": [
                "Complete equipment testing",
                "Update project timeline",
                "Notify project manager"
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update task")

@mobile_router.get("/offline/sync", response_model=Dict[str, Any])
async def get_offline_data(device_id: str, user=Depends(get_mobile_user)):
    """Get data for offline mobile usage"""
    try:
        # TODO: Implement actual offline data preparation
        
        offline_data = {
            "sync_timestamp": datetime.now().isoformat(),
            "device_id": device_id,
            "data_version": "v1.2.0",
            "expires_at": (datetime.now().timestamp() + 86400),  # 24 hours
            "projects": [
                {
                    "id": "PROJ-001",
                    "name": "Downtown Office HVAC",
                    "basic_info": True,
                    "tasks": True,
                    "specifications": False,  # Too large for offline
                    "photos": False  # Download on-demand
                }
            ],
            "reference_data": {
                "equipment_catalog": True,
                "compliance_standards": True,
                "calculation_formulas": True
            },
            "user_preferences": {
                "units": "imperial",
                "language": "en",
                "auto_sync": True
            },
            "estimated_storage_mb": 15.2
        }
        
        return {
            "success": True,
            "offline_data": offline_data,
            "download_urls": {
                "projects": f"/api/mobile/offline/download/projects/{device_id}",
                "reference": f"/api/mobile/offline/download/reference/{device_id}"
            }
        }
    
    except Exception as e:
        logger.error(f"Error preparing offline data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to prepare offline data")

@mobile_router.post("/offline/sync", response_model=Dict[str, Any])
async def sync_offline_updates(sync_data: OfflineSync, user=Depends(get_mobile_user)):
    """Sync offline updates back to server"""
    try:
        processed_updates = []
        failed_updates = []
        
        for update in sync_data.pending_updates:
            try:
                # TODO: Process each offline update
                update_id = update.get("id", "unknown")
                update_type = update.get("type", "unknown")
                
                # Validate and process update based on type
                if update_type == "task_update":
                    # Process task update
                    processed_updates.append({
                        "id": update_id,
                        "type": update_type,
                        "status": "processed",
                        "server_timestamp": datetime.now().isoformat()
                    })
                elif update_type == "photo_upload":
                    # Process photo upload
                    processed_updates.append({
                        "id": update_id,
                        "type": update_type,
                        "status": "processed",
                        "photo_url": f"/api/photos/{update_id}.jpg"
                    })
                else:
                    failed_updates.append({
                        "id": update_id,
                        "error": f"Unknown update type: {update_type}"
                    })
            
            except Exception as update_error:
                failed_updates.append({
                    "id": update.get("id", "unknown"),
                    "error": str(update_error)
                })
        
        return {
            "success": True,
            "sync_timestamp": datetime.now().isoformat(),
            "processed_count": len(processed_updates),
            "failed_count": len(failed_updates),
            "processed_updates": processed_updates,
            "failed_updates": failed_updates,
            "next_sync_recommended": (datetime.now().timestamp() + 3600)  # 1 hour
        }
    
    except Exception as e:
        logger.error(f"Error syncing offline updates: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to sync offline updates")

@mobile_router.get("/ai/insights/{project_id}", response_model=Dict[str, Any])
async def get_mobile_ai_insights(project_id: str, user=Depends(get_mobile_user)):
    """Get AI insights optimized for mobile display"""
    try:
        # TODO: Get actual project data
        mock_project_data = {
            "id": project_id,
            "completion_percentage": 65,
            "total_budget": 150000,
            "spent_amount": 95000,
            "planned_completion": "2025-07-15T00:00:00",
            "start_date": "2025-05-01T00:00:00",
            "team_members": [
                {"id": "tm1", "name": "John Smith", "utilization_percentage": 85, "is_critical": True},
                {"id": "tm2", "name": "Jane Doe", "utilization_percentage": 70, "is_critical": False}
            ]
        }
        
        # Get AI insights
        recommendations = await ai_project_manager.generate_project_recommendations(mock_project_data)
        
        # Simplify for mobile display
        mobile_insights = {
            "project_id": project_id,
            "health_score": recommendations.get("overall_health_score", 75),
            "status_summary": "On Track" if recommendations.get("overall_health_score", 75) > 70 else "Needs Attention",
            "key_insights": recommendations.get("insights", [])[:3],  # Top 3 insights only
            "priority_actions": recommendations.get("recommendations", {}).get("high_priority", [])[:3],
            "risk_count": recommendations.get("risks_count", 0),
            "last_updated": datetime.now().isoformat()
        }
        
        return mobile_insights
    
    except Exception as e:
        logger.error(f"Error getting mobile AI insights: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get AI insights")

@mobile_router.get("/workflows/active", response_model=Dict[str, Any])
async def get_active_workflows_mobile(user=Depends(get_mobile_user)):
    """Get active workflows optimized for mobile"""
    try:
        workflows = workflow_engine.list_active_workflows()
        
        # Simplify for mobile display
        mobile_workflows = []
        for workflow in workflows:
            mobile_workflows.append({
                "id": workflow["id"],
                "name": workflow["name"],
                "status": workflow["status"],
                "progress": workflow["progress"],
                "created_at": workflow["created_at"],
                "status_icon": "🔄" if workflow["status"] == "running" else "✅" if workflow["status"] == "completed" else "⏸️"
            })
        
        return {
            "workflows": mobile_workflows,
            "total_count": len(mobile_workflows),
            "active_count": len([w for w in workflows if w["status"] == "running"]),
            "last_updated": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting mobile workflows: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get workflows")

@mobile_router.get("/health", response_model=Dict[str, Any])
async def mobile_api_health():
    """Mobile API health check"""
    try:
        return {
            "status": "healthy",
            "service": "mobile_api",
            "version": "v1.0.0",
            "features": [
                "authentication",
                "project_management",
                "offline_sync",
                "ai_insights",
                "workflow_integration"
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Health check failed")

# Include router in the main FastAPI app
def include_mobile_routes(app):
    """Include mobile routes in FastAPI app"""
    app.include_router(mobile_router)
