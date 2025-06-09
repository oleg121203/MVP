"""
API Response Optimization Module - Phase 1.4.4
Implements compression, pagination, and response optimization
"""
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import json
import gzip
from datetime import datetime

class PaginatedResponse(BaseModel):
    """Standardized pagination response"""
    data: List[Any]
    page: int
    page_size: int
    total_count: int
    total_pages: int
    has_next: bool
    has_previous: bool

class APIOptimizer:
    """API response optimization utilities"""
    
    @staticmethod
    def compress_response(data: Dict[str, Any]) -> bytes:
        """Compress JSON response using gzip"""
        json_str = json.dumps(data, ensure_ascii=False)
        return gzip.compress(json_str.encode('utf-8'))
    
    @staticmethod
    def paginate_results(
        data: List[Any], 
        page: int = 1, 
        page_size: int = 50
    ) -> PaginatedResponse:
        """Paginate query results efficiently"""
        total_count = len(data)
        total_pages = (total_count + page_size - 1) // page_size
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_data = data[start_idx:end_idx]
        
        return PaginatedResponse(
            data=paginated_data,
            page=page,
            page_size=page_size,
            total_count=total_count,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )
    
    @staticmethod
    def optimize_json_response(data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize JSON response by removing null values and formatting"""
        def remove_nulls(obj):
            if isinstance(obj, dict):
                return {k: remove_nulls(v) for k, v in obj.items() if v is not None}
            elif isinstance(obj, list):
                return [remove_nulls(item) for item in obj if item is not None]
            return obj
        
        optimized = remove_nulls(data)
        optimized['_meta'] = {
            'timestamp': datetime.utcnow().isoformat(),
            'compressed': True,
            'optimized': True
        }
        return optimized

# FastAPI middleware for automatic compression
def setup_api_optimization(app: FastAPI):
    """Setup API optimization middleware"""
    
    # Add gzip compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    @app.middleware("http")
    async def optimize_response_middleware(request: Request, call_next):
        """Middleware to automatically optimize responses"""
        response = await call_next(request)
        
        # Add optimization headers
        response.headers["X-Content-Optimized"] = "true"
        response.headers["X-Compression"] = "gzip"
        response.headers["Cache-Control"] = "public, max-age=300"
        
        return response

# Export optimization functions
__all__ = ['APIOptimizer', 'PaginatedResponse', 'setup_api_optimization']
