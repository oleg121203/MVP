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
    import os
    import sqlite3
    import time
    
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "database": {"status": "unknown", "type": "unknown"},
        "mcp_server": True
    }
    
    # Check database connection
    try:
        database_url = os.getenv("DATABASE_URL", "")
        
        if "postgresql" in database_url:
            health_status["database"]["type"] = "postgresql"
            # For PostgreSQL, we'd need to import psycopg2 and test connection
            # For now, just mark as configured
            health_status["database"]["status"] = "configured"
        elif "sqlite" in database_url or not database_url:
            health_status["database"]["type"] = "sqlite"
            # Test SQLite connection
            try:
                # Extract database path from URL or use default
                if "sqlite:///" in database_url:
                    db_path = database_url.replace("sqlite:///", "")
                else:
                    db_path = "./ventai_local.db"
                
                # Test connection
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                conn.close()
                health_status["database"]["status"] = "connected"
            except Exception as e:
                health_status["database"]["status"] = f"error: {str(e)}"
        else:
            health_status["database"]["status"] = "unknown_url"
    except Exception as e:
        health_status["database"]["status"] = f"check_failed: {str(e)}"
    
    return health_status


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
