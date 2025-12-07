"""
Metrics Middleware
Automatically tracks all requests for metrics collection
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to track request metrics"""
    
    def __init__(self, app):
        super().__init__(app)
        logger.info("✅ Metrics middleware initialized")
    
    async def dispatch(self, request: Request, call_next):
        """Track request metrics"""
        # Record start time
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Record metrics
        try:
            from metrics_collector import record_request
            record_request(
                endpoint=request.url.path,
                method=request.method,
                duration_ms=duration_ms,
                status_code=response.status_code
            )
        except Exception as e:
            logger.error(f"Error recording metrics: {e}")
        
        # Add duration header
        response.headers["X-Response-Time-Ms"] = str(round(duration_ms, 2))
        
        return response
