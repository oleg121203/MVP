from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
import asyncio

from .insights_service import insights_service

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    """Start insights service when app starts"""
    await insights_service.start()

@router.on_event("shutdown")
async def shutdown_event():
    """Stop insights service when app stops"""
    await insights_service.stop()

@router.get("/insights", response_model=List[Dict[str, Any]])
async def get_insights() -> List[Dict[str, Any]]:
    """Get latest generated insights"""
    # TODO: Implement actual storage/retrieval
    return []

@router.post("/insights/generate", response_model=List[Dict[str, Any]])
async def generate_insights() -> List[Dict[str, Any]]:
    """Manually trigger insights generation"""
    return await insights_service.generate_insights()
