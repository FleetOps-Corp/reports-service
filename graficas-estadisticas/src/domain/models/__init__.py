"""Domain Layer - Chart and Report Models
Responsabilidad: Encapsular lógica de negocio para gráficas y reportes.
Patrón: Domain Models (DDD)
Capa: Domain
"""
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class ChartDefinition(BaseModel):
    """Define una gráfica a ser generada.
    
    Patrón: Domain Model (DDD)
    Capa: Domain - Lógica de negocio pura
    """
    
    chart_id: str = Field(..., description="Identificador único de la gráfica")
    chart_type: str = Field(..., description="Tipo: LINE, BAR, PIE, SCATTER")
    title: str = Field(..., description="Título de la gráfica")
    data_source: str = Field(..., description="Fuente de datos: MONGODB_KPI, INCIDENTS, MAINTENANCE")
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
                "y_axis_label": "Availability %",
                "created_at": "2026-05-27T22:00:00Z"
            }
        }


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
                "chart_ids": ["CHART-AVAIL-001", "CHART-INC-001"],
                "kpi_summary": {
                    "availability": 84.5,
                    "mttr": 4.2,
                    "incident_count": 12
                },
                "generated_at": "2026-05-27T22:00:00Z"
            }
        }
    
    def is_complete(self) -> bool:
        """Validar que el reporte tenga todos los elementos.
        
        Returns:
            bool: True si reporte está completo
        """
        return (
            len(self.chart_ids) > 0 and
            len(self.kpi_summary) > 0 and
            self.minio_url is not None
        )
    
    def get_minio_key(self) -> str:
        """Generar clave de almacenamiento en MinIO.
        
        Returns:
            str: Clave para MinIO bucket
        """
        return f"reports/{self.fleet_location}/{self.report_id}.pdf"
