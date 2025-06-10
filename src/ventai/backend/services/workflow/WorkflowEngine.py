"""
Workflow Automation Engine for VentAI Enterprise
Implements automated business processes and AI-powered workflow management
"""
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import asyncio
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class WorkflowTask:
    """Individual task within a workflow"""
    id: str
    name: str
    description: str
    task_type: str
    priority: TaskPriority
    estimated_duration: int  # minutes
    dependencies: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: WorkflowStatus = WorkflowStatus.PENDING
    assigned_to: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

@dataclass
class Workflow:
    """Complete workflow definition"""
    id: str
    name: str
    description: str
    category: str
    tasks: List[WorkflowTask] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_by: str = "system"
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    context: Dict[str, Any] = field(default_factory=dict)

class WorkflowEngine:
    """Core workflow automation engine"""
    
    def __init__(self):
        self.active_workflows: Dict[str, Workflow] = {}
        self.task_handlers: Dict[str, Callable] = {}
        self.workflow_templates: Dict[str, Dict[str, Any]] = {}
        self._load_workflow_templates()
    
    def _load_workflow_templates(self):
        """Load predefined workflow templates"""
        self.workflow_templates = {
            "project_creation": {
                "name": "Project Creation Workflow",
                "description": "Automated workflow for new project setup",
                "tasks": [
                    {
                        "id": "validate_project_data",
                        "name": "Validate Project Data",
                        "task_type": "validation",
                        "priority": TaskPriority.HIGH,
                        "estimated_duration": 5
                    },
                    {
                        "id": "create_project_structure",
                        "name": "Create Project Structure",
                        "task_type": "creation",
                        "priority": TaskPriority.HIGH,
                        "estimated_duration": 10,
                        "dependencies": ["validate_project_data"]
                    },
                    {
                        "id": "setup_ai_analysis",
                        "name": "Setup AI Analysis",
                        "task_type": "ai_setup",
                        "priority": TaskPriority.MEDIUM,
                        "estimated_duration": 15,
                        "dependencies": ["create_project_structure"]
                    },
                    {
                        "id": "generate_initial_recommendations",
                        "name": "Generate Initial AI Recommendations",
                        "task_type": "ai_analysis",
                        "priority": TaskPriority.MEDIUM,
                        "estimated_duration": 20,
                        "dependencies": ["setup_ai_analysis"]
                    },
                    {
                        "id": "notify_stakeholders",
                        "name": "Notify Stakeholders",
                        "task_type": "notification",
                        "priority": TaskPriority.LOW,
                        "estimated_duration": 5,
                        "dependencies": ["generate_initial_recommendations"]
                    }
                ]
            },
            "compliance_check": {
                "name": "Automated Compliance Check",
                "description": "Check project compliance with Ukrainian standards",
                "tasks": [
                    {
                        "id": "extract_project_specifications",
                        "name": "Extract Project Specifications",
                        "task_type": "data_extraction",
                        "priority": TaskPriority.HIGH,
                        "estimated_duration": 10
                    },
                    {
                        "id": "check_dbn_compliance",
                        "name": "Check DBN Compliance",
                        "task_type": "compliance_check",
                        "priority": TaskPriority.CRITICAL,
                        "estimated_duration": 30,
                        "dependencies": ["extract_project_specifications"]
                    },
                    {
                        "id": "generate_compliance_report",
                        "name": "Generate Compliance Report",
                        "task_type": "report_generation",
                        "priority": TaskPriority.HIGH,
                        "estimated_duration": 15,
                        "dependencies": ["check_dbn_compliance"]
                    },
                    {
                        "id": "send_compliance_alerts",
                        "name": "Send Compliance Alerts",
                        "task_type": "notification",
                        "priority": TaskPriority.MEDIUM,
                        "estimated_duration": 5,
                        "dependencies": ["generate_compliance_report"]
                    }
                ]
            },
            "cost_optimization": {
                "name": "Cost Optimization Workflow",
                "description": "Automated cost analysis and optimization recommendations",
                "tasks": [
                    {
                        "id": "analyze_project_costs",
                        "name": "Analyze Project Costs",
                        "task_type": "cost_analysis",
                        "priority": TaskPriority.HIGH,
                        "estimated_duration": 20
                    },
                    {
                        "id": "research_alternative_materials",
                        "name": "Research Alternative Materials",
                        "task_type": "market_research",
                        "priority": TaskPriority.MEDIUM,
                        "estimated_duration": 25,
                        "dependencies": ["analyze_project_costs"]
                    },
                    {
                        "id": "calculate_savings_potential",
                        "name": "Calculate Savings Potential",
                        "task_type": "calculation",
                        "priority": TaskPriority.HIGH,
                        "estimated_duration": 15,
                        "dependencies": ["research_alternative_materials"]
                    },
                    {
                        "id": "generate_optimization_report",
                        "name": "Generate Optimization Report",
                        "task_type": "report_generation",
                        "priority": TaskPriority.MEDIUM,
                        "estimated_duration": 20,
                        "dependencies": ["calculate_savings_potential"]
                    }
                ]
            }
        }
    
    def register_task_handler(self, task_type: str, handler: Callable):
        """Register a handler for specific task types"""
        self.task_handlers[task_type] = handler
        logger.info(f"Registered handler for task type: {task_type}")
    
    def create_workflow_from_template(self, 
                                    template_id: str, 
                                    workflow_id: str,
                                    context: Dict[str, Any] = None) -> Workflow:
        """Create a new workflow from a template"""
        if template_id not in self.workflow_templates:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.workflow_templates[template_id]
        
        # Create workflow tasks from template
        tasks = []
        for task_data in template["tasks"]:
            task = WorkflowTask(
                id=task_data["id"],
                name=task_data["name"],
                description=task_data.get("description", ""),
                task_type=task_data["task_type"],
                priority=task_data["priority"],
                estimated_duration=task_data["estimated_duration"],
                dependencies=task_data.get("dependencies", []),
                parameters=task_data.get("parameters", {})
            )
            tasks.append(task)
        
        # Create workflow
        workflow = Workflow(
            id=workflow_id,
            name=template["name"],
            description=template["description"],
            category=template_id,
            tasks=tasks,
            context=context or {}
        )
        
        self.active_workflows[workflow_id] = workflow
        logger.info(f"Created workflow {workflow_id} from template {template_id}")
        
        return workflow
    
    async def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a workflow asynchronously"""
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        
        try:
            # Execute tasks in dependency order
            while True:
                # Find next executable task
                next_task = self._find_next_executable_task(workflow)
                if not next_task:
                    break
                
                # Execute the task
                await self._execute_task(workflow, next_task)
                
                # Check if workflow is completed
                if all(task.status == WorkflowStatus.COMPLETED for task in workflow.tasks):
                    workflow.status = WorkflowStatus.COMPLETED
                    workflow.completed_at = datetime.now()
                    break
                
                # Check for failed tasks
                failed_tasks = [task for task in workflow.tasks if task.status == WorkflowStatus.FAILED]
                if failed_tasks:
                    workflow.status = WorkflowStatus.FAILED
                    logger.error(f"Workflow {workflow_id} failed due to task failures")
                    return False
            
            logger.info(f"Workflow {workflow_id} completed successfully")
            return True
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            logger.error(f"Workflow {workflow_id} failed with error: {str(e)}")
            return False
    
    def _find_next_executable_task(self, workflow: Workflow) -> Optional[WorkflowTask]:
        """Find the next task that can be executed"""
        for task in workflow.tasks:
            if task.status == WorkflowStatus.PENDING:
                # Check if all dependencies are completed
                dependencies_completed = all(
                    any(t.id == dep_id and t.status == WorkflowStatus.COMPLETED 
                        for t in workflow.tasks)
                    for dep_id in task.dependencies
                )
                
                if not task.dependencies or dependencies_completed:
                    return task
        
        return None
    
    async def _execute_task(self, workflow: Workflow, task: WorkflowTask):
        """Execute a specific task"""
        task.status = WorkflowStatus.RUNNING
        task.started_at = datetime.now()
        
        try:
            # Get task handler
            if task.task_type not in self.task_handlers:
                raise ValueError(f"No handler registered for task type: {task.task_type}")
            
            handler = self.task_handlers[task.task_type]
            
            # Execute task with workflow context
            task_context = {
                **workflow.context,
                **task.parameters,
                "workflow_id": workflow.id,
                "task_id": task.id
            }
            
            result = await handler(task_context)
            task.result = result
            task.status = WorkflowStatus.COMPLETED
            task.completed_at = datetime.now()
            
            logger.info(f"Task {task.id} completed successfully")
            
        except Exception as e:
            task.status = WorkflowStatus.FAILED
            task.error_message = str(e)
            task.completed_at = datetime.now()
            logger.error(f"Task {task.id} failed: {str(e)}")
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get detailed workflow status"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        return {
            "id": workflow.id,
            "name": workflow.name,
            "status": workflow.status.value,
            "created_at": workflow.created_at.isoformat(),
            "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
            "progress": self._calculate_workflow_progress(workflow),
            "tasks": [
                {
                    "id": task.id,
                    "name": task.name,
                    "status": task.status.value,
                    "priority": task.priority.value,
                    "estimated_duration": task.estimated_duration,
                    "started_at": task.started_at.isoformat() if task.started_at else None,
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                    "error_message": task.error_message
                }
                for task in workflow.tasks
            ]
        }
    
    def _calculate_workflow_progress(self, workflow: Workflow) -> float:
        """Calculate workflow completion percentage"""
        if not workflow.tasks:
            return 0.0
        
        completed_tasks = len([task for task in workflow.tasks if task.status == WorkflowStatus.COMPLETED])
        return (completed_tasks / len(workflow.tasks)) * 100
    
    def list_active_workflows(self) -> List[Dict[str, Any]]:
        """List all active workflows"""
        return [
            {
                "id": workflow.id,
                "name": workflow.name,
                "status": workflow.status.value,
                "progress": self._calculate_workflow_progress(workflow),
                "created_at": workflow.created_at.isoformat()
            }
            for workflow in self.active_workflows.values()
        ]
    
    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow"""
        if workflow_id not in self.active_workflows:
            return False
        
        workflow = self.active_workflows[workflow_id]
        if workflow.status == WorkflowStatus.RUNNING:
            workflow.status = WorkflowStatus.CANCELLED
            
            # Cancel running tasks
            for task in workflow.tasks:
                if task.status == WorkflowStatus.RUNNING:
                    task.status = WorkflowStatus.CANCELLED
            
            logger.info(f"Workflow {workflow_id} cancelled")
            return True
        
        return False

