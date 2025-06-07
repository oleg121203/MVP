from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List, Optional

from ..ai.vector_db_service import VectorDBService
from ..ai.price_verification_service import PriceVerificationService

router = APIRouter()
vector_db_service = VectorDBService()
price_verification_service = PriceVerificationService(vector_db_service)

@router.post('/run', response_model=Dict)
async def run_price_verification(data: Dict = Body(...)):
    """
    Manually trigger price verification for all or specific materials.

    Args:
        data: Dictionary containing optional list of material IDs and force update flag.

    Returns:
        Summary of the verification process including counts of checked, updated, and flagged items.
    """
    try:
        material_ids = data.get('material_ids', None)
        force_update = data.get('force_update', False)
        result = await price_verification_service.verify_prices(material_ids, force_update)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running price verification: {str(e)}")

@router.get('/status', response_model=Dict)
async def get_verification_status():
    """
    Get the status of the last price verification run.

    Returns:
        Dictionary with last run timestamp, status, and summary.
    """
    try:
        return price_verification_service.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting verification status: {str(e)}")

@router.get('/review', response_model=List[Dict])
async def get_price_discrepancies():
    """
    Get a list of materials with flagged price discrepancies for manual review.

    Returns:
        List of dictionaries with details of discrepancies.
    """
    try:
        return price_verification_service.get_discrepancies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting price discrepancies: {str(e)}")

@router.post('/review', response_model=Dict)
async def resolve_price_discrepancy(data: Dict = Body(...)):
    """
    Resolve a flagged price discrepancy based on user input.

    Args:
        data: Dictionary containing vector ID, action ('update' or 'ignore'), and optional new price.

    Returns:
        Confirmation of the resolution action.
    """
    try:
        vector_id = data.get('vector_id')
        action = data.get('action')
        new_price_usd = data.get('new_price_usd', None)
        if not vector_id or not action:
            raise HTTPException(status_code=400, detail="vector_id and action are required fields")
        if action not in ['update', 'ignore']:
            raise HTTPException(status_code=400, detail="action must be 'update' or 'ignore'")
        success = price_verification_service.resolve_discrepancy(vector_id, action, new_price_usd)
        if not success:
            raise HTTPException(status_code=404, detail=f"Discrepancy not found for vector_id: {vector_id}")
        return {"message": f"Discrepancy for {vector_id} resolved with action: {action}"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resolving price discrepancy: {str(e)}")
