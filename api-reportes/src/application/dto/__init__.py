"""Application Layer - DTOs (Data Transfer Objects)
Responsabilidad: Transferencia de datos entre capas sin exponer modelos de dominio.
Patrón: DTO Pattern
Capa: Application - Casos de uso
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class VehicleSnapshotDTO(BaseModel):
    """DTO para transferencia de datos de snapshot de vehículo.
    
    Patrón: DTO Pattern
    """
    vehicle_id: str
    fleet_location: str
    status: str
    mileage: int = 0
    last_maintenance_date: Optional[datetime] = None
    incident_count_30days: int = 0
    is_assigned: bool = False
    captured_at: datetime


class OperationalKPIDTO(BaseModel):
    """DTO para transferencia de KPI operativo."""
    kpi_id: str
    fleet_location: str
    total_vehicles: int
    available_vehicles: int
    availability_percentage: float
    average_mttr_hours: float
    preventive_maintenance_ratio: float
    incident_count_month: int
    calculated_at: datetime
    alert_level: str


class AvailabilityReportDTO(BaseModel):
    """DTO para reporte de disponibilidad.
    
    Transactional Example: Respuesta de endpoint /reportes/disponibilidad
    """
    fleet_location: str
    total_vehicles: int
    available_vehicles: int
    availability_percentage: float
    is_healthy: bool
    alert_level: str
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "fleet_location": "BOGOTÁ",
                "total_vehicles": 50,
                "available_vehicles": 42,
                "availability_percentage": 84.0,
                "is_healthy": True,
                "alert_level": "HEALTHY",
                "captured_at": "2026-05-27T22:17:00Z"
            }
        }


class IncidentDTO(BaseModel):
    """DTO para transferencia de incidente histórico."""
    incident_id: str
    vehicle_id: str
    severity: str
    description: str
    occurred_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_hours: Optional[float] = None


class MaintenanceDTO(BaseModel):
    """DTO para transferencia de registro de mantenimiento."""
    maintenance_id: str
    vehicle_id: str
    maintenance_type: str
    description: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_hours: Optional[float] = None
    cost: Optional[float] = None


class MaintenanceMetricsDTO(BaseModel):
    """DTO para métricas de mantenimiento."""
    average_mttr_hours: float
    preventive_maintenance_ratio: float
    total_maintenance_events: int
    preventive_count: int
    corrective_count: int
    period_days: int


class RecurrentIncidentDTO(BaseModel):
    """DTO para incidentes recurrentes de un vehículo."""
    vehicle_id: str
    incident_count: int
    severity_distribution: dict
    last_incident_at: Optional[datetime] = None


class TraceabilityDTO(BaseModel):
    """DTO para trazabilidad 360° de un vehículo.
    
    Transactional Example: Respuesta de endpoint
    /reportes/trazabilidad/{vehicle_id}
    """
    vehicle_id: str
    fleet_location: str
    current_status: str
    total_incidents_lifetime: int
    total_incidents_30days: int
    total_maintenance_events: int
    average_mttr_hours: float
    last_snapshot: VehicleSnapshotDTO
    recent_incidents: List[IncidentDTO]
    recent_maintenances: List[MaintenanceDTO]
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "vehicle_id": "VH-001",
                "fleet_location": "BOGOTÁ",
                "current_status": "DISPONIBLE",
                "total_incidents_lifetime": 15,
                "total_incidents_30days": 2,
                "total_maintenance_events": 8,
                "average_mttr_hours": 4.5,
                "last_snapshot": {
                    "vehicle_id": "VH-001",
                    "fleet_location": "BOGOTÁ",
                    "status": "DISPONIBLE",
                    "mileage": 45000,
                    "last_maintenance_date": "2026-04-15T10:30:00Z",
                    "incident_count_30days": 2,
                    "is_assigned": False,
                    "captured_at": "2026-05-27T22:17:00Z"
                },
                "recent_incidents": [],
                "recent_maintenances": [],
                "captured_at": "2026-05-27T22:17:00Z"
            }
        }
