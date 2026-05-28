"""Domain Model: Maintenance
Representa un evento de mantenimiento histórico de un vehículo.
Responsabilidad: Encapsular datos de mantenimiento para cálculo de métricas.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Maintenance(BaseModel):
    """Registro histórico de una actividad de mantenimiento.
    
    Patrón: Domain Model (DDD)
    Capa: Domain - Lógica de negocio pura
    """
    
    maintenance_id: str = Field(..., description="Identificador único del mantenimiento")
    vehicle_id: str = Field(..., description="Vehículo mantenido")
    maintenance_type: str = Field(..., description="Tipo: PREVENTIVO, CORRECTIVO, RUTINARIO")
    description: str = Field(..., description="Descripción del mantenimiento")
    started_at: datetime = Field(..., description="Inicio del mantenimiento")
    completed_at: Optional[datetime] = Field(None, description="Fin del mantenimiento")
    cost: Optional[float] = Field(None, ge=0, description="Costo en moneda local")
    
    class Config:
        json_schema_extra = {
            "example": {
                "maintenance_id": "MAINT-2026-001",
                "vehicle_id": "VH-001",
                "maintenance_type": "PREVENTIVO",
                "description": "Cambio de aceite y filtro",
                "started_at": "2026-05-20T08:00:00Z",
                "completed_at": "2026-05-20T10:30:00Z",
                "cost": 150000.0
            }
        }
    
    def is_completed(self) -> bool:
        """Determine if maintenance has been completed.
        
        Returns:
            bool: True if completed_at is set
        """
        return self.completed_at is not None
    
    def duration_hours(self) -> Optional[float]:
        """Calculate maintenance duration in hours.
        
        Returns:
            float: Hours of maintenance, None if incomplete
        """
        if not self.is_completed():
            return None
        delta = self.completed_at - self.started_at
        return delta.total_seconds() / 3600.0
    
    def is_preventive(self) -> bool:
        """Determine if this is preventive maintenance.
        
        Returns:
            bool: True if type is PREVENTIVO
        """
        return self.maintenance_type == "PREVENTIVO"
    
    def is_corrective(self) -> bool:
        """Determine if this is corrective maintenance.
        
        Returns:
            bool: True if type is CORRECTIVO
        """
        return self.maintenance_type == "CORRECTIVO"
