"""Application Layer - DTOs for Charts and Reports
Responsabilidad: Transferencia de datos entre capas.
Patrón: DTO Pattern
Capa: Application
"""
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class ChartDataDTO(BaseModel):
    """DTO para datos de gráfica."""
    chart_id: str
    chart_type: str
    title: str
    data_points: List[Dict]
    x_axis_label: str
    y_axis_label: str


class ReportDTO(BaseModel):
    """DTO para reporte generado."""
    report_id: str
    title: str
    period_start: datetime
    period_end: datetime
    fleet_location: str
    chart_count: int
    kpi_summary: Dict
    generated_at: datetime
    download_url: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "REPORT-BOGOTA-2026-05",
                "title": "Fleet Operations Report - May 2026",
                "period_start": "2026-05-01T00:00:00Z",
                "period_end": "2026-05-31T23:59:59Z",
                "fleet_location": "BOGOTA",
                "chart_count": 4,
                "kpi_summary": {
                    "availability": 84.5,
                    "mttr": 4.2,
                    "incident_count": 12
                },
                "generated_at": "2026-05-27T22:00:00Z",
                "download_url": "http://minio:9000/reports/BOGOTA/REPORT-BOGOTA-2026-05.pdf"
            }
        }


class GeneralReportRequestDTO(BaseModel):
    """DTO para solicitar generación de reporte general."""
    location: str = Field(..., description="Ubicación/sede")
    period_months: int = Field(default=1, description="Período en meses")
    include_charts: List[str] = Field(
        default_factory=lambda: ["availability", "incidents", "maintenance", "mttr"],
        description="Gráficas a incluir"
    )
