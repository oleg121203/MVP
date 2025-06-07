from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List, Optional

from ..ai.vector_db_service import VectorDBService
from ..ai.procurement_service import ProcurementService

router = APIRouter()
vector_db_service = VectorDBService()
procurement_service = ProcurementService(vector_db_service)

@router.post('/analyze', response_model=List[Dict])
async def analyze_procurement(project_data: Dict = Body(...)):
    """
    Analyze project material needs and recommend optimal procurement options.

    Args:
        project_data: Dictionary containing project ID, materials needed, project location, and deadline.

    Returns:
        List of dictionaries with recommended suppliers per material.
    """
    try:
        result = await procurement_service.analyze_procurement(project_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing procurement options: {str(e)}")

@router.post('/generate-order', response_model=Dict)
async def generate_purchase_order(order_data: Dict = Body(...)):
    """
    Generate a purchase order based on selected procurement options.

    Args:
        order_data: Dictionary containing project ID, selections of materials and suppliers, and output format.

    Returns:
        Dictionary with URL to generated purchase order or JSON data.
    """
    try:
        project_data = {
            'project_id': order_data.get('project_id', 'PROJ_UNKNOWN')
        }
        selections = order_data.get('selections', [])
        format_type = order_data.get('format', 'pdf')
        if not selections:
            raise HTTPException(status_code=400, detail="No selections provided for purchase order")
        result = procurement_service.generate_purchase_order(project_data, selections, format_type)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating purchase order: {str(e)}")

@router.post('/suppliers/update', response_model=Dict)
async def update_supplier_data(supplier_data: Dict = Body(...)):
    """
    Update or add supplier metadata in the vector database.

    Args:
        supplier_data: Dictionary containing a list of supplier information to update.

    Returns:
        Confirmation of updated supplier data.
    """
    try:
        data_list = supplier_data.get('supplier_data', [])
        if not data_list:
            raise HTTPException(status_code=400, detail="No supplier data provided for update")
        result = procurement_service.update_supplier_data(data_list)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating supplier data: {str(e)}")
