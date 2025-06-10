"""
FastAPI endpoints for Workflow Automation Engine
Provides REST API for workflow management and execution
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime

from ventai.backend.services.workflow.WorkflowEngine import workflow_engine, WorkflowStatus, TaskPriority

# API Router
workflow_router = APIRouter(prefix="/api/workflow", tags=["workflow"])

# Request/Response Models
class CreateWorkflowRequest(BaseModel):
    template_id: str
    workflow_id: str
    context: Optional[Dict[str, Any]] = None

class WorkflowResponse(BaseModel):
    id: str
    name: str
    status: str
    progress: float
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    name: str
    status: str
    priority: int
    estimated_duration: int
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None

class WorkflowDetailResponse(BaseModel):
    id: str
    name: str
    status: str
    progress: float
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    tasks: List[TaskResponse]

@workflow_router.get("/templates", response_model=Dict[str, Any])
async def get_workflow_templates():
    """Get available workflow templates"""
    try:
        templates = {}
        for template_id, template_data in workflow_engine.workflow_templates.items():
            templates[template_id] = {
                "name": template_data["name"],
                "description": template_data["description"],
                "task_count": len(template_data["tasks"]),
                "estimated_duration": sum(task["estimated_duration"] for task in template_data["tasks"])
            }
        
        return {
            "success": True,
            "templates": templates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get templates: {str(e)}")

@workflow_router.post("/create", response_model=Dict[str, Any])
async def create_workflow(request: CreateWorkflowRequest):
    """Create a new workflow from template"""
    try:
        workflow = workflow_engine.create_workflow_from_template(
            request.template_id,
            request.workflow_id,
            request.context
        )
        
        return {
            "success": True,
            "workflow": {
                "id": workflow.id,
                "name": workflow.name,
                "status": workflow.status.value,
                "task_count": len(workflow.tasks),
                "created_at": workflow.created_at.isoformat()
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")

@workflow_router.post("/execute/{workflow_id}", response_model=Dict[str, Any])
async def execute_workflow(workflow_id: str, background_tasks: BackgroundTasks):
    """Execute a workflow asynchronously"""
    try:
        if workflow_id not in workflow_engine.active_workflows:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Execute workflow in background
        background_tasks.add_task(workflow_engine.execute_workflow, workflow_id)
        
        return {
            "success": True,
            "message": f"Workflow {workflow_id} execution started",
            "workflow_id": workflow_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")

@workflow_router.get("/status/{workflow_id}", response_model=WorkflowDetailResponse)
async def get_workflow_status(workflow_id: str):
    """Get detailed workflow status"""
    try:
        status = workflow_engine.get_workflow_status(workflow_id)
        
        if "error" in status:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return WorkflowDetailResponse(**status)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workflow status: {str(e)}")

@workflow_router.get("/list", response_model=List[WorkflowResponse])
async def list_workflows():
    """List all active workflows"""
    try:
        workflows = workflow_engine.list_active_workflows()
        return [WorkflowResponse(**workflow) for workflow in workflows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")

@workflow_router.post("/cancel/{workflow_id}", response_model=Dict[str, Any])
async def cancel_workflow(workflow_id: str):
    """Cancel a running workflow"""
    try:
        success = workflow_engine.cancel_workflow(workflow_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Workflow not found or cannot be cancelled")
        
        return {
            "success": True,
            "message": f"Workflow {workflow_id} cancelled successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel workflow: {str(e)}")

@workflow_router.get("/health", response_model=Dict[str, Any])
async def workflow_health_check():
    """Health check for workflow service"""
    try:
        active_count = len(workflow_engine.active_workflows)
        template_count = len(workflow_engine.workflow_templates)
        handler_count = len(workflow_engine.task_handlers)
        
        return {
            "status": "healthy",
            "active_workflows": active_count,
            "available_templates": template_count,
            "registered_handlers": handler_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@workflow_router.post("/test/create-and-execute", response_model=Dict[str, Any])
async def test_create_and_execute(background_tasks: BackgroundTasks):
    """Test endpoint to create and execute a sample workflow"""
    try:
        # Create test workflow
        workflow_id = f"test_workflow_{int(datetime.now().timestamp())}"
        workflow = workflow_engine.create_workflow_from_template(
            "project_creation",
            workflow_id,
            {
                "project_name": "Test HVAC Project",
                "client_id": "CLIENT-TEST-001",
                "project_type": "commercial"
            }
        )
        
        # Execute in background
        background_tasks.add_task(workflow_engine.execute_workflow, workflow_id)
        
        return {
            "success": True,
            "message": "Test workflow created and execution started",
            "workflow_id": workflow_id,
            "workflow_name": workflow.name,
            "task_count": len(workflow.tasks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test workflow failed: {str(e)}")

# Workflow Analytics Endpoints
@workflow_router.get("/analytics/summary", response_model=Dict[str, Any])
async def get_workflow_analytics():
    """Get workflow execution analytics"""
    try:
        workflows = workflow_engine.active_workflows.values()
        
        total_workflows = len(workflows)
        completed_workflows = len([w for w in workflows if w.status == WorkflowStatus.COMPLETED])
        failed_workflows = len([w for w in workflows if w.status == WorkflowStatus.FAILED])
        running_workflows = len([w for w in workflows if w.status == WorkflowStatus.RUNNING])
        
        # Calculate average completion time for completed workflows
        completed_times = [
            (w.completed_at - w.started_at).total_seconds() / 60
            for w in workflows
            if w.status == WorkflowStatus.COMPLETED and w.started_at and w.completed_at
        ]
        avg_completion_time = sum(completed_times) / len(completed_times) if completed_times else 0
        
        return {
            "total_workflows": total_workflows,
            "completed_workflows": completed_workflows,
            "failed_workflows": failed_workflows,
            "running_workflows": running_workflows,
            "success_rate": (completed_workflows / total_workflows * 100) if total_workflows > 0 else 0,
            "average_completion_time_minutes": round(avg_completion_time, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

@workflow_router.get("/analytics/templates", response_model=Dict[str, Any])
async def get_template_usage_analytics():
    """Get template usage analytics"""
    try:
        workflows = workflow_engine.active_workflows.values()
        
        template_usage = {}
        for workflow in workflows:
            category = workflow.category
            if category not in template_usage:
                template_usage[category] = {
                    "count": 0,
                    "completed": 0,
                    "failed": 0,
                    "success_rate": 0
                }
            
            template_usage[category]["count"] += 1
            if workflow.status == WorkflowStatus.COMPLETED:
                template_usage[category]["completed"] += 1
            elif workflow.status == WorkflowStatus.FAILED:
                template_usage[category]["failed"] += 1
        
        # Calculate success rates
        for template_data in template_usage.values():
            total = template_data["count"]
            if total > 0:
                template_data["success_rate"] = (template_data["completed"] / total) * 100
        
        return {
            "template_usage": template_usage,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get template analytics: {str(e)}")

# Include router in the main FastAPI app
def include_workflow_routes(app):
    """Include workflow routes in FastAPI app"""
    app.include_router(workflow_router)
