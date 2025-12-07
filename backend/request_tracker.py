"""
Request ID Tracking Middleware
Adds unique request ID to each request for debugging and tracing
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import logging
import time
from contextvars import ContextVar

logger = logging.getLogger(__name__)

# Context variable to store request ID for the current request
request_id_var: ContextVar[str] = ContextVar("request_id", default="")

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add unique request ID to each request
    Makes debugging and log correlation much easier
    """
    
    def __init__(self, app):
        super().__init__(app)
        logger.info("✅ Request ID tracking initialized")
    
    async def dispatch(self, request: Request, call_next):
        """Add request ID to request and response"""
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Store in context var for use in logging
        request_id_var.set(request_id)
        
        # Add to request state
        request.state.request_id = request_id
        
        # Record start time
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else "unknown"
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            # Log response
            logger.info(
                f"Request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2)
                }
            )
            
            return response
            
        except Exception as e:
            # Log error with request ID
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e)
                },
                exc_info=True
            )
            raise

def get_request_id() -> str:
    """Get current request ID from context"""
    return request_id_var.get("")

class RequestLogger:
    """Enhanced logger that includes request ID"""
    
    def __init__(self, logger_name: str = __name__):
        self.logger = logging.getLogger(logger_name)
    
    def _log_with_request_id(self, level: str, message: str, **kwargs):
        """Log message with request ID"""
        request_id = get_request_id()
        extra = kwargs.get("extra", {})
        extra["request_id"] = request_id
        kwargs["extra"] = extra
        
        log_func = getattr(self.logger, level)
        log_func(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self._log_with_request_id("debug", message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log_with_request_id("info", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log_with_request_id("warning", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log_with_request_id("error", message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log_with_request_id("critical", message, **kwargs)

# Example usage
# from request_tracker import RequestLogger
# logger = RequestLogger(__name__)
# logger.info("Processing user data")  # Automatically includes request ID
