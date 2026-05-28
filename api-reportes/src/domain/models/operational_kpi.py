"""Domain Model: OperationalKPI
Representa un KPI operativo calculado para una sede o flota.
Responsabilidad: Encapsular y validar métricas operativas según reglas de negocio.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class OperationalKPI(BaseModel):
    """Indicador clave de rendimiento operativo.
    
    Patrón: Domain Model (DDD) + Value Object
    Capa: Domain - Lógica de negocio pura
    """
    
    kpi_id: str = Field(..., description="Identificador único del KPI")
    fleet_location: str = Field(..., description="Sede o región")
    total_vehicles: int = Field(..., ge=0, description="Total de vehículos")
    available_vehicles: int = Field(..., ge=0, description="Vehículos disponibles")
    availability_percentage: float = Field(..., ge=0.0, le=100.0, description="Porcentaje de disponibilidad")
    average_mttr_hours: float = Field(..., ge=0, description="MTTR promedio en horas")
    preventive_maintenance_ratio: float = Field(..., ge=0.0, le=1.0, description="Ratio mantenimiento preventivo")
    incident_count_month: int = Field(..., ge=0, description="Incidentes en el mes")
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "kpi_id": "KPI-BOGOTA-2026-05",
                "fleet_location": "BOGOTÁ",
                "total_vehicles": 50,
                "available_vehicles": 42,
                "availability_percentage": 84.0,
                "average_mttr_hours": 4.5,
                "preventive_maintenance_ratio": 0.65,
                "incident_count_month": 8,
                "calculated_at": "2026-05-27T22:00:00Z"
            }
        }
    
    def is_healthy(self) -> bool:
        """Validación de negocio: ¿La flota está en estado saludable?
        
        Criterios: Disponibilidad >= 80% Y MTTR <= 8 horas Y
        mantenimiento preventivo >= 50%
        
        Returns:
            bool: True si todos los criterios se cumplen
        """
        return (
            self.availability_percentage >= 80.0 and
            self.average_mttr_hours <= 8.0 and
            self.preventive_maintenance_ratio >= 0.5
        )
    
    def alert_level(self) -> str:
        """Determine alert level based on KPI thresholds.
        
        Returns:
            str: "CRITICAL", "WARNING", or "HEALTHY"
        """
        if self.availability_percentage < 70.0:
            return "CRITICAL"
        if self.average_mttr_hours > 12.0:
            return "CRITICAL"
        if self.availability_percentage < 80.0 or self.average_mttr_hours > 8.0:
            return "WARNING"
        return "HEALTHY"
