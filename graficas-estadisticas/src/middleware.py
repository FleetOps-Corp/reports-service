"""Middleware for request/response logging and tracing"""
import logging
from time import time

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """Middleware for logging HTTP requests and responses."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request_start = time()
        path = scope["path"]
        method = scope["method"]
        
        logger.info(f"{method} {path}")
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status = message["status"]
                elapsed = time() - request_start
                logger.info(f"{method} {path} - {status} ({elapsed:.3f}s)")
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
