"""
Customer Support Module for VentAI Enterprise

This module implements AI-driven customer support automation features including
ticket categorization, prioritization, chatbot interactions, and resolution workflows.
"""

import os
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Setup logging
logger = logging.getLogger(__name__)

class CustomerSupport:
    """
    A class to manage AI-driven customer support automation features.
    """
    def __init__(self, config: Dict[str, Any], data_dir: str):
        """
        Initialize the CustomerSupport with configuration and data directory.

        Args:
            config (Dict[str, Any]): Configuration dictionary for customer support.
            data_dir (str): Directory for storing data files.
        """
        self.config = config
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        logger.info("Initialized CustomerSupport with config")

    def categorize_and_prioritize_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Categorizes and prioritizes a customer support ticket using AI-driven analysis.

        Args:
            ticket_data (Dict[str, Any]): Raw ticket data including description and customer information.

        Returns:
            Dict[str, Any]: Processed ticket data with category, priority, and additional metadata.
        """
        logger.info(f"Categorizing and prioritizing ticket: {ticket_data.get('ticket_id', 'N/A')}")
        try:
            # Extract ticket information
            ticket_id = ticket_data.get('ticket_id', f"ticket_{datetime.now().strftime('%Y%m%d%H%M%S%f')}")
            description = ticket_data.get('description', '')
            customer_id = ticket_data.get('customer_id', 'unknown')
            
            # Simulate AI-driven categorization based on description content
            category = self._determine_ticket_category(description)
            priority = self._determine_ticket_priority(description, category, customer_id)
            
            # Enhance ticket data with categorization and prioritization
            processed_ticket = {
                "ticket_id": ticket_id,
                "customer_id": customer_id,
                "description": description,
                "category": category,
                "priority": priority,
                "timestamp": datetime.now().isoformat(),
                "status": "categorized",
                "suggested_action": self._suggest_initial_action(category, priority)
            }
            
            # Save processed ticket data
            ticket_file = os.path.join(self.data_dir, f"ticket_{ticket_id}.json")
            with open(ticket_file, 'w') as f:
                json.dump(processed_ticket, f, indent=2)
            logger.info(f"Saved processed ticket data to {ticket_file}")
            
            return processed_ticket
        except Exception as e:
            logger.error(f"Error categorizing ticket {ticket_data.get('ticket_id', 'N/A')}: {str(e)}")
            raise

    def _determine_ticket_category(self, description: str) -> str:
        """
        Determines the category of a support ticket based on its description.

        Args:
            description (str): The ticket description text.

        Returns:
            str: Determined category for the ticket.
        """
        desc_lower = description.lower()
        if any(kw in desc_lower for kw in ["bug", "error", "crash", "not working", "issue", "problem", "failure"]):
            return "technical_issue"
        elif any(kw in desc_lower for kw in ["billing", "invoice", "payment", "charge", "refund", "cost", "price"]):
            return "billing"
        elif any(kw in desc_lower for kw in ["account", "login", "password", "access", "profile", "signup"]):
            return "account_management"
        elif any(kw in desc_lower for kw in ["feature", "how to", "question", "help", "tutorial", "guide", "training"]):
            return "product_question"
        elif any(kw in desc_lower for kw in ["feedback", "suggestion", "improvement", "idea", "recommendation"]):
            return "feedback"
        else:
            return "general_inquiry"

    def _determine_ticket_priority(self, description: str, category: str, customer_id: str) -> str:
        """
        Determines the priority level of a support ticket.

        Args:
            description (str): The ticket description text.
            category (str): The determined category of the ticket.
            customer_id (str): The ID of the customer who raised the ticket.

        Returns:
            str: Priority level ('low', 'medium', 'high', 'critical').
        """
        desc_lower = description.lower()
        
        # Base priority on category
        if category == "technical_issue":
            base_priority = "high"
        elif category in ["billing", "account_management"]:
            base_priority = "medium"
        else:
            base_priority = "low"
        
        # Escalate priority based on keywords
        if any(kw in desc_lower for kw in ["urgent", "immediate", "asap", "now", "emergency", "critical", "down", "broken"]):
            if base_priority == "high":
                return "critical"
            elif base_priority == "medium":
                return "high"
            else:
                return "medium"
        
        # Additional logic could be added here to check customer value/status
        # and further adjust priority (e.g., VIP customer escalations)
        
        return base_priority

    def _suggest_initial_action(self, category: str, priority: str) -> str:
        """
        Suggests an initial action for the ticket based on category and priority.

        Args:
            category (str): The ticket category.
            priority (str): The ticket priority level.

        Returns:
            str: Suggested initial action for handling the ticket.
        """
        if priority == "critical":
            return "Escalate to senior support team immediately"
        elif category == "technical_issue":
            return "Assign to technical support team"
        elif category == "billing":
            return "Route to billing department"
        elif category == "account_management":
            return "Forward to account management team"
        elif category == "product_question":
            return "Provide relevant documentation or initiate chatbot assistance"
        elif category == "feedback":
            return "Record feedback and notify product team if actionable"
        else:
            return "Review and respond with general assistance"

    def initiate_chatbot_interaction(self, customer_id: str, message: str) -> Dict[str, Any]:
        """
        Initiates an AI-driven chatbot interaction for customer support.

        Args:
            customer_id (str): Unique identifier for the customer.
            message (str): Initial message or query from the customer.

        Returns:
            Dict[str, Any]: Chatbot response data including response text and metadata.
        """
        logger.info(f"Initiating chatbot interaction for customer {customer_id}")
        try:
            interaction_id = f"chat_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            
            # Simulate AI-driven chatbot response based on message content
            response_text, response_type, escalation_needed = self._generate_chatbot_response(message)
            
            # Create interaction record
            interaction_data = {
                "interaction_id": interaction_id,
                "customer_id": customer_id,
                "initial_message": message,
                "response_text": response_text,
                "response_type": response_type,
                "escalation_needed": escalation_needed,
                "timestamp": datetime.now().isoformat(),
                "status": "completed" if not escalation_needed else "escalated"
            }
            
            # Save interaction data
            interaction_file = os.path.join(self.data_dir, f"interaction_{interaction_id}.json")
            with open(interaction_file, 'w') as f:
                json.dump(interaction_data, f, indent=2)
            logger.info(f"Saved chatbot interaction data to {interaction_file}")
            
            # If escalation is needed, create a support ticket
            if escalation_needed:
                ticket_data = {
                    "ticket_id": f"ticket_from_chat_{interaction_id}",
                    "customer_id": customer_id,
                    "description": f"Escalated from chatbot: {message}",
                    "chat_interaction_id": interaction_id
                }
                processed_ticket = self.categorize_and_prioritize_ticket(ticket_data)
                interaction_data["escalated_ticket_id"] = processed_ticket["ticket_id"]
                logger.info(f"Escalated chatbot interaction to ticket {processed_ticket['ticket_id']}")
            
            return interaction_data
        except Exception as e:
            logger.error(f"Error in chatbot interaction for customer {customer_id}: {str(e)}")
            raise

    def _generate_chatbot_response(self, message: str) -> tuple[str, str, bool]:
        """
        Generates a simulated AI chatbot response based on customer message.

        Args:
            message (str): The customer's message to the chatbot.

        Returns:
            tuple[str, str, bool]: Response text, response type, and whether escalation to human support is needed.
        """
        msg_lower = message.lower()
        
        # Determine if the query can be handled by chatbot or needs escalation
        if any(kw in msg_lower for kw in ["urgent", "emergency", "critical", "angry", "frustrated", "escalate", "supervisor", "manager"]):
            return ("I'm sorry to hear about your urgency. I'm escalating your request to a human agent who will assist you shortly.", "escalation", True)
        elif any(kw in msg_lower for kw in ["bug", "error", "crash", "not working", "technical", "issue", "problem"]):
            return ("I understand you're experiencing a technical issue. Let me escalate this to our technical support team for immediate assistance.", "technical_escalation", True)
        elif any(kw in msg_lower for kw in ["billing", "invoice", "payment", "charge", "refund", "cost", "price"]):
            return ("I can see you have a billing concern. I'm transferring you to our billing department for specialized assistance.", "billing_escalation", True)
        elif any(kw in msg_lower for kw in ["hello", "hi", "hey", "greetings"]):
            return ("Hello! How can I assist you today?", "greeting", False)
        elif any(kw in msg_lower for kw in ["how to", "help", "guide", "tutorial", "instructions", "use", "feature"]):
            return ("I'd be happy to help with that. Here's a quick guide on how to use our product feature. [Simulated guide content provided]. If you need more detailed assistance, let me know!", "guidance", False)
        elif any(kw in msg_lower for kw in ["thank you", "thanks", "appreciate"]):
            return ("You're welcome! Is there anything else I can help you with?", "acknowledgement", False)
        else:
            return ("Thank you for your message. I'm here to help. Can you provide more details about your request?", "clarification", False)

    def execute_resolution_workflow(self, ticket_id: str) -> Dict[str, Any]:
        """
        Executes an automated resolution workflow for a given support ticket.

        Args:
            ticket_id (str): Unique identifier for the support ticket.

        Returns:
            Dict[str, Any]: Result of the resolution workflow including status and actions taken.
        """
        logger.info(f"Executing resolution workflow for ticket {ticket_id}")
        try:
            # Load ticket data
            ticket_file = os.path.join(self.data_dir, f"ticket_{ticket_id}.json")
            if not os.path.exists(ticket_file):
                raise ValueError(f"Ticket {ticket_id} not found")
            
            with open(ticket_file, 'r') as f:
                ticket_data = json.load(f)
            
            # Determine applicable workflow based on ticket category and priority
            category = ticket_data.get('category', 'general_inquiry')
            priority = ticket_data.get('priority', 'low')
            workflow_result = self._apply_resolution_workflow(ticket_data, category, priority)
            
            # Update ticket status based on workflow result
            ticket_data['status'] = workflow_result['status']
            ticket_data['resolution_actions'] = workflow_result['actions_taken']
            ticket_data['last_updated'] = datetime.now().isoformat()
            
            # Save updated ticket data
            with open(ticket_file, 'w') as f:
                json.dump(ticket_data, f, indent=2)
            logger.info(f"Updated ticket {ticket_id} with resolution workflow results")
            
            # Prepare response
            resolution_summary = {
                "ticket_id": ticket_id,
                "category": category,
                "priority": priority,
                "resolution_status": workflow_result['status'],
                "actions_taken": workflow_result['actions_taken'],
                "resolution_details": workflow_result['details'],
                "timestamp": datetime.now().isoformat()
            }
            
            # If resolution failed or requires human intervention, log for escalation
            if workflow_result['status'] != "resolved":
                logger.warning(f"Ticket {ticket_id} resolution workflow did not fully resolve issue - status: {workflow_result['status']}")
            
            return resolution_summary
        except Exception as e:
            logger.error(f"Error executing resolution workflow for ticket {ticket_id}: {str(e)}")
            raise

    def _apply_resolution_workflow(self, ticket_data: Dict[str, Any], category: str, priority: str) -> Dict[str, Any]:
        """
        Applies a specific resolution workflow based on ticket category and priority.

        Args:
            ticket_data (Dict[str, Any]): The full ticket data.
            category (str): The ticket category.
            priority (str): The ticket priority.

        Returns:
            Dict[str, Any]: Workflow execution result with status, actions taken, and details.
        """
        description = ticket_data.get('description', '').lower()
        actions_taken = []
        status = "pending_human_review"
        details = "Workflow execution initiated"
        
        if category == "account_management":
            if "login" in description or "password" in description:
                actions_taken.append("Sent password reset instructions to customer")
                status = "resolved"
                details = "Automated password reset workflow applied successfully"
            elif "profile" in description or "update account" in description:
                actions_taken.append("Provided profile update instructions")
                status = "pending_customer_response"
                details = "Customer needs to follow instructions to update profile"
            else:
                actions_taken.append("Unable to automate account management resolution")
                status = "pending_human_review"
                details = "Account management issue requires human support intervention"
        
        elif category == "product_question":
            actions_taken.append("Provided relevant product documentation link")
            actions_taken.append("Initiated FAQ search based on query")
            status = "pending_customer_response"
            details = "Customer provided with documentation; awaiting confirmation of resolution"
        
        elif category == "billing":
            if "invoice" in description or "payment history" in description:
                actions_taken.append("Retrieved and sent billing history to customer")
                status = "pending_customer_response"
                details = "Customer provided with billing information; awaiting confirmation"
            else:
                actions_taken.append("Unable to automate billing resolution")
                status = "pending_human_review"
                details = "Billing issue requires human support intervention"
        
        elif category == "technical_issue":
            if priority in ["low", "medium"]:
                actions_taken.append("Initiated basic troubleshooting protocol")
                actions_taken.append("Sent troubleshooting guide to customer")
                status = "pending_customer_response"
                details = "Customer provided with troubleshooting steps for minor technical issue"
            else:  # high or critical priority
                actions_taken.append("Unable to automate critical technical resolution")
                status = "pending_human_review"
                details = "High-priority technical issue escalated to support team"
        
        elif category == "feedback":
            actions_taken.append("Recorded customer feedback in system")
            actions_taken.append("Sent thank you message for feedback")
            status = "resolved"
            details = "Feedback recorded and acknowledged successfully"
        
        else:  # general_inquiry and others
            actions_taken.append("Provided general information based on query")
            status = "pending_customer_response"
            details = "General inquiry handled with standard information; awaiting customer response"
        
        return {
            "status": status,
            "actions_taken": actions_taken,
            "details": details
        }

    def generate_support_analytics_report(self, report_type: str = "summary", time_period: str = "monthly") -> Dict[str, Any]:
        """
        Generates a support performance analytics report based on ticket and interaction data.

        Args:
            report_type (str): Type of report to generate ("summary", "detailed", "trend", "agent_performance").
            time_period (str): Time period for the report ("daily", "weekly", "monthly", "quarterly").

        Returns:
            Dict[str, Any]: Analytics report with metrics and insights on support performance.
        """
        logger.info(f"Generating support analytics report: {report_type} for {time_period} period")
        try:
            report_id = f"support_report_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            report_data = {
                "report_id": report_id,
                "report_type": report_type,
                "time_period": time_period,
                "timestamp": datetime.now().isoformat(),
                "metrics": {},
                "insights": []
            }
            
            # Aggregate data based on time period and report type
            if report_type == "summary":
                report_data["metrics"] = self._aggregate_summary_metrics(time_period)
                report_data["insights"] = self._generate_summary_insights(report_data["metrics"])
            elif report_type == "detailed":
                report_data["metrics"] = self._aggregate_detailed_metrics(time_period)
                report_data["insights"] = self._generate_detailed_insights(report_data["metrics"])
            elif report_type == "trend":
                report_data["metrics"] = self._aggregate_trend_metrics(time_period)
                report_data["insights"] = self._generate_trend_insights(report_data["metrics"])
            elif report_type == "agent_performance":
                report_data["metrics"] = self._aggregate_agent_performance_metrics(time_period)
                report_data["insights"] = self._generate_agent_performance_insights(report_data["metrics"])
            else:
                raise ValueError(f"Unsupported report type: {report_type}")
            
            # Save report data
            report_file = os.path.join(self.data_dir, f"report_{report_id}.json")
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            logger.info(f"Saved support analytics report to {report_file}")
            
            return report_data
        except Exception as e:
            logger.error(f"Error generating support analytics report ({report_type}, {time_period}): {str(e)}")
            raise

    def _aggregate_summary_metrics(self, time_period: str) -> Dict[str, Any]:
        """
        Aggregates summary metrics for support performance.

        Args:
            time_period (str): Time period for aggregation.

        Returns:
            Dict[str, Any]: Summary metrics for the specified time period.
        """
        # Simulate data aggregation - in real implementation, this would read from stored ticket/interaction data
        tickets_processed = random.randint(50, 500)
        avg_resolution_time = round(random.uniform(1.5, 24.0), 2)  # in hours
        resolution_rate = round(random.uniform(60.0, 95.0), 1)  # percentage
        customer_satisfaction = round(random.uniform(3.5, 4.8), 1)  # out of 5
        chatbot_handled = random.randint(20, 200)
        chatbot_success_rate = round(random.uniform(50.0, 85.0), 1)  # percentage
        escalated_to_human = tickets_processed - chatbot_handled
        
        return {
            "total_tickets_processed": tickets_processed,
            "average_resolution_time_hours": avg_resolution_time,
            "resolution_rate_percent": resolution_rate,
            "customer_satisfaction_score": customer_satisfaction,
            "chatbot_handled_tickets": chatbot_handled,
            "chatbot_success_rate_percent": chatbot_success_rate,
            "escalated_to_human": escalated_to_human,
            "time_period": time_period
        }

    def _generate_summary_insights(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Generates insights based on summary metrics.

        Args:
            metrics (Dict[str, Any]): Summary metrics data.

        Returns:
            List[str]: List of actionable insights based on summary metrics.
        """
        insights = []
        resolution_rate = metrics.get("resolution_rate_percent", 0)
        avg_resolution_time = metrics.get("average_resolution_time_hours", 0)
        customer_satisfaction = metrics.get("customer_satisfaction_score", 0)
        chatbot_success_rate = metrics.get("chatbot_success_rate_percent", 0)
        
        if resolution_rate < 70:
            insights.append("Resolution rate is below target (70%). Consider additional training for support staff or chatbot improvements.")
        if avg_resolution_time > 12:
            insights.append("Average resolution time exceeds 12 hours. Review ticket prioritization and automated workflows for bottlenecks.")
        if customer_satisfaction < 4.0:
            insights.append("Customer satisfaction score is below 4.0. Analyze negative feedback for recurring issues and prioritize resolutions.")
        if chatbot_success_rate < 60:
            insights.append("Chatbot success rate is below 60%. Enhance chatbot training data or escalate complex queries earlier.")
        if not insights:
            insights.append("Support performance metrics are within acceptable ranges. Continue monitoring for any emerging trends.")
        
        return insights

    def _aggregate_detailed_metrics(self, time_period: str) -> Dict[str, Any]:
        """
        Aggregates detailed metrics for support performance by category and priority.

        Args:
            time_period (str): Time period for aggregation.

        Returns:
            Dict[str, Any]: Detailed metrics for the specified time period.
        """
        # Simulate detailed data aggregation
        categories = ["technical_issue", "billing", "account_management", "product_question", "feedback", "general_inquiry"]
        category_metrics = {}
        for cat in categories:
            category_metrics[cat] = {
                "total_tickets": random.randint(5, 100),
                "resolved_tickets": random.randint(3, 80),
                "avg_resolution_time_hours": round(random.uniform(1.0, 30.0), 2),
                "customer_satisfaction": round(random.uniform(3.0, 4.9), 1)
            }
        
        priorities = ["low", "medium", "high", "critical"]
        priority_metrics = {}
        for pri in priorities:
            priority_metrics[pri] = {
                "total_tickets": random.randint(5, 150),
                "resolved_tickets": random.randint(3, 120),
                "avg_resolution_time_hours": round(random.uniform(0.5, 20.0), 2)
            }
        
        return {
            "category_metrics": category_metrics,
            "priority_metrics": priority_metrics,
            "time_period": time_period
        }

    def _generate_detailed_insights(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Generates insights based on detailed metrics by category and priority.

        Args:
            metrics (Dict[str, Any]): Detailed metrics data.

        Returns:
            List[str]: List of actionable insights based on detailed metrics.
        """
        insights = []
        category_metrics = metrics.get("category_metrics", {})
        priority_metrics = metrics.get("priority_metrics", {})
        
        # Category-based insights
        for cat, data in category_metrics.items():
            resolution_rate = (data["resolved_tickets"] / data["total_tickets"]) * 100 if data["total_tickets"] > 0 else 0
            if resolution_rate < 60:
                insights.append(f"Low resolution rate ({resolution_rate:.1f}%) for {cat} tickets. Investigate specific challenges in this category.")
            if data["avg_resolution_time_hours"] > 15:
                insights.append(f"High resolution time ({data['avg_resolution_time_hours']:.1f} hrs) for {cat} tickets. Consider automated solutions or additional resources.")
            if data["customer_satisfaction"] < 3.5:
                insights.append(f"Low satisfaction ({data['customer_satisfaction']:.1f}/5) for {cat} tickets. Review customer feedback for improvement areas.")
        
        # Priority-based insights
        for pri, data in priority_metrics.items():
            resolution_rate = (data["resolved_tickets"] / data["total_tickets"]) * 100 if data["total_tickets"] > 0 else 0
            if pri in ["high", "critical"] and resolution_rate < 80:
                insights.append(f"Urgent: Low resolution rate ({resolution_rate:.1f}%) for {pri} priority tickets. Prioritize resources for faster resolution.")
            if pri in ["high", "critical"] and data["avg_resolution_time_hours"] > 5:
                insights.append(f"Urgent: High resolution time ({data['avg_resolution_time_hours']:.1f} hrs) for {pri} priority tickets. Implement faster escalation protocols.")
        
        if not insights:
            insights.append("Detailed support performance metrics show no critical issues. Continue monitoring category and priority trends.")
        
        return insights

    def _aggregate_trend_metrics(self, time_period: str) -> Dict[str, Any]:
        """
        Aggregates trend metrics for support performance over time.

        Args:
            time_period (str): Base time period for trend analysis.

        Returns:
            Dict[str, Any]: Trend metrics showing performance changes over time.
        """
        # Simulate trend data - in real implementation, this would compare historical data
        trend_data = {}
        periods = 5  # simulate 5 periods of data
        for i in range(periods):
            period_label = f"Period_{i+1}_ago"
            trend_data[period_label] = {
                "total_tickets": random.randint(40, 600),
                "resolution_rate_percent": round(random.uniform(60.0, 95.0), 1),
                "avg_resolution_time_hours": round(random.uniform(1.0, 20.0), 2),
                "customer_satisfaction": round(random.uniform(3.2, 4.8), 1),
                "chatbot_handled_percent": round(random.uniform(30.0, 80.0), 1)
            }
        
        return {
            "trend_data": trend_data,
            "time_period": time_period,
            "periods_compared": periods
        }

    def _generate_trend_insights(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Generates insights based on trend metrics over time.

        Args:
            metrics (Dict[str, Any]): Trend metrics data.

        Returns:
            List[str]: List of actionable insights based on trend metrics.
        """
        insights = []
        trend_data = metrics.get("trend_data", {})
        if not trend_data:
            return ["No trend data available for analysis."]
        
        # Simulate trend analysis by comparing most recent to oldest period
        periods = list(trend_data.keys())
        if len(periods) >= 2:
            oldest_period = periods[-1]
            newest_period = periods[0]
            
            # Resolution rate trend
            old_resolution = trend_data[oldest_period]["resolution_rate_percent"]
            new_resolution = trend_data[newest_period]["resolution_rate_percent"]
            if new_resolution < old_resolution - 5:
                insights.append(f"Downward trend in resolution rate ({old_resolution}% to {new_resolution}%). Investigate potential causes like increased ticket complexity or staffing issues.")
            elif new_resolution > old_resolution + 5:
                insights.append(f"Positive trend in resolution rate ({old_resolution}% to {new_resolution}%). Identify successful practices and reinforce them.")
            
            # Resolution time trend
            old_time = trend_data[oldest_period]["avg_resolution_time_hours"]
            new_time = trend_data[newest_period]["avg_resolution_time_hours"]
            if new_time > old_time + 2:
                insights.append(f"Increasing trend in resolution time ({old_time} hrs to {new_time} hrs). Review workflow efficiency and automation effectiveness.")
            elif new_time < old_time - 2:
                insights.append(f"Positive trend in resolution time reduction ({old_time} hrs to {new_time} hrs). Document and share efficiency gains.")
            
            # Customer satisfaction trend
            old_satisfaction = trend_data[oldest_period]["customer_satisfaction"]
            new_satisfaction = trend_data[newest_period]["customer_satisfaction"]
            if new_satisfaction < old_satisfaction - 0.3:
                insights.append(f"Declining customer satisfaction ({old_satisfaction}/5 to {new_satisfaction}/5). Prioritize customer experience improvements.")
            elif new_satisfaction > old_satisfaction + 0.3:
                insights.append(f"Improving customer satisfaction ({old_satisfaction}/5 to {new_satisfaction}/5). Continue focus on customer-centric support.")
            
            # Chatbot handling trend
            old_chatbot = trend_data[oldest_period]["chatbot_handled_percent"]
            new_chatbot = trend_data[newest_period]["chatbot_handled_percent"]
            if new_chatbot > old_chatbot + 10:
                insights.append(f"Significant increase in chatbot-handled tickets ({old_chatbot}% to {new_chatbot}%). Ensure chatbot quality remains high with increased volume.")
            elif new_chatbot < old_chatbot - 10:
                insights.append(f"Decrease in chatbot-handled tickets ({old_chatbot}% to {new_chatbot}%). Assess if chatbot capabilities need expansion.")
        
        if not insights:
            insights.append("Support performance trends are stable with no significant changes. Maintain current strategies.")
        
        return insights

    def _aggregate_agent_performance_metrics(self, time_period: str) -> Dict[str, Any]:
        """
        Aggregates metrics for individual agent and chatbot performance.

        Args:
            time_period (str): Time period for aggregation.

        Returns:
            Dict[str, Any]: Agent performance metrics for the specified time period.
        """
        # Simulate agent performance data
        agent_metrics = {
            "chatbot": {
                "total_tickets": random.randint(20, 300),
                "resolved_tickets": random.randint(10, 250),
                "avg_resolution_time_hours": round(random.uniform(0.1, 1.0), 2),
                "customer_satisfaction": round(random.uniform(3.5, 4.5), 1),
                "escalation_rate_percent": round(random.uniform(10.0, 40.0), 1)
            },
            "agent_001": {
                "total_tickets": random.randint(10, 100),
                "resolved_tickets": random.randint(5, 90),
                "avg_resolution_time_hours": round(random.uniform(2.0, 10.0), 2),
                "customer_satisfaction": round(random.uniform(3.8, 4.9), 1),
                "escalation_rate_percent": round(random.uniform(5.0, 20.0), 1)
            },
            "agent_002": {
                "total_tickets": random.randint(10, 100),
                "resolved_tickets": random.randint(5, 90),
                "avg_resolution_time_hours": round(random.uniform(2.0, 10.0), 2),
                "customer_satisfaction": round(random.uniform(3.8, 4.9), 1),
                "escalation_rate_percent": round(random.uniform(5.0, 20.0), 1)
            },
            "agent_003": {
                "total_tickets": random.randint(10, 100),
                "resolved_tickets": random.randint(5, 90),
                "avg_resolution_time_hours": round(random.uniform(2.0, 10.0), 2),
                "customer_satisfaction": round(random.uniform(3.8, 4.9), 1),
                "escalation_rate_percent": round(random.uniform(5.0, 20.0), 1)
            }
        }
        
        return {
            "agent_metrics": agent_metrics,
            "time_period": time_period
        }

    def _generate_agent_performance_insights(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Generates insights based on agent performance metrics.

        Args:
            metrics (Dict[str, Any]): Agent performance metrics data.

        Returns:
            List[str]: List of actionable insights based on agent performance.
        """
        insights = []
        agent_metrics = metrics.get("agent_metrics", {})
        if not agent_metrics:
            return ["No agent performance data available for analysis."]
        
        for agent_id, data in agent_metrics.items():
            resolution_rate = (data["resolved_tickets"] / data["total_tickets"]) * 100 if data["total_tickets"] > 0 else 0
            label = "Chatbot" if agent_id == "chatbot" else f"Agent {agent_id}"
            
            if resolution_rate < 60:
                insights.append(f"{label} has low resolution rate ({resolution_rate:.1f}%). Consider additional training or algorithm improvements.")
            if agent_id != "chatbot" and data["avg_resolution_time_hours"] > 6:
                insights.append(f"{label} has high resolution time ({data['avg_resolution_time_hours']:.1f} hrs). Review workload or efficiency strategies.")
            if data["customer_satisfaction"] < 4.0:
                insights.append(f"{label} has low satisfaction score ({data['customer_satisfaction']:.1f}/5). Analyze customer feedback for improvement areas.")
            if data["escalation_rate_percent"] > 25 and agent_id == "chatbot":
                insights.append(f"Chatbot has high escalation rate ({data['escalation_rate_percent']:.1f}%). Enhance chatbot capabilities to handle more queries independently.")
            if agent_id != "chatbot" and data["escalation_rate_percent"] > 15:
                insights.append(f"{label} has high escalation rate ({data['escalation_rate_percent']:.1f}%). Provide additional support or resources to reduce escalations.")
        
        if not insights:
            insights.append("Agent and chatbot performance metrics are within acceptable ranges. Recognize high performers and maintain standards.")
        
        return insights
