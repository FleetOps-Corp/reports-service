"""Presentation Layer - Incident Routes
Responsabilidad: Endpoints REST para análisis de incidentes
Capa: Presentation
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta

router = APIRouter(prefix="/reportes/incidentes", tags=["Incidentes"])


@router.get("/")
async def get_incident_report(
    location: str = "BOGOTA",
    days: int = 30
):
    """Obtener reporte de incidentes y distribución por severidad.
    
    Args:
        location: Ubicación
        days: Días a reportar
        
    Returns:
        Dict con análisis de incidentes
    """
    try:
        return {
            "location": location,
            "period_days": days,
            "total_incidents": 12,
            "distribution": {
                "CRITICA": 2,
                "ALTA": 5,
                "MEDIA": 3,
                "BAJA": 2
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recurrent")
async def get_recurrent_failures(
    location: str = "BOGOTA",
    min_occurrences: int = 2
):
    """Obtener problemas recurrentes."""
    try:
        return {
            "location": location,
            "min_occurrences": min_occurrences,
            "recurrent_issues": {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
