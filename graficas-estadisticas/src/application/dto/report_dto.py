"""Application DTOs - Report DTO
Responsabilidad: Data Transfer Object para reportes generados
Capa: Application
"""
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field


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
                "generated_at": "2026-05-28T10:00:00Z",
                "download_url": "http://minio:9000/reports/BOGOTA/REPORT-BOGOTA-2026-05.pdf"
            }
        }
