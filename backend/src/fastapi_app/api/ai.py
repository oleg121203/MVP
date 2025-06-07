from fastapi import APIRouter
from ai.optimization_service import HVACOptimizer
from pydantic import BaseModel

router = APIRouter()
optimizer = HVACOptimizer()


class ChatRequest(BaseModel):
    message: str


class OptimizationRequest(BaseModel):
    area: float
    occupancy: int
    climate_zone: str
    current_system: str


@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """Handle natural language HVAC queries"""
    # TODO: Connect to actual NLP model
    return {"reply": f"AI analysis for: {request.message}", "suggestions": []}


@router.post("/optimize")
async def optimize_system(request: OptimizationRequest):
    """Run HVAC optimization"""
    params = {
        "area": request.area,
        "occupancy": request.occupancy,
        "climate_zone": request.climate_zone,
        "current_system_type": request.current_system,
    }
    return optimizer.optimize(params)
