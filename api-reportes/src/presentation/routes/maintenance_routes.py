"""Presentation Layer - Maintenance Routes
Responsabilidad: Endpoints REST para métricas de mantenimiento
Capa: Presentation
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta

router = APIRouter(prefix="/reportes/mantenimiento", tags=["Mantenimiento"])


@router.get("/")
async def get_maintenance_metrics(
    location: str = "BOGOTA",
    days: int = 30
):
    """Obtener métricas de mantenimiento preventivo vs correctivo.
    
    Args:
        location: Ubicación
        days: Días a reportar
        
    Returns:
        Dict con métricas de mantenimiento
    """
    try:
        return {
            "location": location,
            "period_days": days,
            "preventive_ratio": 0.65,
            "total_maintenances": 24,
            "preventive_count": 16,
            "corrective_count": 8
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/breakdown")
async def get_maintenance_breakdown(location: str = "BOGOTA"):
    """Obtener desglose de mantenimiento por tipo."""
    try:
        return {
            "location": location,
            "preventive": {"count": 16, "percentage": 65},
            "corrective": {"count": 8, "percentage": 35}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
