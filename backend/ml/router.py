from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Dict, Any
import pandas as pd
import tempfile
import os

from .lead_scoring_model import LeadScoringModel

router = APIRouter()

# Singleton model instance
model = LeadScoringModel()

@router.post("/train")
async def train_model(
    file: UploadFile = File(...)
) -> Dict[str, Any]:
    """
    Train model using uploaded CSV data
    CSV should contain features and target column 'conversion_probability'
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        
        # Read CSV
        data = pd.read_csv(tmp_path)
        os.unlink(tmp_path)  # Clean up
        
        # Train model
        result = model.train(data)
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Training failed: {str(e)}"
        )

@router.post("/predict")
async def predict(
    input_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Predict conversion probability for a lead
    Requires all features used during training
    """
    try:
        return model.predict(input_data)
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Prediction failed: {str(e)}"
        )

@router.get("/status")
async def status() -> Dict[str, Any]:
    """Get model training status"""
    return {
        "is_trained": model.is_trained,
        "features": model.features if model.is_trained else None
    }
