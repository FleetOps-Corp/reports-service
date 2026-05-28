"""Domain Model: VehicleSnapshot - Entidad de Dominio
Representa un snapshot operacional histórico de un vehículo.
Responsabilidad: Persistir estado histórico de vehículos para análisis.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class VehicleSnapshot(BaseModel):
    """Snapshot operacional de un vehículo en un punto en el tiempo.
    
    Patrón: Domain Model (DDD)
    Capa: Domain - Lógica de negocio pura
    """
    
    vehicle_id: str = Field(..., description="Identificador único del vehículo")
    fleet_location: str = Field(..., description="Ubicación de la flota (sede)")
    status: str = Field(..., description="Estado operativo: DISPONIBLE, EN_USO, EN_MANTENIMIENTO")
    mileage: int = Field(default=0, description="Kilometraje actual")
    last_maintenance_date: Optional[datetime] = Field(None, description="Fecha último mantenimiento")
    incident_count_30days: int = Field(default=0, description="Incidentes en últimos 30 días")
    is_assigned: bool = Field(default=False, description="¿Vehículo asignado actualmente?")
    captured_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp del snapshot")
    
    class Config:
        json_schema_extra = {
            "example": {
                "vehicle_id": "VH-001",
                "fleet_location": "BOGOTÁ",
                "status": "DISPONIBLE",
                "mileage": 45000,
                "last_maintenance_date": "2026-04-15T10:30:00Z",
                "incident_count_30days": 2,
                "is_assigned": False,
                "captured_at": "2026-05-27T22:17:00Z"
            }
        }
    
    def is_available(self) -> bool:
        """Determina si el vehículo está disponible.
        
        Lógica de dominio: Un vehículo está disponible si su estado es DISPONIBLE
        y no está asignado actualmente.
        
        Returns:
            bool: True si el vehículo está disponible
        """
        return self.status == "DISPONIBLE" and not self.is_assigned
    
    def requires_maintenance(self) -> bool:
        """Determina si el vehículo requiere mantenimiento basado en criterios.
        
        Heurística: Si hace más de 30 días desde último mantenimiento
        
        Returns:
            bool: True si requiere mantenimiento
        """
        if self.last_maintenance_date is None:
            return True
        days_since_maintenance = (datetime.utcnow() - self.last_maintenance_date).days
        return days_since_maintenance > 30
