from typing import Dict, List, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .crm_integration import CRMLead, get_db

class EmailTemplate(BaseModel):
    id: str
    category: str
    subject: str
    body: str
    variables: List[str]

class TemplateManager:
    def __init__(self, db: Session = next(get_db())):
        self.templates: Dict[str, EmailTemplate] = {}
        self.db = db
        self.load_default_templates()
    
    def load_default_templates(self):
        """Initialize with default response templates"""
        self.templates = {
            "sales": EmailTemplate(
                id="sales_response",
                category="sales",
                subject="Thank you for your interest in VentAI",
                body="""Dear {customer_name},\n\nThank you for reaching out about our {product}. \n\nWe've created a lead for you (ID: {lead_id}). Our team will contact you shortly.\n\nBest regards,\nVentAI Team""",
                variables=["customer_name", "product", "lead_id"]
            ),
            "support": EmailTemplate(
                id="support_response",
                category="support",
                subject="VentAI Support Ticket #{ticket_id}",
                body="""Hello {customer_name},\n\nWe've received your support request (#{ticket_id}) and will respond within 24 hours.\n\nIssue: {issue_description}\n\nThank you for your patience.\n\nVentAI Support Team""",
                variables=["customer_name", "ticket_id", "issue_description"]
            ),
        }
    
    def create_crm_lead(self, email_data: Dict[str, Any]) -> str:
        """Create a CRM lead from email data"""
        lead = CRMLead(
            name=email_data.get("from", "").split("@")[0],
            email=email_data.get("from", ""),
            status="New",
            source="Email",
            notes=f"Original subject: {email_data.get('subject', '')}"
        )
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return str(lead.id)
    
    def generate_response(self, template_id: str, email_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate a response email using a template and CRM integration"""
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Create CRM lead if this is a sales inquiry
        lead_id = ""
        if template.category == "sales":
            lead_id = self.create_crm_lead(email_data)
        
        # Prepare variables
        variables = {
            "customer_name": email_data.get("from", "").split("@")[0],
            "product": "VentAI Enterprise",
            "lead_id": lead_id,
            "ticket_id": str(hash(email_data.get("from", "") + email_data.get("date", "")))[:8],
            "issue_description": email_data.get("subject", "")
        }
        
        return {
            "subject": template.subject.format(**variables),
            "body": template.body.format(**variables),
            "lead_id": lead_id if lead_id else None
        }
    
    def get_template(self, category: str) -> EmailTemplate:
        """Get template for a specific category"""
        return self.templates.get(category)
    
    def add_template(self, template: EmailTemplate):
        """Add or update a response template"""
        self.templates[template.id] = template
