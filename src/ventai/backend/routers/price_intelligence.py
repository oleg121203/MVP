from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from ..services.market_analysis import MarketAnalysisService

router = APIRouter(prefix="/api/v1/pricing", tags=["price_intelligence"])

# Initialize service
market_service = MarketAnalysisService()

@router.post("/prices")
async def add_price_data(
    supplier_id: str, 
    product_id: str, 
    price: float
):
    """Add new price data point"""
    try:
        market_service.add_price_data(supplier_id, product_id, price)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/trends/{product_id}")
async def get_price_trends(product_id: str):
    """Get price trends for a product"""
    return market_service.get_price_trends(product_id)

@router.get("/recommendations")
async def get_recommendations(product_ids: str):
    """Get cost-saving recommendations for products"""
    # Convert comma-separated string to list
    product_list = product_ids.split(',')
    recommendations = market_service.get_cost_saving_recommendations(product_list)
    
    # Ensure we always return a response with all requested products
    response = {}
    for pid in product_list:
        if pid in recommendations:
            response[pid] = recommendations[pid]
        else:
            response[pid] = {"recommendation": "No recommendations available", "potential_savings": None}
    
    return response
