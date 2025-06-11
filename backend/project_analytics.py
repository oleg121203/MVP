from typing import List, Dict, Any, Optional
import asyncio
import random
from datetime import datetime

class ProjectAnalytics:
    def __init__(self):
        self.project_db = None  # To be connected to project database

    async def connect_to_db(self, db_connection):
        """Connect to the project database"""
        self.project_db = db_connection
        return self

    async def generate_project_report(self, project_id: str, report_type: str = "summary") -> Dict[str, Any]:
        """Generate a project report based on the specified type"""
        if not self.project_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "report": {}
            }

        project_summary = await self.project_db.get_project_summary(project_id)
        if project_summary.get("status") != "success":
            return {
                "status": "error",
                "message": "Project summary not found",
                "report": {}
            }

        if report_type == "detailed":
            report = await self._generate_detailed_report(project_summary)
        elif report_type == "comparative":
            report = await self._generate_comparative_report(project_summary)
        else:
            report = await self._generate_summary_report(project_summary)

        return {
            "status": "success",
            "message": f"{report_type.capitalize()} report generated",
            "project_id": project_id,
            "report_type": report_type,
            "report": report
        }

    async def _generate_summary_report(self, project_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary report for the project"""
        await asyncio.sleep(0.5)  # Simulate async processing

        project = project_summary.get("project", {})
        tasks = project_summary.get("tasks", [])
        resources = project_summary.get("resources", [])

        completed_tasks = sum(1 for task in tasks if task.get("status") == "Completed")
        total_tasks = len(tasks)
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            "project_name": project.get("name", "Unknown"),
            "project_status": project.get("status", "Unknown"),
            "start_date": project.get("start_date", "Not set"),
            "end_date": project.get("end_date", "Not set"),
            "budget": project.get("budget", 0.0),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress_percentage": round(progress, 2),
            "total_resources": len(resources),
            "report_generated": datetime.now().isoformat(),
            "summary": f"Project is {round(progress, 2)}% complete with {completed_tasks} out of {total_tasks} tasks done."
        }

    async def _generate_detailed_report(self, project_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed report for the project"""
        await asyncio.sleep(1)  # Simulate async processing

        project = project_summary.get("project", {})
        tasks = project_summary.get("tasks", [])
        resources = project_summary.get("resources", [])

        completed_tasks = sum(1 for task in tasks if task.get("status") == "Completed")
        total_tasks = len(tasks)
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        task_details = []
        for task in tasks:
            task_details.append({
                "task_id": task.get("task_id"),
                "name": task.get("name"),
                "status": task.get("status"),
                "start_date": task.get("start_date", "Not set"),
                "end_date": task.get("end_date", "Not set"),
                "assigned_to": task.get("assigned_to", "Unassigned"),
                "priority": task.get("priority", "Medium")
            })

        resource_details = []
        for resource in resources:
            resource_details.append({
                "resource_id": resource.get("resource_id"),
                "name": resource.get("name"),
                "type": resource.get("type"),
                "quantity": resource.get("quantity", 0),
                "status": resource.get("status", "Unknown")
            })

        return {
            "project_name": project.get("name", "Unknown"),
            "project_status": project.get("status", "Unknown"),
            "start_date": project.get("start_date", "Not set"),
            "end_date": project.get("end_date", "Not set"),
            "budget": project.get("budget", 0.0),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress_percentage": round(progress, 2),
            "total_resources": len(resources),
            "task_details": task_details,
            "resource_details": resource_details,
            "report_generated": datetime.now().isoformat(),
            "summary": f"Detailed report for project with {total_tasks} tasks and {len(resources)} resources."
        }

    async def _generate_comparative_report(self, project_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comparative report for the project"""
        await asyncio.sleep(0.5)  # Simulate async processing

        project = project_summary.get("project", {})
        tasks = project_summary.get("tasks", [])

        completed_tasks = sum(1 for task in tasks if task.get("status") == "Completed")
        in_progress_tasks = sum(1 for task in tasks if task.get("status") == "In Progress")
        not_started_tasks = sum(1 for task in tasks if task.get("status") == "Not Started")
        total_tasks = len(tasks)
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            "project_name": project.get("name", "Unknown"),
            "project_status": project.get("status", "Unknown"),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "not_started_tasks": not_started_tasks,
            "progress_percentage": round(progress, 2),
            "report_generated": datetime.now().isoformat(),
            "comparison": {
                "completed_vs_total": f"{completed_tasks} completed out of {total_tasks}",
                "in_progress_vs_total": f"{in_progress_tasks} in progress out of {total_tasks}",
                "not_started_vs_total": f"{not_started_tasks} not started out of {total_tasks}"
            },
            "summary": f"Comparative report showing task status distribution."
        }

    async def assess_project_health(self, project_id: str) -> Dict[str, Any]:
        """Assess the overall health of a project"""
        if not self.project_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "health": {}
            }

        project_summary = await self.project_db.get_project_summary(project_id)
        if project_summary.get("status") != "success":
            return {
                "status": "error",
                "message": "Project summary not found",
                "health": {}
            }

        health = await self._assess_health_with_ai(project_summary)
        return {
            "status": "success",
            "message": "Project health assessment completed",
            "project_id": project_id,
            "health": health
        }

    async def _assess_health_with_ai(self, project_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate AI-driven project health assessment"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        project = project_summary.get("project", {})
        tasks = project_summary.get("tasks", [])
        resources = project_summary.get("resources", [])

        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.get("status") == "Completed")
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        health_score = round(random.uniform(50, 90), 2) if progress > 0 else round(random.uniform(10, 50), 2)
        status = "Healthy" if health_score > 75 else "At Risk" if health_score > 50 else "Critical"

        issues = []
        if progress < 30 and total_tasks > 0:
            issues.append("Slow progress - consider revising timelines or resource allocation")
        if len(resources) < total_tasks / 2 and total_tasks > 0:
            issues.append("Insufficient resources - potential bottleneck ahead")

        return {
            "health_score": health_score,
            "status": status,
            "progress_percentage": round(progress, 2),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "total_resources": len(resources),
            "issues": issues,
            "recommendations": [
                "Review task prioritization and critical path",
                "Monitor resource utilization closely",
                "Consider stakeholder communication for updates"
            ],
            "assessment_date": datetime.now().isoformat()
        }

    async def predict_project_outcomes(self, project_id: str) -> Dict[str, Any]:
        """Predict potential project outcomes"""
        if not self.project_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "predictions": []
            }

        project_summary = await self.project_db.get_project_summary(project_id)
        if project_summary.get("status") != "success":
            return {
                "status": "error",
                "message": "Project summary not found",
                "predictions": []
            }

        predictions = await self._predict_outcomes_with_ai(project_summary)
        return {
            "status": "success",
            "message": "Project outcome predictions completed",
            "project_id": project_id,
            "predictions": predictions
        }

    async def _predict_outcomes_with_ai(self, project_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simulate AI-driven project outcome predictions"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        project = project_summary.get("project", {})
        tasks = project_summary.get("tasks", [])

        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.get("status") == "Completed")
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        base_confidence = min(0.9, max(0.5, progress / 100))

        return [
            {
                "scenario": "On-Time Completion",
                "probability": round(base_confidence * random.uniform(0.7, 0.9), 2),
                "description": "Project completes within the planned timeline",
                "factors": ["Current progress rate", "Resource availability"],
                "mitigation": "Maintain current momentum and monitor risks"
            },
            {
                "scenario": "Delayed Completion",
                "probability": round((1 - base_confidence) * random.uniform(0.6, 0.8), 2),
                "description": "Project completion extends beyond planned end date",
                "factors": ["Unforeseen task delays", "Resource constraints"],
                "mitigation": "Identify critical path tasks and allocate buffers"
            },
            {
                "scenario": "Budget Overrun",
                "probability": round(random.uniform(0.2, 0.5), 2),
                "description": "Project costs exceed planned budget",
                "factors": ["Unexpected resource costs", "Scope creep"],
                "mitigation": "Implement strict cost monitoring and change control"
            }
        ]

    async def get_analytics_recommendations(self, project_id: str) -> Dict[str, Any]:
        """Get AI-generated recommendations based on project analytics"""
        await asyncio.sleep(0.5)  # Simulate async processing

        return {
            "status": "success",
            "project_id": project_id,
            "recommendations": [
                "Focus on completing high-priority tasks to improve health score",
                "Review resource allocation for underperforming areas",
                "Conduct regular progress reviews to stay on track"
            ]
        }
