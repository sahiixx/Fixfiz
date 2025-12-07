"""
Response Caching System
In-memory cache with TTL for frequently accessed data
"""
from typing import Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

class CacheManager:
    """In-memory cache with TTL support"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.cache = {}
        self.cache_ttl = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
        
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from function arguments"""
        key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            # Check if expired
            if datetime.now() < self.cache_ttl.get(key, datetime.min):
                self.hits += 1
                logger.debug(f"Cache HIT: {key}")
                return self.cache[key]
            else:
                # Expired, remove from cache
                self.delete(key)
        
        self.misses += 1
        logger.debug(f"Cache MISS: {key}")
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL"""
        # Check cache size limit
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        ttl = ttl or self.default_ttl
        self.cache[key] = value
        self.cache_ttl[key] = datetime.now() + timedelta(seconds=ttl)
        logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
    
    def delete(self, key: str) -> None:
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
            if key in self.cache_ttl:
                del self.cache_ttl[key]
            logger.debug(f"Cache DELETE: {key}")
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
        self.cache_ttl.clear()
        logger.info("Cache cleared")
    
    def _evict_oldest(self) -> None:
        """Evict oldest cache entry"""
        if self.cache_ttl:
            oldest_key = min(self.cache_ttl, key=self.cache_ttl.get)
            self.delete(oldest_key)
            logger.debug(f"Cache EVICT: {oldest_key}")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
            "total_requests": total_requests
        }
    
    def cleanup_expired(self) -> int:
        """Remove expired entries"""
        now = datetime.now()
        expired_keys = [
            key for key, expiry in self.cache_ttl.items()
            if now >= expiry
        ]
        
        for key in expired_keys:
            self.delete(key)
        
        logger.info(f"Cache cleanup: {len(expired_keys)} expired entries removed")
        return len(expired_keys)

# Global cache instance
cache_manager = CacheManager()

def cached(ttl: Optional[int] = None, key_prefix: str = ""):
    """
    Decorator to cache function results
    
    Usage:
        @cached(ttl=600, key_prefix="user_data")
        async def get_user_data(user_id: str):
            # expensive operation
            return data
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            prefix = key_prefix or func.__name__
            cache_key = cache_manager._generate_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_value = cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache_manager.set(cache_key, result, ttl)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            prefix = key_prefix or func.__name__
            cache_key = cache_manager._generate_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_value = cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_manager.set(cache_key, result, ttl)
            
            return result
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator

def invalidate_cache(key_prefix: str = "") -> None:
    """Invalidate all cache entries with given prefix"""
    if not key_prefix:
        cache_manager.clear()
        return
    
    keys_to_delete = [
        key for key in cache_manager.cache.keys()
        if key.startswith(key_prefix)
    ]
    
    for key in keys_to_delete:
        cache_manager.delete(key)
    
    logger.info(f"Invalidated {len(keys_to_delete)} cache entries with prefix: {key_prefix}")

# Background task to cleanup expired entries
async def cache_cleanup_task():
    """Background task to cleanup expired cache entries"""
    while True:
        try:
            await asyncio.sleep(300)  # Run every 5 minutes
            cache_manager.cleanup_expired()
        except Exception as e:
            logger.error(f"Error in cache cleanup task: {e}")

# Example usage functions
@cached(ttl=600, key_prefix="platform_stats")
async def get_cached_platform_stats():
    """Example: Cache platform statistics for 10 minutes"""
    # This would normally fetch from database
    return {
        "total_users": 1500,
        "active_agents": 5,
        "projects_completed": 500
    }

@cached(ttl=3600, key_prefix="service_catalog")
async def get_cached_service_catalog():
    """Example: Cache service catalog for 1 hour"""
    return {
        "services": [
            {"id": "ai_automation", "name": "AI Automation"},
            {"id": "web_dev", "name": "Web Development"},
            # ... more services
        ]
    }
