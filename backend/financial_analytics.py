from typing import List, Dict, Any, Optional
import asyncio

class FinancialAnalytics:
    def __init__(self):
        self.financial_db = None  # To be connected to financial database

    async def connect_to_db(self, db_connection):
        """Connect to the financial database"""
        self.financial_db = db_connection
        return self

    async def generate_financial_report(self, project_ids: List[str] = None, report_type: str = "summary") -> Dict[str, Any]:
        """Generate financial performance reports for specified projects or all projects"""
        if not self.financial_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "report": {}
            }

        if project_ids:
            projects_data = []
            for project_id in project_ids:
                project_data = await self._get_project_financial_data(project_id)
                if project_data.get("status") == "success":
                    projects_data.append(project_data)
        else:
            # If no specific projects provided, generate for all projects in database
            # This is a placeholder for fetching all project IDs from a project database
            projects_data = await self._get_all_projects_data()

        if not projects_data:
            return {
                "status": "error",
                "message": "No financial data available for reporting",
                "report": {}
            }

        if report_type == "detailed":
            report = await self._generate_detailed_report(projects_data)
        elif report_type == "comparative":
            report = await self._generate_comparative_report(projects_data)
        else:  # summary is default
            report = await self._generate_summary_report(projects_data)

        return {
            "status": "success",
            "message": f"Financial {report_type} report generated for {len(projects_data)} projects",
            "report": report
        }

    async def _get_project_financial_data(self, project_id: str) -> Dict[str, Any]:
        """Retrieve financial data for a specific project"""
        # Simulate async database operation
        await asyncio.sleep(0.5)
        return self.financial_db.get_financial_summary(project_id) if self.financial_db else {"status": "error"}

    async def _get_all_projects_data(self) -> List[Dict[str, Any]]:
        """Retrieve financial data for all projects - placeholder for actual implementation"""
        # Simulate async database operation
        await asyncio.sleep(0.5)
        # Dummy data for demonstration
        return [
            {
                "status": "success",
                "project_id": "proj-001",
                "budget": {"total_amount": 500000.0},
                "total_expenses": 325000.0,
                "remaining_budget": 175000.0,
                "transactions": {"income": 400000.0, "expense": -325000.0}
            },
            {
                "status": "success",
                "project_id": "proj-002",
                "budget": {"total_amount": 750000.0},
                "total_expenses": 600000.0,
                "remaining_budget": 150000.0,
                "transactions": {"income": 700000.0, "expense": -600000.0}
            }
        ]

    async def _generate_summary_report(self, projects_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary financial report across projects"""
        # Simulate processing delay
        await asyncio.sleep(0.5)

        total_projects = len(projects_data)
        total_budget = sum(p.get("budget", {}).get("total_amount", 0.0) for p in projects_data)
        total_expenses = sum(p.get("total_expenses", 0.0) for p in projects_data)
        total_remaining = sum(p.get("remaining_budget", 0.0) for p in projects_data)

        return {
            "report_type": "summary",
            "total_projects": total_projects,
            "total_budget": total_budget,
            "total_expenses": total_expenses,
            "total_remaining_budget": total_remaining,
            "average_budget_utilization": (total_expenses / total_budget * 100) if total_budget > 0 else 0.0,
            "key_insights": [
                f"Average budget utilization across projects: {round((total_expenses / total_budget * 100) if total_budget > 0 else 0.0, 1)}%",
                f"Remaining budget across all projects: ${total_remaining:,.2f}"
            ],
            "project_summaries": [
                {
                    "project_id": p.get("project_id", "Unknown"),
                    "budget": p.get("budget", {}).get("total_amount", 0.0),
                    "expenses": p.get("total_expenses", 0.0),
                    "remaining": p.get("remaining_budget", 0.0),
                    "utilization_percent": (p.get("total_expenses", 0.0) / p.get("budget", {}).get("total_amount", 0.0) * 100) if p.get("budget", {}).get("total_amount", 0.0) > 0 else 0.0
                }
                for p in projects_data
            ]
        }

    async def _generate_detailed_report(self, projects_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a detailed financial report for each project"""
        # Simulate processing delay
        await asyncio.sleep(0.5)

        project_details = []
        for project in projects_data:
            project_details.append({
                "project_id": project.get("project_id", "Unknown"),
                "budget_details": project.get("budget", {}),
                "total_expenses": project.get("total_expenses", 0.0),
                "remaining_budget": project.get("remaining_budget", 0.0),
                "transaction_summary": project.get("transactions", {}),
                "financial_health": self._assess_financial_health(project),
                "recommendations": self._generate_project_recommendations(project)
            })

        return {
            "report_type": "detailed",
            "total_projects": len(projects_data),
            "project_details": project_details
        }

    async def _generate_comparative_report(self, projects_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a comparative financial report across projects"""
        # Simulate processing delay
        await asyncio.sleep(0.5)

        if len(projects_data) < 2:
            return {
                "report_type": "comparative",
                "error": "Insufficient data",
                "message": "Comparative reports require data from at least 2 projects",
                "comparisons": []
            }

        total_budget = sum(p.get("budget", {}).get("total_amount", 0.0) for p in projects_data)
        total_expenses = sum(p.get("total_expenses", 0.0) for p in projects_data)
        count = len(projects_data)

        return {
            "report_type": "comparative",
            "total_projects": count,
            "average_budget": total_budget / count if count > 0 else 0.0,
            "average_expenses": total_expenses / count if count > 0 else 0.0,
            "comparisons": {
                "budget_utilization": [
                    {
                        "project_id": p.get("project_id", "Unknown"),
                        "utilization_percent": (p.get("total_expenses", 0.0) / p.get("budget", {}).get("total_amount", 0.0) * 100) if p.get("budget", {}).get("total_amount", 0.0) > 0 else 0.0,
                        "comparison_to_average": self._compare_to_average(p.get("total_expenses", 0.0), total_expenses / count if count > 0 else 0.0)
                    }
                    for p in projects_data
                ],
                "remaining_budget": [
                    {
                        "project_id": p.get("project_id", "Unknown"),
                        "remaining": p.get("remaining_budget", 0.0),
                        "comparison_to_average": self._compare_to_average(p.get("remaining_budget", 0.0), total_remaining / count if count > 0 else 0.0)
                    }
                    for p in projects_data
                    if (total_remaining := sum(p.get("remaining_budget", 0.0) for p in projects_data)) or True
                ]
            },
            "key_findings": self._generate_comparative_findings(projects_data)
        }

    def _compare_to_average(self, value: float, average: float) -> str:
        """Helper method to generate comparison text"""
        if average == 0:
            return "N/A (no average available)"
        percent_diff = ((value - average) / average * 100) if average != 0 else 0
        if percent_diff > 10:
            return f"{round(percent_diff, 1)}% above average"
        elif percent_diff < -10:
            return f"{abs(round(percent_diff, 1))}% below average"
        else:
            return "near average"

    def _assess_financial_health(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the financial health of a project based on available data"""
        budget = project_data.get("budget", {}).get("total_amount", 0.0)
        expenses = project_data.get("total_expenses", 0.0)
        remaining = project_data.get("remaining_budget", 0.0)

        if budget == 0:
            return {"health": "unknown", "reason": "No budget data available", "score": 0.0}

        utilization = (expenses / budget * 100) if budget > 0 else 0.0
        if utilization > 100:
            return {
                "health": "critical",
                "reason": "Project is over budget",
                "score": 0.2
            }
        elif utilization > 90:
            return {
                "health": "warning",
                "reason": "Project is nearing budget limit",
                "score": 0.4
            }
        elif utilization > 70:
            return {
                "health": "caution",
                "reason": "Significant budget portion used",
                "score": 0.6
            }
        elif utilization > 50:
            return {
                "health": "moderate",
                "reason": "Moderate budget utilization",
                "score": 0.7
            }
        else:
            return {
                "health": "good",
                "reason": "Project within safe budget range",
                "score": 0.9
            }

    def _generate_project_recommendations(self, project_data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on project financial status"""
        health_assessment = self._assess_financial_health(project_data)
        recommendations = []

        if health_assessment["health"] == "critical":
            recommendations.extend([
                "Immediate budget review required",
                "Identify and halt non-critical expenses",
                "Seek additional funding or budget reallocation"
            ])
        elif health_assessment["health"] == "warning":
            recommendations.extend([
                "Review upcoming expenses for potential savings",
                "Prioritize critical spending only",
                "Prepare contingency funding plan"
            ])
        elif health_assessment["health"] == "caution":
            recommendations.extend([
                "Monitor spending closely for next period",
                "Identify potential cost-saving opportunities",
                "Review project scope for budget alignment"
            ])
        else:  # moderate or good
            recommendations.extend([
                "Maintain current spending patterns",
                "Document successful cost management practices",
                "Consider strategic investments within budget"
            ])

        return recommendations

    def _generate_comparative_findings(self, projects_data: List[Dict[str, Any]]) -> List[str]:
        """Generate key findings from comparative analysis"""
        if len(projects_data) < 2:
            return ["Insufficient data for comparative analysis"]

        # Calculate some basic comparative metrics
        budget_utilizations = [(p.get("total_expenses", 0.0) / p.get("budget", {}).get("total_amount", 1.0) * 100) if p.get("budget", {}).get("total_amount", 0.0) > 0 else 0.0 for p in projects_data]
        highest_utilization = max(budget_utilizations) if budget_utilizations else 0.0
        lowest_utilization = min(budget_utilizations) if budget_utilizations else 0.0
        highest_project = projects_data[budget_utilizations.index(highest_utilization)].get("project_id", "Unknown") if budget_utilizations else "N/A"
        lowest_project = projects_data[budget_utilizations.index(lowest_utilization)].get("project_id", "Unknown") if budget_utilizations else "N/A"

        return [
            f"Highest budget utilization: Project {highest_project} at {round(highest_utilization, 1)}%",
            f"Lowest budget utilization: Project {lowest_project} at {round(lowest_utilization, 1)}%",
            f"Range of budget utilization across projects: {round(highest_utilization - lowest_utilization, 1)} percentage points"
        ]
