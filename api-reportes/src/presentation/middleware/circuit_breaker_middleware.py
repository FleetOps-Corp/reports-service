"""Presentation Layer - Circuit Breaker Middleware
Responsabilidad: Protección contra cascadas de fallos
Patrón: Circuit Breaker
Capa: Presentation
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CircuitBreakerMiddleware(BaseHTTPMiddleware):
    """Middleware que implementa Circuit Breaker pattern."""
    
    def __init__(self, app, failure_threshold: int = 5, timeout_seconds: int = 60):
        super().__init__(app)
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def dispatch(self, request: Request, call_next):
        # Check circuit breaker state
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                return JSONResponse(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    content={
                        "error": "Service Unavailable",
                        "detail": "Circuit breaker is OPEN",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
        
        try:
            response = await call_next(request)
            
            # Reset on success
            if self.state == "HALF_OPEN" and response.status_code < 500:
                self.failure_count = 0
                self.state = "CLOSED"
            
            return response
        
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()
            logger.error(f"Request failed: {str(e)}")
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.warning("Circuit breaker opened due to excessive failures")
            
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if timeout has passed to attempt reset."""
        if not self.last_failure_time:
            return True
        
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout_seconds
