from typing import Dict, Any
from sqlalchemy.orm import Session

from .crm_integration import CRMLead
from .lead_scoring import calculate_lead_score, qualify_lead

class LeadNurturingWorkflow:
    def __init__(self, db: Session):
        self.db = db

    def send_nurturing_email(self, lead: CRMLead, message: str):
        """Simulates sending a nurturing email to the lead."""
        print(f"[Nurturing Email] Sending to {lead.email}: {message}")
        # In a real application, this would integrate with an email service (e.g., SendGrid, Mailgun)

    def update_lead_status(self, lead: CRMLead, new_status: str):
        """Updates the lead's status in the database."""
        lead.status = new_status
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        print(f"[Lead Status Update] Lead {lead.email} status updated to: {new_status}")

    def run_workflow_for_lead(self, lead: CRMLead):
        """Runs the nurturing workflow for a single lead based on its score and status."""
        lead_data = {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "status": lead.status,
            "created_at": lead.created_at.isoformat() if lead.created_at else None
        }
        score = calculate_lead_score(lead_data)
        qualification = qualify_lead(score)

        print(f"Processing lead {lead.email} - Score: {score}, Qualification: {qualification}")

        if qualification == "Hot Lead" and lead.status == "New":
            self.send_nurturing_email(lead, "Your recent activity indicates high interest! Let's connect.")
            self.update_lead_status(lead, "Engaged - Hot")
        elif qualification == "Warm Lead" and lead.status == "New":
            self.send_nurturing_email(lead, "Here's some more information that might be helpful.")
            self.update_lead_status(lead, "Engaged - Warm")
        elif qualification == "Cold Lead" and lead.status == "New":
            self.send_nurturing_email(lead, "We noticed your interest. Here's a quick overview.")
            self.update_lead_status(lead, "Nurturing - Cold")
        elif lead.status == "Engaged - Hot" and score < 15:
            self.send_nurturing_email(lead, "Checking in! Do you have any questions?")
        # Add more complex workflow rules as needed

    def run_all_workflows(self):
        """Runs nurturing workflows for all leads in the database."""
        leads = self.db.query(CRMLead).all()
        for lead in leads:
            self.run_workflow_for_lead(lead)
        print("Lead nurturing workflows completed for all leads.")
