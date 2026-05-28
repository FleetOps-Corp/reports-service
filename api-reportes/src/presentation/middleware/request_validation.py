"""Presentation Layer - Request Validation Middleware
Responsabilidad: Validación de requests
Capa: Presentation
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Middleware para validar requests entrantes."""
    
    async def dispatch(self, request: Request, call_next):
        # Log request details
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'Unknown'}"
        )
        
        response = await call_next(request)
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(time.time())
        
        return response


import time
