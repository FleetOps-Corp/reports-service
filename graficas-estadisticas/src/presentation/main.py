"""Presentation Layer - FastAPI Application
Responsabilidad: Inicializar aplicación y configurar rutas.
Capa: Presentation
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import logging

from ...infrastructure.config import get_settings
from ..routes import router as estadisticas_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(estadisticas_router)


@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup."""
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    logger.info("🛑 Shutting down")


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


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )
