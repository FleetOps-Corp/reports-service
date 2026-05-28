"""Domain Model - PDF Report
Responsabilidad: Representa un reporte PDF consolidado
Patrón: Domain Model + Builder Pattern
Capa: Domain
"""
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class PDFReport(BaseModel):
    """Representa un reporte PDF consolidado.
    
    Patrón: Domain Model (DDD) + Builder Pattern
    Responsabilidad: Encapsular lógica de construcción de reportes
    """
    
    report_id: str = Field(..., description="Identificador único del reporte")
    title: str = Field(..., description="Título del reporte ejecutivo")
    period_start: datetime = Field(..., description="Inicio del período reportado")
    period_end: datetime = Field(..., description="Fin del período reportado")
    fleet_location: str = Field(..., description="Ubicación/sede del reporte")
    chart_ids: List[str] = Field(default_factory=list, description="Gráficas incluidas")
    kpi_summary: Dict = Field(default_factory=dict, description="Resumen de KPIs")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    file_size_bytes: Optional[int] = None
    minio_url: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "REPORT-2026-05",
                "title": "Fleet Operations Report - May 2026",
                "period_start": "2026-05-01T00:00:00Z",
                "period_end": "2026-05-31T23:59:59Z",
                "fleet_location": "BOGOTA",
                "chart_ids": ["CHART-AVAIL-001"],
                "kpi_summary": {"availability": 84.5},
                "generated_at": "2026-05-28T10:00:00Z"
            }
        }
    
    def is_complete(self) -> bool:
        """Validar que el reporte tenga todos los elementos."""
        return (
            len(self.chart_ids) > 0 and
            len(self.kpi_summary) > 0 and
            self.minio_url is not None
        )
    
    def get_minio_key(self) -> str:
        """Generar clave de almacenamiento en MinIO."""
        return f"reports/{self.fleet_location}/{self.report_id}.pdf"
