"""Presentation Layer - Availability Routes
Responsabilidad: Endpoints REST para reportes de disponibilidad
Capa: Presentation
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from ...application.use_cases import GetAvailabilityReportUseCase
from ...application.dto import KPIResponseDTO
from ...infrastructure.observability import track_use_case

router = APIRouter(prefix="/reportes/disponibilidad", tags=["Disponibilidad"])


@router.get("/", response_model=KPIResponseDTO)
@track_use_case("get_availability")
async def get_availability_report(
    location: str = "BOGOTA",
    days: int = 30
):
    """Obtener reporte de disponibilidad de flota.
    
    Args:
        location: Ubicación/sede (BOGOTA, MEDELLIN, etc.)
        days: Días a reportar (default 30)
        
    Returns:
        KPIResponseDTO: Métricas de disponibilidad
    """
    try:
        period_start = datetime.utcnow() - timedelta(days=days)
        period_end = datetime.utcnow()
        
        # En producción, usaría inyección de dependencias
        use_case = GetAvailabilityReportUseCase(None, None)
        result = await use_case.execute(location, period_start, period_end)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trend")
async def get_availability_trend(
    location: str = "BOGOTA",
    days: int = 30
):
    """Obtener tendencia de disponibilidad en el tiempo."""
    try:
        return {
            "location": location,
            "period_days": days,
            "trend_data": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
