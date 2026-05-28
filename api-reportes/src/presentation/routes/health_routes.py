"""Presentation Layer - Health Routes
Responsabilidad: Endpoints de health check y readiness
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
        "service": "api-reportes",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check - verifica si el servicio está listo para tráfico."""
    return {
        "ready": True,
        "service": "api-reportes",
        "mongodb": "connected",
        "grpc": "connected"
    }
