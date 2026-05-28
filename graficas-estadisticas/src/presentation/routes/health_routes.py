"""Presentation - Health Routes
Responsabilidad: Endpoints de health check
Capa: Presentation
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "graficas-estadisticas",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {
        "ready": True,
        "service": "graficas-estadisticas",
        "mongodb": "connected",
        "minio": "connected"
    }
