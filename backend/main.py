"""
VentAI FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Імпортуємо AI routes
try:
    from api_routes import router as ai_router
    AI_ROUTES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  AI routes not available: {e}")
    AI_ROUTES_AVAILABLE = False

app = FastAPI(
    title="VentAI API", 
    description="AI-powered HVAC analysis platform with Claude 4 integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Додаємо AI routes якщо доступні
if AI_ROUTES_AVAILABLE:
    app.include_router(ai_router)
    print("✅ AI routes включені")
else:
    print("❌ AI routes недоступні")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VentAI API is running", 
        "version": "1.0.0",
        "ai_enabled": AI_ROUTES_AVAILABLE,
        "description": "AI-powered HVAC analysis platform"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "ventai-api",
        "ai_providers": "available" if AI_ROUTES_AVAILABLE else "disabled"
    }

@app.get("/api/events")
async def get_events():
    """Get all events"""
    # Placeholder for events endpoint
    return {
        "events": [
            {
                "id": 1,
                "title": "Sample Event",
                "description": "This is a sample event",
                "date": "2025-06-15T10:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
