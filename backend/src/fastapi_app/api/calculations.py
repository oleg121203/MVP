from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import datetime

router = APIRouter()

# Pydantic Models for Calculation Data
class CalculationBase(BaseModel):
    calculation_type: str
    result_summary: str
    date_performed: datetime.datetime

class CalculationCreate(CalculationBase):
    pass

class Calculation(CalculationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Mock database for demonstration purposes
# In a real application, this would be replaced with actual database queries
mock_calculations = [
    Calculation(
        id=1,
        user_id=1,
        calculation_type="Air Exchange Rate",
        result_summary="Calculated air exchange rate for a 500 sq ft room: 6 ACH",
        date_performed=datetime.datetime(2025, 6, 1, 10, 0, 0)
    ),
    Calculation(
        id=2,
        user_id=1,
        calculation_type="Duct Sizing",
        result_summary="Duct size for 200 CFM airflow: 8 inch diameter",
        date_performed=datetime.datetime(2025, 6, 2, 14, 30, 0)
    )
]

# Dependency to get current user (placeholder for auth)
def get_current_user():
    return {"user_id": 1}  # Mock user ID for demonstration

@router.get("/calculations/", response_model=List[Calculation])
async def get_calculations(
    limit: Optional[int] = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get a list of recent calculations for the current user."""
    user_id = current_user["user_id"]
    user_calculations = [calc for calc in mock_calculations if calc.user_id == user_id]
    return user_calculations[:limit]

@router.get("/calculations/{calc_id}", response_model=Calculation)
async def get_calculation(
    calc_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get details of a specific calculation by ID."""
    user_id = current_user["user_id"]
    for calc in mock_calculations:
        if calc.id == calc_id and calc.user_id == user_id:
            return calc
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Calculation not found or access denied"
    )

@router.post("/calculations/", response_model=Calculation)
async def create_calculation(
    calculation: CalculationCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new calculation record."""
    user_id = current_user["user_id"]
    new_id = max([calc.id for calc in mock_calculations], default=0) + 1
    new_calc = Calculation(
        id=new_id,
        user_id=user_id,
        calculation_type=calculation.calculation_type,
        result_summary=calculation.result_summary,
        date_performed=calculation.date_performed
    )
    mock_calculations.append(new_calc)
    return new_calc
