from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from . import optimized_models, financial_models
from .database import get_db
from .schemas import FinancialProject

router = APIRouter()

@router.get("/projects/{project_id}/financial", response_model=Dict[str, Any])
def get_project_financial_view(
    project_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get combined project and financial data
    Includes:
    - Project details
    - Financial summary
    - Cost optimization recommendations
    - Budget forecast
    """
    project = db.query(optimized_models.Project).filter(
        optimized_models.Project.id == project_id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not project.financial_project_id:
        return {
            "project": project,
            "financial": None,
            "message": "No financial project linked"
        }
    
    # Get financial data
    financial_project = db.query(financial_models.FinancialProject).filter(
        financial_models.FinancialProject.id == project.financial_project_id
    ).first()
    
    # Get optimization recommendations
    optimizer = CostOptimizer(db)
    optimization = optimizer.optimize_project_costs(project.financial_project_id)
    forecast = optimizer.forecast_budget(project.financial_project_id)
    anomalies = optimizer.detect_cost_anomalies(project.financial_project_id)
    
    return {
        "project": project,
        "financial": financial_project,
        "optimization": optimization,
        "forecast": forecast,
        "anomalies": anomalies
    }
