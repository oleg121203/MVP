from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List, Optional

from ..ai.vector_db_service import VectorDBService
from ..ai.cost_optimization_service import CostOptimizationService

router = APIRouter()
vector_db_service = VectorDBService()
cost_optimization_service = CostOptimizationService(vector_db_service)

@router.post('/analyze', response_model=Dict)
async def analyze_costs(project_data: Dict = Body(...)):
    """
    Analyze project costs based on specifications and materials.

    Args:
        project_data: Dictionary containing project specifications and current materials.

    Returns:
        Dictionary with cost breakdown and potential savings suggestions.
    """
    try:
        result = cost_optimization_service.analyze_costs(project_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing costs: {str(e)}")

@router.post('/scenarios', response_model=List[Dict])
async def compare_scenarios(scenarios_data: Dict = Body(...)):
    """
    Compare multiple cost scenarios for a project.

    Args:
        scenarios_data: Dictionary containing a list of scenarios with materials and settings.

    Returns:
        List of dictionaries with cost analysis for each scenario.
    """
    try:
        scenarios = scenarios_data.get('scenarios', [])
        result = cost_optimization_service.compare_scenarios(scenarios)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing scenarios: {str(e)}")

@router.post('/material-suggestions', response_model=List[Dict])
async def material_suggestions(search_data: Dict = Body(...)):
    """
    Suggest cost-effective materials based on a query.

    Args:
        search_data: Dictionary containing query and optional max cost filter.

    Returns:
        List of dictionaries with suggested materials and their metadata.
    """
    try:
        query = search_data.get('query', '')
        max_cost_usd = search_data.get('max_cost_usd', None)
        top_k = search_data.get('top_k', 5)
        result = cost_optimization_service.get_material_suggestions(query, max_cost_usd, top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting material suggestions: {str(e)}")

@router.post('/train', status_code=200)
async def train_cost_model(training_data: List[Dict] = Body(...)):
    """
    Train the cost optimization model with new data.

    Args:
        training_data: List of dictionaries containing project parameters and actual costs.

    Returns:
        Confirmation message upon successful training.
    """
    try:
        cost_optimization_service.train_model(training_data)
        return {"message": "Cost optimization model training completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training cost model: {str(e)}")
