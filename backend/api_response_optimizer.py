from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import json
import gzip
from datetime import datetime
import asyncio

from . import crm_integration
from . import lead_scoring
from . import email_processing
from . import financial_router
from . import project_integration
from . import analytics
from . import ml
from .lead_nurturing import LeadNurturingWorkflow
from .analytics.insights_router import router as insights_router

app = FastAPI()

# Include all routers
app.include_router(crm_integration.router)
app.include_router(lead_scoring.router)
app.include_router(email_processing.router)
app.include_router(financial_router.router)
app.include_router(project_integration.router)
app.include_router(analytics.router, prefix="/analytics")
app.include_router(ml.router, prefix="/ml")
app.include_router(insights_router, prefix="/insights")

# Add lead scoring endpoint
@app.get("/crm/leads/score", response_model=List[Dict[str, Any]])
def get_scored_leads(db: Session = Depends(crm_integration.get_db)):
    return lead_scoring.process_leads_for_scoring(db)

# Add lead nurturing endpoint
@app.post("/crm/leads/nurture", status_code=status.HTTP_200_OK)
def run_lead_nurturing(db: Session = Depends(crm_integration.get_db)):
    workflow = LeadNurturingWorkflow(db)
    workflow.run_all_workflows()
    return {"message": "Lead nurturing workflows initiated."}
    return lead_scoring.process_leads_for_scoring(db)

# Add GZip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

class APIResponseOptimizer:
    def __init__(self):
        self.compression_enabled = True
        self.pagination_default_size = 20
        self.max_page_size = 100
    
    async def compress_response(self, data: Any) -> bytes:
        """Compress response data using gzip"""
        if not self.compression_enabled:
            return json.dumps(data).encode()
        
        json_data = json.dumps(data, ensure_ascii=False)
        return gzip.compress(json_data.encode('utf-8'))
    
    def paginate_data(self, data: List[Any], page: int = 1, size: Optional[int] = None) -> Dict[str, Any]:
        """Paginate large datasets for better performance"""
        if size is None:
            size = self.pagination_default_size
        
        size = min(size, self.max_page_size)  # Enforce max page size
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        
        paginated_data = data[start_idx:end_idx]
        total_items = len(data)
        total_pages = (total_items + size - 1) // size
        
        return {
            "data": paginated_data,
            "pagination": {
                "current_page": page,
                "page_size": size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            },
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "response_time_ms": None  # Will be filled by middleware
            }
        }
    
    async def optimize_response(self, data: Any, paginate: bool = False, **kwargs) -> Dict[str, Any]:
        """Main optimization function for API responses"""
        if paginate and isinstance(data, list):
            return self.paginate_data(data, **kwargs)
        
        return {
            "data": data,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "compressed": self.compression_enabled,
                "response_time_ms": None
            }
        }

# Global optimizer instance
optimizer = APIResponseOptimizer()

@app.middleware("http")
async def response_time_middleware(request: Request, call_next):
    """Middleware to track response times"""
    start_time = asyncio.get_event_loop().time()
    response = await call_next(request)
    process_time = (asyncio.get_event_loop().time() - start_time) * 1000
    
    # Add response time to headers
    response.headers["X-Process-Time"] = str(round(process_time, 2))
    
    return response

# Example optimized endpoints
@app.get("/api/v1/analytics/data")
async def get_analytics_data(
    page: int = 1,
    size: int = 20,
    compress: bool = True
):
    """Example endpoint with pagination and compression"""
    # Mock data - replace with actual database queries
    mock_data = [{"id": i, "value": f"data_{i}", "timestamp": datetime.now().isoformat()} 
                 for i in range(1000)]
    
    optimizer.compression_enabled = compress
    optimized_response = await optimizer.optimize_response(
        mock_data, 
        paginate=True, 
        page=page, 
        size=size
    )
    
    return JSONResponse(content=optimized_response)

@app.get("/api/v1/projects")
async def get_projects(page: int = 1, size: int = 20):
    """Paginated projects endpoint"""
    # Mock project data
    projects = [
        {
            "id": i,
            "name": f"Project {i}",
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        for i in range(1, 501)  # 500 mock projects
    ]
    
    return await optimizer.optimize_response(projects, paginate=True, page=page, size=size)

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint with response optimization"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "redis": "connected",
            "api": "operational"
        }
    }
    
    return await optimizer.optimize_response(health_data)
