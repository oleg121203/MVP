from typing import List, Dict, Any, Optional
import asyncio
import random
from datetime import datetime

class ResourceAllocation:
    def __init__(self):
        self.project_db = None  # To be connected to project database

    async def connect_to_db(self, db_connection):
        """Connect to the project database"""
        self.project_db = db_connection
        return self

    async def allocate_resources(self, project_id: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Allocate resources to a project or specific task using AI-driven analysis"""
        if not self.project_db:
            return {
                "status": "error",
                "message": "No database connection established",
                "allocations": []
            }

        project_summary = await self.project_db.get_project_summary(project_id)
        if project_summary.get("status") != "success":
            return {
                "status": "error",
                "message": "Project summary not found",
                "allocations": []
            }

        allocations = await self._allocate_with_ai(project_summary, task_id)
        return allocations

    async def _allocate_with_ai(self, project_summary: Dict[str, Any], task_id: Optional[str] = None) -> Dict[str, Any]:
        """Simulate AI-driven resource allocation"""
        await asyncio.sleep(1)  # Simulate async AI processing

        resources = project_summary.get("resources", [])
        tasks = project_summary.get("tasks", [])
        allocations = []

        if task_id:
            target_tasks = [t for t in tasks if t.get("task_id") == task_id]
        else:
            target_tasks = tasks

        for task in target_tasks:
            for resource in resources:
                if resource.get("status") == "Available":
                    allocations.append({
                        "task_id": task.get("task_id"),
                        "task_name": task.get("name"),
                        "resource_id": resource.get("resource_id"),
                        "resource_name": resource.get("name"),
                        "quantity_allocated": min(resource.get("quantity", 0), random.uniform(1, 5)),
                        "allocation_date": datetime.now().isoformat(),
                        "confidence": round(random.uniform(0.7, 0.95), 2),
                        "notes": "AI-driven allocation based on task priority and resource availability"
                    })
                    # Update resource status for simulation
                    resource["status"] = "Allocated"

        return {
            "status": "success",
            "message": "AI-driven resource allocation completed",
            "project_id": project_summary.get("project", {}).get("project_id", "Unknown"),
            "allocations": allocations
        }

    async def optimize_resource_usage(self, project_id: str) -> Dict[str, Any]:
        """Optimize resource usage across a project"""
        if not self.project_db:
            return {
                "status": "error",
                "message": "No database connection established",
                "optimization": []
            }

        project_summary = await self.project_db.get_project_summary(project_id)
        if project_summary.get("status") != "success":
            return {
                "status": "error",
                "message": "Project summary not found",
                "optimization": []
            }

        optimization = await self._optimize_with_ai(project_summary)
        return optimization

    async def _optimize_with_ai(self, project_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate AI-driven resource usage optimization"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        resources = project_summary.get("resources", [])
        optimization = []

        for resource in resources:
            optimization.append({
                "resource_id": resource.get("resource_id"),
                "name": resource.get("name"),
                "current_status": resource.get("status"),
                "recommended_action": "Reallocate" if resource.get("status") == "Allocated" and random.random() > 0.7 else "Maintain",
                "usage_efficiency": round(random.uniform(0.5, 0.9), 2),
                "optimization_notes": "AI recommendation based on current project demands"
            })

        return {
            "status": "success",
            "message": "AI resource usage optimization completed",
            "project_id": project_summary.get("project", {}).get("project_id", "Unknown"),
            "optimization": optimization
        }

    async def predict_resource_needs(self, project_id: str) -> Dict[str, Any]:
        """Predict future resource needs for a project"""
        if not self.project_db:
            return {
                "status": "error",
                "message": "No database connection established",
                "predictions": []
            }

        project_summary = await self.project_db.get_project_summary(project_id)
        if project_summary.get("status") != "success":
            return {
                "status": "error",
                "message": "Project summary not found",
                "predictions": []
            }

        predictions = await self._predict_needs_with_ai(project_summary)
        return predictions

    async def _predict_needs_with_ai(self, project_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate AI prediction of resource needs"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        tasks = project_summary.get("tasks", [])
        predictions = []

        for task in tasks:
            if task.get("status") == "Not Started":
                predictions.append({
                    "task_id": task.get("task_id"),
                    "task_name": task.get("name"),
                    "predicted_resource_type": random.choice(["Personnel", "Equipment", "Software"]),
                    "predicted_quantity": round(random.uniform(1, 10), 2),
                    "timeframe": "Next 30 days",
                    "confidence": round(random.uniform(0.6, 0.85), 2),
                    "notes": "AI prediction based on task scope and timeline"
                })

        return {
            "status": "success",
            "message": "AI resource needs prediction completed",
            "project_id": project_summary.get("project", {}).get("project_id", "Unknown"),
            "predictions": predictions
        }

    async def get_allocation_recommendations(self, project_id: str) -> Dict[str, Any]:
        """Get AI-generated recommendations for resource allocation"""
        await asyncio.sleep(0.5)  # Simulate async processing

        return {
            "status": "success",
            "project_id": project_id,
            "recommendations": [
                "Prioritize critical path tasks for resource allocation",
                "Balance resource distribution to avoid overallocation",
                "Consider cross-training to increase resource flexibility"
            ]
        }
