from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import ai, project_analysis, vector_db, cost_optimization, price_verification, procurement, crm

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


@app.get("/")
async def root():
    return {"message": "VentAI Backend Service"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