# Singleton workflow engine instance
workflow_engine = WorkflowEngine()

async def sample_task_handlers():
    """Sample task handlers for demonstration"""
    
    async def validate_project_data(context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate project data"""
        await asyncio.sleep(1)  # Simulate processing
        return {"status": "valid", "validation_score": 0.95}
    
    async def create_project_structure(context: Dict[str, Any]) -> Dict[str, Any]:
        """Create project structure in database"""
        await asyncio.sleep(2)  # Simulate processing
        return {"project_id": "PROJ-001", "status": "created"}
    
    async def setup_ai_analysis(context: Dict[str, Any]) -> Dict[str, Any]:
        """Setup AI analysis for project"""
        await asyncio.sleep(3)  # Simulate processing
        return {"ai_model_initialized": True, "analysis_ready": True}
    
    async def generate_initial_recommendations(context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI recommendations"""
        await asyncio.sleep(4)  # Simulate processing
        return {
            "recommendations": [
                {"type": "cost_saving", "description": "Use alternative material X", "savings": 15.5},
                {"type": "compliance", "description": "Update insulation specs", "priority": "high"}
            ]
        }
    
    async def notify_stakeholders(context: Dict[str, Any]) -> Dict[str, Any]:
        """Send notifications to stakeholders"""
        await asyncio.sleep(1)  # Simulate processing
        return {"notifications_sent": 3, "delivery_status": "success"}
    
    # Register handlers
    workflow_engine.register_task_handler("validation", validate_project_data)
    workflow_engine.register_task_handler("creation", create_project_structure)
    workflow_engine.register_task_handler("ai_setup", setup_ai_analysis)
    workflow_engine.register_task_handler("ai_analysis", generate_initial_recommendations)
    workflow_engine.register_task_handler("notification", notify_stakeholders)

if __name__ == "__main__":
    # Example usage
    async def main():
        # Register sample handlers
        await sample_task_handlers()
        
        # Create and execute a workflow
        workflow = workflow_engine.create_workflow_from_template(
            "project_creation",
            "test_workflow_001",
            {"project_name": "Test HVAC Project", "client_id": "CLIENT-001"}
        )
        
        print(f"Created workflow: {workflow.name}")
        print(f"Tasks: {len(workflow.tasks)}")
        
        # Execute workflow
        success = await workflow_engine.execute_workflow("test_workflow_001")
        print(f"Workflow execution result: {success}")
        
        # Get status
        status = workflow_engine.get_workflow_status("test_workflow_001")
        print(f"Final status: {json.dumps(status, indent=2)}")
    
    asyncio.run(main())
