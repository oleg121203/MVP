from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import datetime

router = APIRouter()

# Pydantic Models for AI Insight Data
class InsightBase(BaseModel):
    title: str
    description: str
    severity: str  # e.g., 'low', 'medium', 'high'
    date_generated: datetime.datetime

class InsightCreate(InsightBase):
    pass

class Insight(InsightBase):
    id: int
    user_id: int
    action_taken: bool

    class Config:
        orm_mode = True

# Mock database for demonstration purposes
# In a real application, this would be replaced with actual database queries
mock_insights = [
    Insight(
        id=1,
        user_id=1,
        title="Optimize Duct Layout",
        description="Consider revising duct layout in Project #3 for 15% efficiency gain.",
        severity="medium",
        date_generated=datetime.datetime(2025, 6, 5, 9, 0, 0),
        action_taken=False
    ),
    Insight(
        id=2,
        user_id=1,
        title="Equipment Upgrade Suggestion",
        description="Newer HVAC model available with better energy rating for Project #1.",
        severity="low",
        date_generated=datetime.datetime(2025, 6, 6, 11, 30, 0),
        action_taken=False
    )
]

# Dependency to get current user (placeholder for auth)
def get_current_user():
    return {"user_id": 1}  # Mock user ID for demonstration

@router.get("/ai/insights/", response_model=List[Insight])
async def get_insights(
    limit: Optional[int] = 5,
    current_user: dict = Depends(get_current_user)
):
    """Get a list of AI-generated insights for the current user."""
    user_id = current_user["user_id"]
    user_insights = [insight for insight in mock_insights if insight.user_id == user_id]
    return user_insights[:limit]

@router.post("/ai/insights/{insight_id}/action", response_model=Insight)
async def take_action_on_insight(
    insight_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Mark an insight as action taken."""
    user_id = current_user["user_id"]
    for insight in mock_insights:
        if insight.id == insight_id and insight.user_id == user_id:
            insight.action_taken = True
            return insight
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Insight not found or access denied"
    )
