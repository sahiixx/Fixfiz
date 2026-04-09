"""
Rate Limiting Middleware
Protects API from abuse and ensures fair usage
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Simple in-memory rate limiter
    Tracks requests per IP address with sliding window
    """
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Store: {ip: [(timestamp, count), ...]}
        self.minute_buckets: Dict[str, list] = {}
        self.hour_buckets: Dict[str, list] = {}
        
        self.blocked_ips: Dict[str, datetime] = {}
        self.block_duration = timedelta(minutes=15)
    
    def _clean_old_entries(self, ip: str, window_minutes: int = 1):
        """Remove entries older than the window"""
        now = datetime.now()
        cutoff = now - timedelta(minutes=window_minutes)
        
        # Clean minute buckets
        if ip in self.minute_buckets:
            self.minute_buckets[ip] = [
                entry for entry in self.minute_buckets[ip]
                if entry[0] > cutoff
            ]
            if not self.minute_buckets[ip]:
                del self.minute_buckets[ip]
        
        # Clean hour buckets (60 minute window)
        if ip in self.hour_buckets:
            hour_cutoff = now - timedelta(hours=1)
            self.hour_buckets[ip] = [
                entry for entry in self.hour_buckets[ip]
                if entry[0] > hour_cutoff
            ]
            if not self.hour_buckets[ip]:
                del self.hour_buckets[ip]
    
    def is_blocked(self, ip: str) -> bool:
        """Check if IP is temporarily blocked"""
        if ip in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip]:
                return True
            else:
                del self.blocked_ips[ip]
        return False
    
    def block_ip(self, ip: str):
        """Temporarily block an IP"""
        self.blocked_ips[ip] = datetime.now() + self.block_duration
        logger.warning(f"IP blocked for {self.block_duration.seconds}s: {ip}")
    
    def is_allowed(self, ip: str) -> Tuple[bool, str, Dict[str, int]]:
        """
        Check if request is allowed for this IP
        
        Returns:
            (allowed, reason, limits_info)
        """
        # Check if blocked
        if self.is_blocked(ip):
            return False, "IP temporarily blocked due to rate limit violations", {}
        
        # Clean old entries
        self._clean_old_entries(ip)
        
        now = datetime.now()
        
        # Count requests in last minute
        minute_count = len(self.minute_buckets.get(ip, []))
        
        # Count requests in last hour
        hour_count = len(self.hour_buckets.get(ip, []))
        
        # Check minute limit
        if minute_count >= self.requests_per_minute:
            self.block_ip(ip)
            return False, f"Rate limit exceeded: {self.requests_per_minute} requests per minute", {
                "limit_per_minute": self.requests_per_minute,
                "requests_this_minute": minute_count,
                "retry_after": 60
            }
        
        # Check hour limit
        if hour_count >= self.requests_per_hour:
            return False, f"Rate limit exceeded: {self.requests_per_hour} requests per hour", {
                "limit_per_hour": self.requests_per_hour,
                "requests_this_hour": hour_count,
                "retry_after": 3600
            }
        
        # Record this request
        if ip not in self.minute_buckets:
            self.minute_buckets[ip] = []
        if ip not in self.hour_buckets:
            self.hour_buckets[ip] = []
        
        self.minute_buckets[ip].append((now, 1))
        self.hour_buckets[ip].append((now, 1))
        
        # Return current usage info
        return True, "OK", {
            "limit_per_minute": self.requests_per_minute,
            "requests_this_minute": minute_count + 1,
            "limit_per_hour": self.requests_per_hour,
            "requests_this_hour": hour_count + 1
        }
    
    def get_stats(self) -> Dict:
        """Get rate limiter statistics"""
        return {
            "tracked_ips": len(self.minute_buckets),
            "blocked_ips": len(self.blocked_ips),
            "limits": {
                "per_minute": self.requests_per_minute,
                "per_hour": self.requests_per_hour
            }
        }

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to apply rate limiting to API requests
    """
    
    def __init__(self, app, enabled: bool = True, 
                 requests_per_minute: int = 60, 
                 requests_per_hour: int = 1000,
                 exempt_paths: list = None):
        super().__init__(app)
        self.enabled = enabled
        self.limiter = RateLimiter(requests_per_minute, requests_per_hour)
        self.exempt_paths = exempt_paths or ["/api/health", "/docs", "/openapi.json"]
        
        logger.info(f"✅ Rate limiter initialized: {requests_per_minute}/min, {requests_per_hour}/hour")
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        # Try to get from X-Forwarded-For header (if behind proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        # Try X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct client
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _is_exempt(self, path: str) -> bool:
        """Check if path is exempt from rate limiting"""
        return any(path.startswith(exempt) for exempt in self.exempt_paths)
    
    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting to request"""
        # Skip if disabled or path is exempt
        if not self.enabled or self._is_exempt(request.url.path):
            return await call_next(request)
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check rate limit
        allowed, reason, limits = self.limiter.is_allowed(client_ip)
        
        if not allowed:
            logger.warning(f"Rate limit exceeded for {client_ip}: {reason}")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "message": reason,
                    "limits": limits
                }
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        
        response.headers["X-RateLimit-Limit-Minute"] = str(self.limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(
            self.limiter.requests_per_minute - limits.get("requests_this_minute", 0)
        )
        response.headers["X-RateLimit-Limit-Hour"] = str(self.limiter.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(
            self.limiter.requests_per_hour - limits.get("requests_this_hour", 0)
        )
        
        return response

# Global rate limiter instance (for direct access)
rate_limiter = RateLimiter()

def get_rate_limiter_stats() -> Dict:
    """Get rate limiter statistics"""
    return rate_limiter.get_stats()
