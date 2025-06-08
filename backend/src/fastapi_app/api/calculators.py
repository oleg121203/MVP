from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Pydantic Models for Air Exchange Calculator
class AirExchangeInput(BaseModel):
    room_length: float  # in feet
    room_width: float   # in feet
    room_height: float  # in feet
    air_changes_per_hour: float  # desired ACH

class AirExchangeOutput(BaseModel):
    room_volume: float  # in cubic feet
    required_airflow: float  # in CFM (cubic feet per minute)

# Pydantic Models for Duct Sizing Calculator
class DuctSizingInput(BaseModel):
    airflow_rate: float  # in CFM (cubic feet per minute)
    velocity: float      # in FPM (feet per minute)
    is_round_duct: bool  # True for round duct, False for rectangular
    aspect_ratio: Optional[float] = 1.0  # Width to height ratio for rectangular ducts, default 1:1

class DuctSizingOutput(BaseModel):
    duct_type: str
    diameter: Optional[float] = None  # in inches, for round ducts
    width: Optional[float] = None     # in inches, for rectangular ducts
    height: Optional[float] = None    # in inches, for rectangular ducts
    area: float                       # cross-sectional area in square inches

# Dependency to get current user (placeholder for auth)
def get_current_user():
    return {"user_id": 1}  # Mock user ID for demonstration

@router.post("/calculators/air-exchange", response_model=AirExchangeOutput)
async def calculate_air_exchange(
    input_data: AirExchangeInput,
    current_user: dict = Depends(get_current_user)
):
    """Calculate required airflow for air exchange based on room dimensions and desired ACH."""
    try:
        # Calculate room volume in cubic feet
        room_volume = input_data.room_length * input_data.room_width * input_data.room_height
        
        # Calculate required airflow in CFM
        # Airflow (CFM) = (Room Volume * ACH) / 60 minutes
        required_airflow = (room_volume * input_data.air_changes_per_hour) / 60
        
        return AirExchangeOutput(
            room_volume=room_volume,
            required_airflow=round(required_airflow, 2)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Calculation error: {str(e)}"
        )

@router.post("/calculators/duct-sizing", response_model=DuctSizingOutput)
async def calculate_duct_sizing(
    input_data: DuctSizingInput,
    current_user: dict = Depends(get_current_user)
):
    """Calculate duct dimensions based on airflow rate and velocity."""
    try:
        # Calculate cross-sectional area in square feet
        # Area (sq ft) = Airflow Rate (CFM) / Velocity (FPM)
        area_sq_ft = input_data.airflow_rate / input_data.velocity
        
        # Convert area to square inches (1 sq ft = 144 sq in)
        area_sq_in = area_sq_ft * 144
        
        if input_data.is_round_duct:
            # For round duct, calculate diameter
            # Area = π * (diameter/2)^2, so diameter = sqrt(Area * 4 / π)
            import math
            diameter = math.sqrt(area_sq_in * 4 / math.pi)
            return DuctSizingOutput(
                duct_type="round",
                diameter=round(diameter, 2),
                area=round(area_sq_in, 2)
            )
        else:
            # For rectangular duct, calculate width and height based on aspect ratio
            # Area = width * height, and width / height = aspect_ratio
            # So, height = sqrt(Area / aspect_ratio), width = height * aspect_ratio
            import math
            height = math.sqrt(area_sq_in / input_data.aspect_ratio)
            width = height * input_data.aspect_ratio
            return DuctSizingOutput(
                duct_type="rectangular",
                width=round(width, 2),
                height=round(height, 2),
                area=round(area_sq_in, 2)
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Calculation error: {str(e)}"
        )
