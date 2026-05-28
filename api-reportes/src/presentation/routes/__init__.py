"""Presentation Layer - REST Routes
Responsabilidad: Exponer endpoints REST.
Patrón: REST API, Hexagonal Adapter
Capa: Presentation
"""
from fastapi import APIRouter, HTTPException, Depends
from ...application.use_cases import (
    GetAvailabilityReportUseCase,
    GetMaintenanceMetricsUseCase,
    GetRecurrentIncidentsUseCase,
    GetVehicleTraceabilityUseCase,
)
from ...application.dto import (
    AvailabilityReportDTO,
    MaintenanceMetricsDTO,
    TraceabilityDTO,
)
from ...infrastructure.observability import track_request, set_availability_metric
from ...infrastructure.persistence import (
    VehicleSnapshotRepositoryMongoDB,
    IncidentRepositoryMongoDB,
    MaintenanceRepositoryMongoDB,
    MongoDBConnection,
)
from ...infrastructure.config import get_settings

router = APIRouter(prefix="/reportes", tags=["reportes"])


async def get_repositories():
    """Dependency injection para repositorios."""
    db = MongoDBConnection.get_database()
    return {
        "vehicle_repo": VehicleSnapshotRepositoryMongoDB(db),
        "incident_repo": IncidentRepositoryMongoDB(db),
        "maintenance_repo": MaintenanceRepositoryMongoDB(db),
    }


@router.get("/disponibilidad", response_model=AvailabilityReportDTO)
@track_request("GET", "/reportes/disponibilidad")
async def get_availability_report(
    sede_id: str = "BOGOTA",
    repos=Depends(get_repositories)
):
    """Obtener reporte de disponibilidad de flota.
    
    Transactional Example: Endpoint REST que orquesta flujo completo
    - Entrada: query parameter sede_id
    - Salida: JSON con métricas de disponibilidad
    - Atraviesa: Application → Domain → Infrastructure → MongoDB
    
    Args:
        sede_id: Identificador de la sede (default: BOGOTA)
        repos: Inyección de dependencias de repositorios
        
    Returns:
        AvailabilityReportDTO: Reporte de disponibilidad
    """
    try:
        use_case = GetAvailabilityReportUseCase(
            vehicle_snapshot_repo=repos["vehicle_repo"],
            incident_repo=repos["incident_repo"],
        )
        
        report = await use_case.execute(sede_id)
        
        # Emit metrics
        set_availability_metric(sede_id, report.availability_percentage)
        
        return report
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mantenimiento", response_model=MaintenanceMetricsDTO)
@track_request("GET", "/reportes/mantenimiento")
async def get_maintenance_metrics(
    sede_id: str = "BOGOTA",
    dias: int = 30,
    repos=Depends(get_repositories)
):
    """Obtener métricas de mantenimiento.
    
    Args:
        sede_id: Identificador de la sede
        dias: Período a analizar en días
        repos: Inyección de dependencias
        
    Returns:
        MaintenanceMetricsDTO: Métricas calculadas
    """
    try:
        use_case = GetMaintenanceMetricsUseCase(
            incident_repo=repos["incident_repo"],
            maintenance_repo=repos["maintenance_repo"],
        )
        
        return await use_case.execute(sede_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/incidentes/recurrentes")
@track_request("GET", "/reportes/incidentes/recurrentes")
async def get_recurrent_incidents(
    dias: int = 30,
    repos=Depends(get_repositories)
):
    """Detectar vehículos con mayor recurrencia de incidentes.
    
    Args:
        dias: Período a analizar
        repos: Inyección de dependencias
        
    Returns:
        List[dict]: Ranking de vehículos con incidentes recurrentes
    """
    try:
        use_case = GetRecurrentIncidentsUseCase(
            incident_repo=repos["incident_repo"],
        )
        
        return await use_case.execute(dias)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trazabilidad/{vehicle_id}", response_model=TraceabilityDTO)
@track_request("GET", "/reportes/trazabilidad/{vehicle_id}")
async def get_vehicle_traceability(
    vehicle_id: str,
    repos=Depends(get_repositories)
):
    """Obtener trazabilidad 360° de un vehículo.
    
    TRANSACTIONAL EXAMPLE COMPLETO:
    - Entrada: vehicle_id en URL
    - Capa Presentation: Validar parámetro
    - Capa Application: Coordinar use case
    - Capa Domain: Calcular métricas
    - Capa Infrastructure: Consultar MongoDB
    - Salida: TraceabilityDTO JSON completo
    
    Args:
        vehicle_id: Identificador del vehículo
        repos: Inyección de dependencias
        
    Returns:
        TraceabilityDTO: Historial completo del vehículo
    """
    try:
        use_case = GetVehicleTraceabilityUseCase(
            vehicle_snapshot_repo=repos["vehicle_repo"],
            incident_repo=repos["incident_repo"],
            maintenance_repo=repos["maintenance_repo"],
        )
        
        return await use_case.execute(vehicle_id)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "api-reportes",
        "version": "1.0.0"
    }
