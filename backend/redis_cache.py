"""
Phase 1.4.2 - Redis Caching Layer Implementation
High-performance caching system for analytics data
"""
import redis
import json
import hashlib
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
import asyncio
import aioredis

class RedisCache:
    """Optimized Redis caching system"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client = None
        self.async_redis = None
        
    async def connect(self):
        """Connect to Redis with connection pooling"""
        try:
            self.async_redis = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=20,
                retry_on_timeout=True
            )
            print("✅ Redis connected with connection pooling")
        except Exception as e:
            print(f"⚠️ Redis connection failed: {e}")
            self.async_redis = None
    
    def _generate_cache_key(self, prefix: str, **params) -> str:
        """Generate optimized cache key"""
        param_string = json.dumps(params, sort_keys=True)
        hash_suffix = hashlib.md5(param_string.encode()).hexdigest()[:8]
        return f"ventai:{prefix}:{hash_suffix}"
    
    async def get_analytics_data(self, project_id: int, metric_type: str) -> Optional[Dict]:
        """Get cached analytics data"""
        if not self.async_redis:
            return None
            
        cache_key = self._generate_cache_key(
            "analytics", 
            project_id=project_id, 
            metric_type=metric_type
        )
        
        try:
            cached_data = await self.async_redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Cache read error: {e}")
        
        return None
    
    async def set_analytics_data(
        self, 
        project_id: int, 
        metric_type: str, 
        data: Dict, 
        ttl: int = 300
    ) -> bool:
        """Cache analytics data with TTL"""
        if not self.async_redis:
            return False
            
        cache_key = self._generate_cache_key(
            "analytics", 
            project_id=project_id, 
            metric_type=metric_type
        )
        
        try:
            cached_data = {
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "ttl": ttl
            }
            
            await self.async_redis.setex(
                cache_key, 
                ttl, 
                json.dumps(cached_data)
            )
            return True
        except Exception as e:
            print(f"Cache write error: {e}")
            return False
    
    async def invalidate_project_cache(self, project_id: int):
        """Invalidate all cache entries for a project"""
        if not self.async_redis:
            return
            
        pattern = f"ventai:analytics:*project_id*{project_id}*"
        try:
            keys = await self.async_redis.keys(pattern)
            if keys:
                await self.async_redis.delete(*keys)
                print(f"✅ Invalidated {len(keys)} cache entries for project {project_id}")
        except Exception as e:
            print(f"Cache invalidation error: {e}")
    
    async def get_cached_query(self, query_hash: str) -> Optional[Any]:
        """Get cached database query result"""
        if not self.async_redis:
            return None
            
        cache_key = f"ventai:query:{query_hash}"
        try:
            cached_result = await self.async_redis.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
        except Exception as e:
            print(f"Query cache read error: {e}")
        
        return None
    
    async def cache_query_result(
        self, 
        query_hash: str, 
        result: Any, 
        ttl: int = 600
    ) -> bool:
        """Cache expensive query results"""
        if not self.async_redis:
            return False
            
        cache_key = f"ventai:query:{query_hash}"
        try:
            await self.async_redis.setex(
                cache_key, 
                ttl, 
                json.dumps(result, default=str)
            )
            return True
        except Exception as e:
            print(f"Query cache write error: {e}")
            return False

# Global cache instance
cache = RedisCache()

async def initialize_cache():
    """Initialize Redis cache on startup"""
    await cache.connect()

# Cache decorators for common patterns
def cache_analytics(ttl: int = 300):
    """Decorator for caching analytics functions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache first
            cached_result = await cache.get_cached_query(cache_key)
            if cached_result:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache.cache_query_result(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator

if __name__ == "__main__":
    async def test_cache():
        await initialize_cache()
        
        # Test cache operations
        test_data = {"metric": "cost_analysis", "value": 15000.50}
        await cache.set_analytics_data(1, "cost", test_data)
        
        retrieved = await cache.get_analytics_data(1, "cost")
        print(f"Cache test result: {retrieved}")
    
    asyncio.run(test_cache())
