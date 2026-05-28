"""Presentation Layer - REST API Routes
Responsabilidad: Exponer endpoints REST.
Patrón: REST API, Hexagonal Adapter
Capa: Presentation
"""
from fastapi import APIRouter, HTTPException, Depends
from ...application.use_cases import (
    GenerateGeneralReportUseCase,
    GetAvailabilityDataUseCase,
    GetIncidentDataUseCase,
    GetMaintenanceDataUseCase,
    GetMTTRDataUseCase,
)
from ...application.dto import (
    ReportDTO,
    GeneralReportRequestDTO,
    ChartDataDTO,
)
from ...infrastructure.observability import track_report_generation
from ...infrastructure.persistence import (
    MongoDBAnalyticsRepository,
    MinIOReportStorage,
)

router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])


@router.post("/reporte-general", response_model=ReportDTO)
@track_report_generation("default")
async def generate_general_report(
    request: GeneralReportRequestDTO
):
    """Generar reporte general consolidado.
    
    Args:
        request: Solicitud de reporte con parámetros
        
    Returns:
        ReportDTO: Reporte generado con URL de descarga
    """
    try:
        # Mock implementation - en producción usaría inyección de dependencias
        use_case = GenerateGeneralReportUseCase(None, None)
        return await use_case.execute(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datos/disponibilidad", response_model=ChartDataDTO)
async def get_availability_data(location: str = "BOGOTA"):
    """Obtener datos consolidados de disponibilidad.
    
    Args:
        location: Ubicación/sede
        
    Returns:
        ChartDataDTO: Datos para graficar disponibilidad
    """
    try:
        use_case = GetAvailabilityDataUseCase(None)
        return await use_case.execute(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datos/incidentes", response_model=ChartDataDTO)
async def get_incident_data(location: str = "BOGOTA"):
    """Obtener datos consolidados de incidentes.
    
    Args:
        location: Ubicación/sede
        
    Returns:
        ChartDataDTO: Datos para graficar incidentes
    """
    try:
        use_case = GetIncidentDataUseCase(None)
        return await use_case.execute(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datos/mantenimientos", response_model=ChartDataDTO)
async def get_maintenance_data(location: str = "BOGOTA"):
    """Obtener datos consolidados de mantenimiento.
    
    Args:
        location: Ubicación/sede
        
    Returns:
        ChartDataDTO: Datos para graficar mantenimiento
    """
    try:
        use_case = GetMaintenanceDataUseCase(None)
        return await use_case.execute(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datos/mttr", response_model=ChartDataDTO)
async def get_mttr_data(location: str = "BOGOTA"):
    """Obtener datos consolidados de MTTR.
    
    Args:
        location: Ubicación/sede
        
    Returns:
        ChartDataDTO: Datos para graficar MTTR
    """
    try:
        use_case = GetMTTRDataUseCase(None)
        return await use_case.execute(location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/storage/reportes/{report_id}")
async def get_stored_report(report_id: str):
    """Descargar reporte PDF almacenado.
    
    Args:
        report_id: ID del reporte
        
    Returns:
        bytes: Contenido del PDF
    """
    try:
        # Mock implementation
        return {"message": f"Report {report_id} retrieved"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Report not found")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "graficas-estadisticas",
        "version": "1.0.0"
    }
