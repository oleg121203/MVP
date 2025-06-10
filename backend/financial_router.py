from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from . import financial_models
from .database import get_db
from .schemas import FinancialProjectCreate, FinancialProject, FinancialTransactionCreate, FinancialForecastCreate
from .cost_optimization import CostOptimizer

router = APIRouter()

@router.post("/projects/", response_model=FinancialProject)
def create_project(project: FinancialProjectCreate, db: Session = Depends(get_db)):
    db_project = financial_models.FinancialProject(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/projects/", response_model=List[FinancialProject])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(financial_models.FinancialProject).offset(skip).limit(limit).all()

@router.post("/transactions/", response_model=FinancialTransaction)
def create_transaction(transaction: FinancialTransactionCreate, db: Session = Depends(get_db)):
    db_transaction = financial_models.FinancialTransaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.post("/forecasts/", response_model=FinancialForecast)
def create_forecast(forecast: FinancialForecastCreate, db: Session = Depends(get_db)):
    db_forecast = financial_models.FinancialForecast(**forecast.dict())
    db.add(db_forecast)
    db.commit()
    db.refresh(db_forecast)
    return db_forecast

@router.get("/projects/{project_id}/optimize", response_model=Dict[str, Any])
def optimize_project_costs(project_id: int, db: Session = Depends(get_db)):
    """Optimize project costs and return recommendations"""
    optimizer = CostOptimizer(db)
    return optimizer.optimize_project_costs(project_id)

@router.get("/projects/{project_id}/anomalies", response_model=List[Dict[str, Any]])
def detect_cost_anomalies(project_id: int, db: Session = Depends(get_db)):
    """Detect anomalous transactions in project"""
    optimizer = CostOptimizer(db)
    return optimizer.detect_cost_anomalies(project_id)

@router.get("/projects/{project_id}/forecast", response_model=Dict[str, Any])
def forecast_project_budget(
    project_id: int, 
    periods: int = 3, 
    db: Session = Depends(get_db)
):
    """Forecast future budget needs for a project"""
    optimizer = CostOptimizer(db)
    return optimizer.forecast_budget(project_id, periods)
