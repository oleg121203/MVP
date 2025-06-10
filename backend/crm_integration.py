from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import optimized_models, database_config # Assuming database_config sets up the DB
from .database_config import SessionLocal, engine

# Ensure tables are created (for initial setup, migrations handle this normally)
optimized_models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRM Model (example - define your actual CRM data structure here)
class CRMLead(optimized_models.Base):
    __tablename__ = "crm_leads"

    id = optimized_models.Column(optimized_models.Integer, primary_key=True, index=True)
    name = optimized_models.Column(optimized_models.String, index=True)
    email = optimized_models.Column(optimized_models.String, unique=True, index=True)
    status = optimized_models.Column(optimized_models.String, default="New")
    created_at = optimized_models.Column(optimized_models.DateTime, default=optimized_models.func.now())

# Pydantic models for request/response (example)
from pydantic import BaseModel

class CRMLeadCreate(BaseModel):
    name: str
    email: str
    status: str = "New"

class CRMLeadResponse(CRMLeadCreate):
    id: int
    created_at: optimized_models.datetime

    class Config:
        orm_mode = True


@router.post("/crm/leads/", response_model=CRMLeadResponse, status_code=status.HTTP_201_CREATED)
def create_crm_lead(lead: CRMLeadCreate, db: Session = Depends(get_db)):
    db_lead = CRMLead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.get("/crm/leads/", response_model=List[CRMLeadResponse])
def get_crm_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leads = db.query(CRMLead).offset(skip).limit(limit).all()
    return leads

@router.get("/crm/leads/{lead_id}", response_model=CRMLeadResponse)
def get_crm_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(CRMLead).filter(CRMLead.id == lead_id).first()
    if lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead

# You would typically integrate with an external CRM API here
# For example, using a library like 'requests' to send data to Salesforce, HubSpot, etc.
# This example focuses on the internal API for managing CRM leads in the VentAI system.
