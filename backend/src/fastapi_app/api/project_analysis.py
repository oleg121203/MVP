from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List

from ..ai.project_analysis_service import ProjectAnalysisService

router = APIRouter()
project_analysis_service = ProjectAnalysisService()

@router.post('/analyze', response_model=Dict)
async def analyze_project(project_data: Dict = Body(...)):
    """
    Analyze project data to provide insights and recommendations.

    Args:
        project_data: Dict containing project parameters such as area, occupancy, climate_zone,
                     system_type, energy_consumption, ventilation_rate, and noise_level.

    Returns:
        Dict with analysis results including compliance status, issues, and recommendations.
    """
    try:
        result = project_analysis_service.analyze_project(project_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing project: {str(e)}")

@router.post('/train', status_code=200)
async def train_model(training_data: List[Dict] = Body(...)):
    """
    Train the project analysis model with new data.

    Args:
        training_data: List of dictionaries containing project parameters and outcomes.

    Returns:
        Confirmation message upon successful training.
    """
    try:
        project_analysis_service.train_model(training_data)
        return {"message": "Model training completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training model: {str(e)}")
