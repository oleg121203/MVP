from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from . import optimized_models
from .database import get_db
from .financial_models import FinancialProject
from .cost_optimization import CostOptimizer
from .budget_forecasting import BudgetForecaster
from .app.core.cache import cache_manager

router = APIRouter()

@router.get("/projects/{project_id}/financial", response_model=Dict[str, Any])
@cache_manager.cache_function(key_prefix="project_financial", ttl=300)
async def get_project_financial_view(
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
    - Cost efficiency analysis
    """
    project = db.query(optimized_models.Project).filter(
        optimized_models.Project.id == project_id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not project.financial_project_id:
        raise HTTPException(status_code=404, detail="No financial data associated with this project")
    
    financial_project = db.query(FinancialProject).filter(
        FinancialProject.id == project.financial_project_id
    ).first()
    
    # Get optimization recommendations
    optimizer = CostOptimizer(db)
    optimization = optimizer.optimize_project_costs(project.financial_project_id)
    forecast = optimizer.forecast_budget(project.financial_project_id)
    anomalies = optimizer.detect_cost_anomalies(project.financial_project_id)
    efficiency = optimizer.analyze_cost_efficiency(project.financial_project_id)
    
    # Get advanced long-term forecast
    forecaster = BudgetForecaster(db)
    long_term_forecast = forecaster.create_long_term_forecast(project.financial_project_id, months=12)
    forecast_accuracy = forecaster.evaluate_forecast_accuracy(project.financial_project_id)
    
    # Save forecast to DB if successful
    if long_term_forecast.get('status') == 'forecasted':
        forecaster.save_forecast_to_db(project.financial_project_id, long_term_forecast)
    
    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "client_name": project.client_name,
            "status": project.status,
            "total_cost": project.total_cost,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        },
        "financial": {
            "id": financial_project.id,
            "name": financial_project.name,
            "budget": financial_project.budget,
            "actual_cost": financial_project.actual_cost,
            "status": financial_project.status,
            "start_date": financial_project.start_date,
            "end_date": financial_project.end_date,
            "region": financial_project.region,
            "industry": financial_project.industry
        },
        "optimization": optimization,
        "short_term_forecast": forecast,
        "long_term_forecast": long_term_forecast,
        "anomalies": anomalies,
        "efficiency": efficiency,
        "forecast_accuracy": forecast_accuracy
    }

@router.post("/projects/{project_id}/link-financial/{financial_id}", response_model=Dict[str, Any])
async def link_project_to_financial(
    project_id: int,
    financial_id: int,
    db: Session = Depends(get_db)
):
    """
    Link a project to a financial project record if not already linked
    """
    project = db.query(optimized_models.Project).filter(
        optimized_models.Project.id == project_id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.financial_project_id:
        raise HTTPException(status_code=400, detail="Project already linked to a financial record")
    
    financial_project = db.query(FinancialProject).filter(
        FinancialProject.id == financial_id
    ).first()
    
    if not financial_project:
        raise HTTPException(status_code=404, detail="Financial project not found")
    
    # Update the link
    project.financial_project_id = financial_id
    db.commit()
    db.refresh(project)
    
    # Invalidate cache for this project
    cache_manager.invalidate_cache(f"project_financial:get_project_financial_view:{project_id}")
    
    return {
        "status": "linked",
        "project_id": project_id,
        "financial_project_id": financial_id,
        "message": f"Project {project_id} successfully linked to financial project {financial_id}"
    }

@router.get("/projects/financial-summary", response_model=List[Dict[str, Any]])
@cache_manager.cache_function(key_prefix="projects_financial_summary", ttl=600)
async def get_all_projects_financial_summary(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get financial summary for all projects with linked financial data
    """
    projects = db.query(optimized_models.Project).filter(
        optimized_models.Project.financial_project_id != None
    ).offset(skip).limit(limit).all()
    
    summaries = []
    optimizer = CostOptimizer(db)
    forecaster = BudgetForecaster(db)
    
    for p in projects:
        financial = db.query(FinancialProject).filter(
            FinancialProject.id == p.financial_project_id
        ).first()
        
        if financial:
            efficiency = optimizer.analyze_cost_efficiency(financial.id)
            forecast = forecaster.create_long_term_forecast(financial.id, months=3)
            
            summaries.append({
                "project": {
                    "id": p.id,
                    "name": p.name,
                    "status": p.status
                },
                "financial": {
                    "id": financial.id,
                    "budget": financial.budget,
                    "actual_cost": financial.actual_cost,
                    "status": financial.status
                },
                "efficiency": {
                    "score": efficiency.get("efficiency_score", 0.0),
                    "utilization": efficiency.get("budget_utilization", 0.0)
                },
                "forecast_next_3_months": forecast.get("forecast", [])[:3]
            })
    
    return summaries
