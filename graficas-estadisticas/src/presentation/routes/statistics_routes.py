"""Presentation - Statistics Routes
Responsabilidad: Endpoints REST para estadísticas
Capa: Presentation
"""
from fastapi import APIRouter, HTTPException
from ...application.use_cases import (
    GenerateGeneralReportUseCase,
    GenerateAvailabilityChartsUseCase,
    GenerateIncidentChartsUseCase,
)
from ...application.dto import ReportDTO, ChartDataDTO

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])


@router.post("/reporte-general", response_model=ReportDTO)
async def generate_general_report(location: str = "BOGOTA", period_months: int = 1):
    """Generar reporte general consolidado."""
    try:
        use_case = GenerateGeneralReportUseCase(None, None)
        return await use_case.execute(location, period_months)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/disponibilidad", response_model=ChartDataDTO)
async def get_availability_charts(location: str = "BOGOTA"):
    """Obtener gráficas de disponibilidad."""
    try:
        use_case = GenerateAvailabilityChartsUseCase(None)
        return await use_case.execute(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/incidentes", response_model=ChartDataDTO)
async def get_incident_charts(location: str = "BOGOTA"):
    """Obtener gráficas de incidentes."""
    try:
        use_case = GenerateIncidentChartsUseCase(None)
        return await use_case.execute(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
