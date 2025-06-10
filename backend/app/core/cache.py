import redis
import json
import logging
from typing import Any, Optional, Dict, List
from functools import wraps
import time

from ...config import settings

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, host: str = settings.REDIS_HOST, port: int = settings.REDIS_PORT, 
                 db: int = settings.REDIS_DB, password: str = settings.REDIS_PASSWORD):
        """
        Initialize Redis cache connection
        """
        try:
            self.redis = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True
            )
            # Test connection
            self.redis.ping()
            self.enabled = True
            logger.info("Redis cache connection established")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.enabled = False
            self.redis = None

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache by key
        Returns None if cache is disabled, key doesn't exist, or on error
        """
        if not self.enabled:
            return None
        
        try:
            value = self.redis.get(key)
            if value is None:
                return None
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # Return raw string if not JSON
                return value
        except redis.RedisError as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set value in cache with optional TTL (time-to-live) in seconds
        Returns True if successful, False if cache disabled or on error
        """
        if not self.enabled:
            return False
        
        try:
            # Serialize complex data structures to JSON
            if isinstance(value, (dict, list, tuple)):
                value = json.dumps(value)
            
            if ttl:
                self.redis.setex(key, ttl, value)
            else:
                self.redis.set(key, value)
            return True
        except redis.RedisError as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete key from cache
        Returns True if successful or key doesn't exist, False on error
        """
        if not self.enabled:
            return False
        
        try:
            self.redis.delete(key)
            return True
        except redis.RedisError as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching a pattern (use with caution)
        Returns number of keys deleted, 0 if cache disabled or on error
        """
        if not self.enabled:
            return 0
        
        try:
            count = 0
            for key in self.redis.scan_iter(match=pattern):
                self.redis.delete(key)
                count += 1
            logger.info(f"Cleared {count} cache keys matching pattern {pattern}")
            return count
        except redis.RedisError as e:
            logger.error(f"Cache clear pattern error for pattern {pattern}: {e}")
            return 0

    def cache_function(self, key_prefix: str, ttl: int = 300):
        """
        Decorator to cache function results based on arguments
        key_prefix: Unique prefix for this function's cache keys
        ttl: Time-to-live in seconds for cached results
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if not self.enabled:
                    return await func(*args, **kwargs)

                # Create unique cache key from function name and arguments
                arg_str = ':'.join(str(a) for a in args)
                kwarg_str = ':'.join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = f"{key_prefix}:{func.__name__}:{arg_str}:{kwarg_str}"

                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_result

                # If not in cache, call function
                result = await func(*args, **kwargs)

                # Store result in cache
                if result is not None:
                    self.set(cache_key, result, ttl)
                    logger.debug(f"Cache miss for {cache_key}, stored with TTL {ttl}")
                
                return result
            return wrapper
        return decorator

    def invalidate_cache(self, key_prefix: str) -> int:
        """
        Invalidate all cache entries starting with key_prefix
        Useful when data updates and cached results need to be refreshed
        """
        return self.clear_pattern(f"{key_prefix}:*")

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics if available
        """
        if not self.enabled or not self.redis:
            return {"enabled": False, "message": "Cache is disabled or not connected"}
        
        try:
            info = self.redis.info()
            return {
                "enabled": True,
                "memory_used": info.get("used_memory_human", "N/A"),
                "memory_peak": info.get("used_memory_peak_human", "N/A"),
                "total_keys": info.get("db0", {}).get("keys", 0) if "db0" in info else "N/A",
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "hit_rate": round(info.get("keyspace_hits", 0) / 
                    (info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0) or 1), 2)
            }
        except redis.RedisError as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"enabled": True, "error": str(e)}

    def warmup_cache(self, key_patterns: List[str], fetch_function, ttl: int = 3600) -> Dict[str, Any]:
        """
        Warm up cache by pre-fetching data for given key patterns
        fetch_function should take a key pattern and return data to cache
        Returns stats on warmup process
        """
        if not self.enabled:
            return {"status": "disabled", "message": "Cache is disabled", "cached_items": 0}
        
        start_time = time.time()
        cached_count = 0
        failed_count = 0
        
        for pattern in key_patterns:
            try:
                # Get keys matching pattern
                keys = [k for k in self.redis.scan_iter(match=pattern)]
                
                for key in keys:
                    # Check if already in cache with sufficient TTL
                    remaining_ttl = self.redis.ttl(key)
                    if remaining_ttl > ttl / 2:
                        cached_count += 1
                        continue
                    
                    # Fetch fresh data
                    data = fetch_function(key)
                    if data is not None:
                        if self.set(key, data, ttl):
                            cached_count += 1
                        else:
                            failed_count += 1
                    else:
                        failed_count += 1
            except Exception as e:
                logger.error(f"Error warming cache for pattern {pattern}: {e}")
                failed_count += 1
        
        duration = time.time() - start_time
        return {
            "status": "completed",
            "message": f"Cache warmup completed in {duration:.2f} seconds",
            "cached_items": cached_count,
            "failed_items": failed_count,
            "total_patterns": len(key_patterns)
        }

# Global cache instance
cache_manager = CacheManager()
