from typing import List, Dict, Any
from sqlalchemy.orm import Session

from . import optimized_models
from .crm_integration import CRMLead # Assuming CRMLead is defined in crm_integration.py

# Placeholder for a simple lead scoring model
def calculate_lead_score(lead_data: Dict[str, Any]) -> float:
    """Calculates a lead score based on predefined criteria."""
    score = 0.0
    # Example criteria (these would be much more complex in a real scenario)
    if "email" in lead_data and "@example.com" not in lead_data["email"]:
        score += 10
    if lead_data.get("status") == "New":
        score += 5
    # Add more complex logic based on lead activity, demographics, etc.
    return score

def qualify_lead(lead_score: float) -> str:
    """Qualifies a lead based on its score."""
    if lead_score >= 15:
        return "Hot Lead"
    elif lead_score >= 10:
        return "Warm Lead"
    else:
        return "Cold Lead"

def process_leads_for_scoring(db: Session) -> List[Dict[str, Any]]:
    """Fetches leads from the database, calculates their scores, and qualifies them."""
    leads = db.query(CRMLead).all()
    processed_leads = []
    for lead in leads:
        lead_data = {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "status": lead.status,
            "created_at": lead.created_at.isoformat() if lead.created_at else None
        }
        score = calculate_lead_score(lead_data)
        qualification = qualify_lead(score)
        processed_leads.append({
            "lead_id": lead.id,
            "score": score,
            "qualification": qualification,
            "original_data": lead_data
        })
    return processed_leads
