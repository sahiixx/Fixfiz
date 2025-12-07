"""
Global Error Handlers
Centralized error handling for consistent API responses
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
from typing import Union

from models import StandardResponse

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base API Error"""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class NotFoundError(APIError):
    """Resource not found"""
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, status_code=404)

class ValidationError(APIError):
    """Validation error"""
    def __init__(self, message: str, errors: list = None):
        super().__init__(message, status_code=422, details={"errors": errors or []})

class AuthenticationError(APIError):
    """Authentication error"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, status_code=401)

class AuthorizationError(APIError):
    """Authorization error"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)

class RateLimitError(APIError):
    """Rate limit exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)

class ServiceUnavailableError(APIError):
    """Service unavailable"""
    def __init__(self, service: str):
        super().__init__(f"Service unavailable: {service}", status_code=503)

async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle custom API errors"""
    logger.warning(
        f"API Error: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
            "details": exc.details
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse(
            success=False,
            message=exc.message,
            data=exc.details if exc.details else None
        ).dict()
    )

async def validation_exception_handler(
    request: Request, 
    exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """Handle Pydantic validation errors"""
    errors = []
    
    if isinstance(exc, RequestValidationError):
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
    
    logger.warning(
        f"Validation Error: {request.url.path}",
        extra={
            "errors": errors,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=StandardResponse(
            success=False,
            message="Validation error",
            data={"errors": errors}
        ).dict()
    )

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    logger.error(
        f"Unexpected error: {str(exc)}",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method
        }
    )
    
    # Don't expose internal errors in production
    from config_enhanced import settings
    
    error_message = "An unexpected error occurred"
    error_details = None
    
    if settings.is_development:
        error_message = str(exc)
        error_details = {
            "type": type(exc).__name__,
            "traceback": str(exc.__traceback__)
        }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=StandardResponse(
            success=False,
            message=error_message,
            data=error_details
        ).dict()
    )

async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle FastAPI HTTP exceptions"""
    status_code = getattr(exc, "status_code", 500)
    detail = getattr(exc, "detail", "An error occurred")
    
    logger.warning(
        f"HTTP Exception: {detail}",
        extra={
            "status_code": status_code,
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=status_code,
        content=StandardResponse(
            success=False,
            message=detail,
            data=None
        ).dict()
    )

def register_error_handlers(app):
    """Register all error handlers with FastAPI app"""
    from fastapi.exceptions import HTTPException
    
    app.add_exception_handler(APIError, api_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
    
    logger.info("✅ Error handlers registered")

# Utility functions for raising errors
def require_authentication():
    """Raise authentication error"""
    raise AuthenticationError()

def require_authorization(message: str = None):
    """Raise authorization error"""
    raise AuthorizationError(message)

def not_found(resource: str, identifier: str = None):
    """Raise not found error"""
    raise NotFoundError(resource, identifier)

def validation_failed(message: str, errors: list = None):
    """Raise validation error"""
    raise ValidationError(message, errors)

def service_unavailable(service: str):
    """Raise service unavailable error"""
    raise ServiceUnavailableError(service)
