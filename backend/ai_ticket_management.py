from typing import List, Dict, Any, Optional
import asyncio
import random
from datetime import datetime

class AITicketManagement:
    def __init__(self):
        self.support_db = None  # To be connected to customer support database

    async def connect_to_db(self, db_connection):
        """Connect to the customer support database"""
        self.support_db = db_connection
        return self

    async def prioritize_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Prioritize a ticket using AI analysis"""
        if not self.support_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "priority": ""
            }

        ticket_response = self.support_db.get_ticket(ticket_id)
        if ticket_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Ticket not found",
                "priority": ""
            }

        ticket = ticket_response.get("ticket", {})
        priority = await self._analyze_priority_with_ai(ticket)
        
        # Update ticket priority in database
        update_response = self.support_db.update_ticket(ticket_id, priority=priority)
        if update_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Failed to update ticket priority",
                "priority": priority
            }

        return {
            "status": "success",
            "message": "Ticket priority updated",
            "ticket_id": ticket_id,
            "priority": priority
        }

    async def _analyze_priority_with_ai(self, ticket: Dict[str, Any]) -> str:
        """Simulate AI-driven priority analysis"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        subject = ticket.get("subject", "").lower()
        description = ticket.get("description", "").lower()
        
        high_priority_keywords = ["urgent", "critical", "emergency", "down", "crash", "failure"]
        medium_priority_keywords = ["problem", "issue", "error", "bug", "help"]

        score = 0
        text = subject + " " + description
        for keyword in high_priority_keywords:
            if keyword in text:
                score += 2
        for keyword in medium_priority_keywords:
            if keyword in text:
                score += 1

        if score >= 3:
            return "High"
        elif score >= 1:
            return "Medium"
        return "Low"

    async def categorize_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Categorize a ticket using AI analysis"""
        if not self.support_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "category": ""
            }

        ticket_response = self.support_db.get_ticket(ticket_id)
        if ticket_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Ticket not found",
                "category": ""
            }

        ticket = ticket_response.get("ticket", {})
        category = await self._analyze_category_with_ai(ticket)
        
        # Update ticket category in database
        update_response = self.support_db.update_ticket(ticket_id, category=category)
        if update_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Failed to update ticket category",
                "category": category
            }

        return {
            "status": "success",
            "message": "Ticket category updated",
            "ticket_id": ticket_id,
            "category": category
        }

    async def _analyze_category_with_ai(self, ticket: Dict[str, Any]) -> str:
        """Simulate AI-driven category analysis"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        subject = ticket.get("subject", "").lower()
        description = ticket.get("description", "").lower()
        
        categories = {
            "Technical": ["error", "bug", "crash", "system", "login", "access", "password", "network", "server", "website", "app", "software", "hardware"],
            "Billing": ["payment", "invoice", "bill", "charge", "refund", "subscription", "account", "pricing", "cost", "fee"],
            "Product": ["product", "feature", "use", "how to", "tutorial", "guide", "function", "item", "purchase", "order", "delivery"],
            "Feedback": ["feedback", "suggestion", "complaint", "review", "experience", "improve", "idea", "satisfied", "happy", "disappoint"]
        }

        text = subject + " " + description
        max_matches = 0
        selected_category = "General Inquiry"

        for category, keywords in categories.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            if matches > max_matches:
                max_matches = matches
                selected_category = category

        return selected_category

    async def assign_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Assign a ticket to an appropriate support agent using AI"""
        if not self.support_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "assigned_to": ""
            }

        ticket_response = self.support_db.get_ticket(ticket_id)
        if ticket_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Ticket not found",
                "assigned_to": ""
            }

        ticket = ticket_response.get("ticket", {})
        assigned_to = await self._assign_with_ai(ticket)
        
        # Update ticket assignment in database
        update_response = self.support_db.update_ticket(ticket_id, assigned_to=assigned_to)
        if update_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Failed to update ticket assignment",
                "assigned_to": assigned_to
            }

        return {
            "status": "success",
            "message": "Ticket assigned",
            "ticket_id": ticket_id,
            "assigned_to": assigned_to
        }

    async def _assign_with_ai(self, ticket: Dict[str, Any]) -> str:
        """Simulate AI-driven ticket assignment"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        category = ticket.get("category", "General Inquiry")
        priority = ticket.get("priority", "Medium")

        # Simulated team assignments based on category and priority
        technical_team = ["Tech Agent 1", "Tech Agent 2", "Tech Agent 3"]
        billing_team = ["Billing Agent 1", "Billing Agent 2"]
        product_team = ["Product Agent 1", "Product Agent 2"]
        feedback_team = ["Feedback Agent 1"]
        general_team = ["General Agent 1", "General Agent 2"]

        if category == "Technical":
            team = technical_team
        elif category == "Billing":
            team = billing_team
        elif category == "Product":
            team = product_team
        elif category == "Feedback":
            team = feedback_team
        else:
            team = general_team

        # Adjust assignment based on priority
        if priority == "High" and len(team) > 1:
            # Assign to more senior agents for high priority (simulated as first in list)
            return team[0]
        else:
            # Random assignment for normal priority
            return random.choice(team)

    async def analyze_ticket_sentiment(self, ticket_id: str) -> Dict[str, Any]:
        """Analyze the sentiment of a ticket's content"""
        if not self.support_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "sentiment": ""
            }

        ticket_response = self.support_db.get_ticket(ticket_id)
        if ticket_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Ticket not found",
                "sentiment": ""
            }

        ticket = ticket_response.get("ticket", {})
        sentiment = await self._analyze_sentiment_with_ai(ticket)
        return {
            "status": "success",
            "message": "Sentiment analysis completed",
            "ticket_id": ticket_id,
            "sentiment": sentiment
        }

    async def _analyze_sentiment_with_ai(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate AI-driven sentiment analysis"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        description = ticket.get("description", "").lower()
        subject = ticket.get("subject", "").lower()
        
        positive_keywords = ["great", "good", "happy", "satisfied", "thank", "awesome", "excellent", "pleased"]
        negative_keywords = ["bad", "terrible", "awful", "disappoint", "frustrat", "angry", "upset", "worst", "poor"]
        
        text = subject + " " + description
        positive_score = sum(1 for keyword in positive_keywords if keyword in text)
        negative_score = sum(1 for keyword in negative_keywords if keyword in text)

        if positive_score > negative_score:
            sentiment = "Positive"
            confidence = round((positive_score / (positive_score + negative_score + 1)) * random.uniform(0.7, 0.9), 2)
        elif negative_score > positive_score:
            sentiment = "Negative"
            confidence = round((negative_score / (positive_score + negative_score + 1)) * random.uniform(0.7, 0.9), 2)
        else:
            sentiment = "Neutral"
            confidence = round(random.uniform(0.5, 0.7), 2)

        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "notes": f"AI analysis based on content tone and keywords"
        }

    async def predict_ticket_resolution_time(self, ticket_id: str) -> Dict[str, Any]:
        """Predict the resolution time for a ticket"""
        if not self.support_db:
            return {
                "status": "error",
                "message": "Database connection not established",
                "predicted_resolution": ""
            }

        ticket_response = self.support_db.get_ticket(ticket_id)
        if ticket_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Ticket not found",
                "predicted_resolution": ""
            }

        ticket = ticket_response.get("ticket", {})
        prediction = await self._predict_resolution_with_ai(ticket)
        return {
            "status": "success",
            "message": "Resolution time prediction completed",
            "ticket_id": ticket_id,
            "predicted_resolution": prediction
        }

    async def _predict_resolution_with_ai(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate AI-driven resolution time prediction"""
        await asyncio.sleep(0.5)  # Simulate async AI processing

        priority = ticket.get("priority", "Medium")
        category = ticket.get("category", "General Inquiry")
        
        base_hours = random.uniform(2, 24)
        if priority == "High":
            multiplier = 0.5
        elif priority == "Medium":
            multiplier = 1.0
        else:
            multiplier = 1.5

        if category == "Technical":
            multiplier *= 1.2
        elif category == "Billing":
            multiplier *= 0.8

        predicted_hours = round(base_hours * multiplier, 1)
        confidence = round(random.uniform(0.6, 0.85), 2)

        return {
            "hours": predicted_hours,
            "confidence": confidence,
            "notes": f"AI prediction based on priority ({priority}) and category ({category})"
        }

    async def get_management_recommendations(self, ticket_id: str) -> Dict[str, Any]:
        """Get AI-generated recommendations for ticket management"""
        await asyncio.sleep(0.5)  # Simulate async processing

        ticket_response = self.support_db.get_ticket(ticket_id)
        if ticket_response.get("status") != "success":
            return {
                "status": "error",
                "message": "Ticket not found",
                "recommendations": []
            }

        ticket = ticket_response.get("ticket", {})
        priority = ticket.get("priority", "Medium")
        status = ticket.get("status", "Open")
        recommendations = []

        if priority == "High":
            recommendations.append("Escalate to senior support team for immediate attention")
        elif priority == "Medium":
            recommendations.append("Assign to available agent with relevant expertise")
        else:
            recommendations.append("Schedule for review in next available slot")

        if status == "Open":
            recommendations.append("Send initial acknowledgment to customer")
        elif status == "In Progress":
            recommendations.append("Provide status update to customer if not updated recently")

        recommendations.append("Review ticket details for additional context before responding")

        return {
            "status": "success",
            "ticket_id": ticket_id,
            "recommendations": recommendations
        }
