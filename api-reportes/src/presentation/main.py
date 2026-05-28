"""Presentation Layer - FastAPI Application Main Entry Point
Responsabilidad: Inicializar aplicación, registrar rutas, configurar middleware.
Capa: Presentation
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import logging
from typing import Callable

from ...infrastructure.config import get_settings
from ...infrastructure.persistence import MongoDBConnection
from ..routes import router as reportes_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include routers
app.include_router(reportes_router)


@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup."""
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    try:
        await MongoDBConnection.connect(settings)
        logger.info("✅ MongoDB connection established")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    logger.info("🛑 Shutting down")
    
    try:
        await MongoDBConnection.disconnect()
        logger.info("✅ MongoDB connection closed")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")


@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "metrics": "/metrics"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
