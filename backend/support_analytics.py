from typing import List, Dict, Any, Optional
import asyncio
import random
from datetime import datetime, timedelta

class SupportAnalytics:
    def __init__(self):
        self.support_db = None  # To be connected to customer support database

    async def connect_to_db(self, db_connection):
        """Connect to the customer support database"""
        self.support_db = db_connection
        return self

    async def generate_support_report(self, report_type: str = "summary", start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Generate a support performance report"""
        if not self.support_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "report": {}
            }

        # Default to last 30 days if no date range is provided
        if end_date is None:
            end_date_dt = datetime.now()
        else:
            end_date_dt = datetime.fromisoformat(end_date)
        
        if start_date is None:
            start_date_dt = end_date_dt - timedelta(days=30)
        else:
            start_date_dt = datetime.fromisoformat(start_date)

        tickets_response = await self._get_tickets_in_range(start_date_dt, end_date_dt)
        if tickets_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Failed to retrieve tickets for report",
                "report": {}
            }

        tickets = tickets_response.get("tickets", [])
        if report_type == "detailed":
            report = await self._generate_detailed_report(tickets, start_date_dt, end_date_dt)
        elif report_type == "performance":
            report = await self._generate_performance_report(tickets, start_date_dt, end_date_dt)
        else:
            report = await self._generate_summary_report(tickets, start_date_dt, end_date_dt)

        return {
            "status": "success",
            "message": f"{report_type.capitalize()} support report generated",
            "report_type": report_type,
            "start_date": start_date_dt.isoformat(),
            "end_date": end_date_dt.isoformat(),
            "report": report
        }

    async def _get_tickets_in_range(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get tickets within a date range - simulation"""
        await asyncio.sleep(0.5)  # Simulate async processing
        
        # In a real implementation, this would query the database with date filters
        # For simulation, we'll get all tickets and filter in code
        all_tickets_response = self.support_db.get_all_tickets()
        if all_tickets_response.get("status") != "success":
            return all_tickets_response

        all_tickets = all_tickets_response.get("tickets", [])
        filtered_tickets = []
        for ticket in all_tickets:
            try:
                created_at = datetime.fromisoformat(ticket.get("created_at", "1970-01-01T00:00:00"))
                if start_date <= created_at <= end_date:
                    filtered_tickets.append(ticket)
            except ValueError:
                # Skip tickets with invalid date format
                continue

        return {"status": "success", "tickets": filtered_tickets}

    async def _generate_summary_report(self, tickets: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate a summary report for support tickets"""
        await asyncio.sleep(0.5)  # Simulate async processing

        total_tickets = len(tickets)
        open_tickets = sum(1 for t in tickets if t.get("status") == "Open")
        in_progress_tickets = sum(1 for t in tickets if t.get("status") == "In Progress")
        closed_tickets = sum(1 for t in tickets if t.get("status") == "Closed")
        
        high_priority = sum(1 for t in tickets if t.get("priority") == "High")
        medium_priority = sum(1 for t in tickets if t.get("priority") == "Medium")
        low_priority = sum(1 for t in tickets if t.get("priority") == "Low")

        categories = {}
        for t in tickets:
            cat = t.get("category", "Uncategorized")
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "closed_tickets": closed_tickets,
            "closure_rate": round((closed_tickets / total_tickets * 100) if total_tickets > 0 else 0, 2),
            "priority_distribution": {
                "high": high_priority,
                "medium": medium_priority,
                "low": low_priority
            },
            "category_distribution": categories,
            "report_generated": datetime.now().isoformat(),
            "summary": f"Support summary for {total_tickets} tickets from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        }

    async def _generate_detailed_report(self, tickets: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate a detailed report for support tickets"""
        await asyncio.sleep(1)  # Simulate async processing

        total_tickets = len(tickets)
        open_tickets = sum(1 for t in tickets if t.get("status") == "Open")
        in_progress_tickets = sum(1 for t in tickets if t.get("status") == "In Progress")
        closed_tickets = sum(1 for t in tickets if t.get("status") == "Closed")
        
        high_priority = sum(1 for t in tickets if t.get("priority") == "High")
        medium_priority = sum(1 for t in tickets if t.get("priority") == "Medium")
        low_priority = sum(1 for t in tickets if t.get("priority") == "Low")

        categories = {}
        ticket_details = []
        for t in tickets:
            cat = t.get("category", "Uncategorized")
            categories[cat] = categories.get(cat, 0) + 1
            
            ticket_details.append({
                "ticket_id": t.get("ticket_id"),
                "subject": t.get("subject"),
                "status": t.get("status"),
                "priority": t.get("priority"),
                "category": cat,
                "created_at": t.get("created_at", "N/A"),
                "updated_at": t.get("updated_at", "N/A"),
                "assigned_to": t.get("assigned_to", "Unassigned")
            })

        return {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "closed_tickets": closed_tickets,
            "closure_rate": round((closed_tickets / total_tickets * 100) if total_tickets > 0 else 0, 2),
            "priority_distribution": {
                "high": high_priority,
                "medium": medium_priority,
                "low": low_priority
            },
            "category_distribution": categories,
            "ticket_details": ticket_details[:50],  # Limit to 50 for brevity in simulation
            "report_generated": datetime.now().isoformat(),
            "summary": f"Detailed support report for {total_tickets} tickets from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        }

    async def _generate_performance_report(self, tickets: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate a performance report for support tickets"""
        await asyncio.sleep(0.5)  # Simulate async processing

        total_tickets = len(tickets)
        closed_tickets = sum(1 for t in tickets if t.get("status") == "Closed")
        
        # Calculate average resolution time for closed tickets
        resolution_times = []
        for t in tickets:
            if t.get("status") == "Closed":
                try:
                    created_at = datetime.fromisoformat(t.get("created_at", "1970-01-01T00:00:00"))
                    updated_at = datetime.fromisoformat(t.get("updated_at", "1970-01-01T00:00:00"))
                    if updated_at > created_at:
                        resolution_time = (updated_at - created_at).total_seconds() / 3600  # in hours
                        resolution_times.append(resolution_time)
                except ValueError:
                    continue

        avg_resolution_time = round(sum(resolution_times) / len(resolution_times), 2) if resolution_times else 0
        
        # Calculate resolution times by priority
        high_priority_times = []
        medium_priority_times = []
        low_priority_times = []
        for t in tickets:
            if t.get("status") == "Closed":
                try:
                    created_at = datetime.fromisoformat(t.get("created_at", "1970-01-01T00:00:00"))
                    updated_at = datetime.fromisoformat(t.get("updated_at", "1970-01-01T00:00:00"))
                    if updated_at > created_at:
                        resolution_time = (updated_at - created_at).total_seconds() / 3600  # in hours
                        if t.get("priority") == "High":
                            high_priority_times.append(resolution_time)
                        elif t.get("priority") == "Medium":
                            medium_priority_times.append(resolution_time)
                        elif t.get("priority") == "Low":
                            low_priority_times.append(resolution_time)
                except ValueError:
                    continue

        avg_high_priority_time = round(sum(high_priority_times) / len(high_priority_times), 2) if high_priority_times else 0
        avg_medium_priority_time = round(sum(medium_priority_times) / len(medium_priority_times), 2) if medium_priority_times else 0
        avg_low_priority_time = round(sum(low_priority_times) / len(low_priority_times), 2) if low_priority_times else 0

        return {
            "total_tickets": total_tickets,
            "closed_tickets": closed_tickets,
            "closure_rate": round((closed_tickets / total_tickets * 100) if total_tickets > 0 else 0, 2),
            "average_resolution_time_hours": avg_resolution_time,
            "resolution_time_by_priority": {
                "high": {
                    "average_hours": avg_high_priority_time,
                    "ticket_count": len(high_priority_times)
                },
                "medium": {
                    "average_hours": avg_medium_priority_time,
                    "ticket_count": len(medium_priority_times)
                },
                "low": {
                    "average_hours": avg_low_priority_time,
                    "ticket_count": len(low_priority_times)
                }
            },
            "report_generated": datetime.now().isoformat(),
            "summary": f"Support performance report from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        }

    async def analyze_customer_satisfaction(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Analyze customer satisfaction based on ticket interactions"""
        if not self.support_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "analysis": {}
            }

        # Default to last 30 days if no date range is provided
        if end_date is None:
            end_date_dt = datetime.now()
        else:
            end_date_dt = datetime.fromisoformat(end_date)
        
        if start_date is None:
            start_date_dt = end_date_dt - timedelta(days=30)
        else:
            start_date_dt = datetime.fromisoformat(start_date)

        tickets_response = await self._get_tickets_in_range(start_date_dt, end_date_dt)
        if tickets_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Failed to retrieve tickets for analysis",
                "analysis": {}
            }

        tickets = tickets_response.get("tickets", [])
        analysis = await self._analyze_satisfaction_with_ai(tickets, start_date_dt, end_date_dt)
        return {
            "status": "success",
            "message": "Customer satisfaction analysis completed",
            "start_date": start_date_dt.isoformat(),
            "end_date": end_date_dt.isoformat(),
            "analysis": analysis
        }

    async def _analyze_satisfaction_with_ai(self, tickets: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Simulate AI-driven customer satisfaction analysis"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        total_tickets = len(tickets)
        closed_tickets = sum(1 for t in tickets if t.get("status") == "Closed")

        # Simulated satisfaction score
        satisfaction_score = round(random.uniform(3.5, 4.5), 2) if closed_tickets > 0 else round(random.uniform(2.0, 3.5), 2)
        status = "Good" if satisfaction_score >= 4.0 else "Fair" if satisfaction_score >= 3.0 else "Poor"

        # Distribution of simulated ratings
        ratings = {
            "5_star": round(total_tickets * random.uniform(0.3, 0.5)) if total_tickets > 0 else 0,
            "4_star": round(total_tickets * random.uniform(0.2, 0.4)) if total_tickets > 0 else 0,
            "3_star": round(total_tickets * random.uniform(0.1, 0.2)) if total_tickets > 0 else 0,
            "2_star": round(total_tickets * random.uniform(0.05, 0.15)) if total_tickets > 0 else 0,
            "1_star": round(total_tickets * random.uniform(0.05, 0.1)) if total_tickets > 0 else 0
        }
        # Adjust for rounding errors to match total tickets
        ratings_sum = sum(ratings.values())
        if ratings_sum != total_tickets and total_tickets > 0:
            ratings["5_star"] += total_tickets - ratings_sum

        issues = []
        if satisfaction_score < 4.0:
            issues.append("Customer wait times may be longer than desired")
        if satisfaction_score < 3.5:
            issues.append("Resolution quality may not be meeting customer expectations")

        return {
            "satisfaction_score": satisfaction_score,
            "status": status,
            "total_tickets": total_tickets,
            "closed_tickets": closed_tickets,
            "rating_distribution": ratings,
            "issues": issues,
            "recommendations": [
                "Monitor ticket response times for improvement opportunities",
                "Review low-rated tickets for common resolution issues",
                "Consider customer follow-up surveys for more detailed feedback"
            ],
            "analysis_date": datetime.now().isoformat()
        }

    async def predict_support_trends(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Predict future support trends based on historical data"""
        if not self.support_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "predictions": []
            }

        # Default to last 30 days if no date range is provided
        if end_date is None:
            end_date_dt = datetime.now()
        else:
            end_date_dt = datetime.fromisoformat(end_date)
        
        if start_date is None:
            start_date_dt = end_date_dt - timedelta(days=30)
        else:
            start_date_dt = datetime.fromisoformat(start_date)

        tickets_response = await self._get_tickets_in_range(start_date_dt, end_date_dt)
        if tickets_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Failed to retrieve tickets for prediction",
                "predictions": []
            }

        tickets = tickets_response.get("tickets", [])
        predictions = await self._predict_trends_with_ai(tickets, start_date_dt, end_date_dt)
        return {
            "status": "success",
            "message": "Support trend predictions completed",
            "start_date": start_date_dt.isoformat(),
            "end_date": end_date_dt.isoformat(),
            "predictions": predictions
        }

    async def _predict_trends_with_ai(self, tickets: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Simulate AI-driven support trend prediction"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        total_tickets = len(tickets)
        base_confidence = min(0.9, max(0.5, total_tickets / 50))

        return [
            {
                "trend": "Increasing Technical Issues",
                "probability": round(base_confidence * random.uniform(0.6, 0.8), 2),
                "description": "Expected increase in technical support requests due to recent product updates",
                "factors": ["Recent feature releases", "Historical spike patterns"],
                "mitigation": "Prepare additional technical support resources"
            },
            {
                "trend": "Billing Inquiry Spike",
                "probability": round(base_confidence * random.uniform(0.5, 0.7), 2),
                "description": "Potential increase in billing inquiries during upcoming renewal period",
                "factors": ["Subscription renewal dates", "Historical billing trends"],
                "mitigation": "Enhance self-service billing options and documentation"
            },
            {
                "trend": "Seasonal Support Volume",
                "probability": round(base_confidence * random.uniform(0.7, 0.85), 2),
                "description": "Anticipated fluctuation in support volume due to seasonal patterns",
                "factors": ["Holiday periods", "Historical seasonal data"],
                "mitigation": "Adjust staffing levels to match predicted volume"
            }
        ]

    async def get_analytics_recommendations(self) -> Dict[str, Any]:
        """Get AI-generated recommendations based on support analytics"""
        await asyncio.sleep(0.5)  # Simulate async processing

        return {
            "status": "success",
            "recommendations": [
                "Implement proactive communication for common technical issues",
                "Review high-priority ticket resolution times for process improvements",
                "Enhance knowledge base articles for frequently asked questions",
                "Monitor customer satisfaction trends and address negative feedback promptly"
            ]
        }
