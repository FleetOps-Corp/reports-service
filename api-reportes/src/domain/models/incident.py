"""Domain Model: Incident
Representa un incidente histórico asociado a un vehículo.
Responsabilidad: Encapsular datos de incidentes para análisis de patrones.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Incident(BaseModel):
    """Registro histórico de un incidente en un vehículo.
    
    Patrón: Domain Model (DDD)
    Capa: Domain - Lógica de negocio pura
    """
    
    incident_id: str = Field(..., description="Identificador único del incidente")
    vehicle_id: str = Field(..., description="Vehículo afectado")
    severity: str = Field(..., description="Severidad: CRITICA, ALTA, MEDIA, BAJA")
    description: str = Field(..., description="Descripción del incidente")
    occurred_at: datetime = Field(..., description="Fecha/hora del incidente")
    resolved_at: Optional[datetime] = Field(None, description="Fecha/hora de resolución")
    root_cause: Optional[str] = Field(None, description="Causa raíz identificada")
    
    class Config:
        json_schema_extra = {
            "example": {
                "incident_id": "INC-2026-001",
                "vehicle_id": "VH-001",
                "severity": "ALTA",
                "description": "Fallo en sistema de frenos",
                "occurred_at": "2026-05-20T14:30:00Z",
                "resolved_at": "2026-05-21T09:15:00Z",
                "root_cause": "Desgaste de pastillas de freno"
            }
        }
    
    def is_resolved(self) -> bool:
        """Determine if the incident has been resolved.
        
        Returns:
            bool: True if resolved_at is set
        """
        return self.resolved_at is not None
    
    def resolution_time_hours(self) -> Optional[float]:
        """Calculate time to resolution in hours.
        
        Returns:
            float: Hours between occurrence and resolution, None if unresolved
        """
        if not self.is_resolved():
            return None
        delta = self.resolved_at - self.occurred_at
        return delta.total_seconds() / 3600.0
    
    def is_critical(self) -> bool:
        """Determine if incident is critical for operations.
        
        Returns:
            bool: True if severity is CRITICA
        """
        return self.severity == "CRITICA"
