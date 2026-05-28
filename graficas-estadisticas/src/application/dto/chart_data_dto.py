"""Application DTOs - Chart Data
Responsabilidad: Data Transfer Object para datos de gráfica
Capa: Application
"""
from typing import List, Dict
from pydantic import BaseModel, Field


class ChartDataDTO(BaseModel):
    """DTO para datos de gráfica."""
    
    chart_id: str
    chart_type: str
    title: str
    data_points: List[Dict] = Field(default_factory=list)
    x_axis_label: str
    y_axis_label: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "chart_id": "CHART-AVAIL-001",
                "chart_type": "LINE",
                "title": "Availability Trend",
                "data_points": [
                    {"date": "2026-05-01", "value": 82.5},
                    {"date": "2026-05-02", "value": 84.2}
                ],
                "x_axis_label": "Date",
                "y_axis_label": "Availability %"
            }
        }
