"""Domain Model - Chart Definition
Responsabilidad: Definir una gráfica a ser generada
Patrón: Domain Model (DDD)
Capa: Domain
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChartDefinition(BaseModel):
    """Define una gráfica a ser generada.
    
    Patrón: Domain Model (DDD)
    Capa: Domain - Lógica de negocio pura
    """
    
    chart_id: str = Field(..., description="Identificador único de la gráfica")
    chart_type: str = Field(..., description="Tipo: LINE, BAR, PIE, SCATTER")
    title: str = Field(..., description="Título de la gráfica")
    data_source: str = Field(..., description="Fuente de datos")
    x_axis_label: str = Field(..., description="Etiqueta del eje X")
    y_axis_label: str = Field(..., description="Etiqueta del eje Y")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "chart_id": "CHART-AVAIL-001",
                "chart_type": "LINE",
                "title": "Fleet Availability Trend",
                "data_source": "MONGODB_KPI",
                "x_axis_label": "Date",
                "y_axis_label": "Availability %"
            }
        }
