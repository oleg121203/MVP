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
import time
import pandas as pd

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
    
    def __init__(self):
        self._cache = {}
        self._metrics = []

    def optimize_response(self, data, request_url: str):
        """Optimize API response based on request context"""
        start_time = time.time()
        
        # Check cache first
        cache_key = f"{request_url}:{hash(str(data))}"
        if cache_key in self._cache:
            cached_response = self._cache[cache_key]
            latency = time.time() - start_time
            self._metrics.append({
                "url": request_url,
                "cache_hit": True,
                "latency": latency,
                "timestamp": datetime.now().isoformat(),
                "response_size": len(str(cached_response))
            })
            return cached_response

        # Apply optimizations
        optimized_data = self._apply_optimizations(data)
        
        # Store in cache
        self._cache[cache_key] = optimized_data
        
        # Record metrics
        latency = time.time() - start_time
        self._metrics.append({
            "url": request_url,
            "cache_hit": False,
            "latency": latency,
            "timestamp": datetime.now().isoformat(),
            "response_size": len(str(optimized_data)),
            "optimizations_applied": len(optimized_data) < len(str(data))
        })
        return optimized_data

    def _apply_optimizations(self, data):
        """Apply various optimization techniques"""
        if isinstance(data, dict):
            return {k: self._apply_optimizations(v) for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [self._apply_optimizations(item) for item in data]
        return data

    def get_performance_metrics(self):
        """Get API performance metrics"""
        if not self._metrics:
            return {"message": "No metrics available yet", "count": 0}

        df = pd.DataFrame(self._metrics)
        cache_hit_rate = len(df[df['cache_hit'] == True]) / len(df) if 'cache_hit' in df.columns else 0
        avg_latency = df['latency'].mean() if 'latency' in df.columns else 0
        avg_response_size = df['response_size'].mean() if 'response_size' in df.columns else 0
        optimizations_rate = len(df[df['optimizations_applied'] == True]) / len(df) if 'optimizations_applied' in df.columns else 0

        return {
            "total_requests": len(self._metrics),
            "cache_hit_rate": cache_hit_rate,
            "average_latency": avg_latency,
            "average_response_size": avg_response_size,
            "optimizations_rate": optimizations_rate,
            "detailed_metrics": self._metrics[-10:]  # Last 10 requests
        }

    def clear_cache(self):
        """Clear the response cache"""
        self._cache.clear()

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
