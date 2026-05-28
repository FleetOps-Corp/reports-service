"""Application Layer - DTOs for api-reportes
Responsabilidad: Data Transfer Objects
Patrón: DTO Pattern
Capa: Application
"""
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class VehicleDTO(BaseModel):
    """DTO para vehículo."""
    vehicle_id: str
    status: str
    location: str


class KPIResponseDTO(BaseModel):
    """DTO para respuesta de métrica KPI."""
    metric_name: str
    location: str
    value: float
    period_start: datetime
    period_end: datetime
    unit: str = "%"
    
    class Config:
        json_schema_extra = {
            "example": {
                "metric_name": "availability",
                "location": "BOGOTA",
                "value": 84.5,
                "period_start": "2026-04-28T00:00:00Z",
                "period_end": "2026-05-28T23:59:59Z",
                "unit": "%"
            }
        }


class TraceabilityDTO(BaseModel):
    """DTO para trazabilidad."""
    vehicle_id: str
    events: List[Dict]
    total_incidents: int
    total_maintenance: int
