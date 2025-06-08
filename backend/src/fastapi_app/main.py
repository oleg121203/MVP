from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import ai, project_analysis, vector_db, cost_optimization, price_verification, procurement, crm, calculations, insights, calculators

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai.router, prefix="/api/ai")
app.include_router(project_analysis.router, prefix="/api/project-analysis")
app.include_router(vector_db.router, prefix="/api/vectors")
app.include_router(cost_optimization.router, prefix="/api/cost-optimization")
app.include_router(price_verification.router, prefix="/api/price-verification")
app.include_router(procurement.router, prefix="/api/procurement")
app.include_router(crm.router, prefix="/api/crm")
app.include_router(calculations.router, prefix="/api", tags=["calculations"])
app.include_router(calculators.router, prefix="/api", tags=["calculators"])
app.include_router(insights.router, prefix="/api", tags=["insights"])


@app.get("/")
async def root():
    return {"message": "VentAI Backend Service"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "mcp_server": True
    }


@app.get("/status")
async def status():
    # Hardcoded AI status for now as direct access to providers status is not available
    ai_status = [
        {
            "name": "ollama",
            "available": True,
            "model": "llama3.1"
        }
    ]
    ai_initialized = any(provider["available"] for provider in ai_status)
    return {
        "status": "ok",
        "ai_providers": ai_status,
        "project_status": {
            "success": ai_initialized,
            "status_info": {
                "message": "Project analysis backend status.",
                "services": {
                    "database": False,
                    "redis": False,
                    "ai_engine": ai_initialized
                }
            }
        }
    }


@app.get("/capabilities")
async def capabilities():
    return {
        "tools": {
            "hvac_optimize": True,
            "ai_hvac_analyze": True,
            "ai_providers_status": True,
            "get_project_status": True,
            "cost_optimization": True,
            "price_verification": True,
            "procurement": True,
            "crm": True,
            "project_analysis": True,
            "vector_db": True
        },
        "total_tools": 10,
        "available_tools": 10
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
