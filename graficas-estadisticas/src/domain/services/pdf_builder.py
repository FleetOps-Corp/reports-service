"""Domain Services - PDF Builder
Responsabilidad: Construir reportes PDF ejecutivos
Patrón: Builder Pattern
Capa: Domain
"""
from typing import Dict
from .chart_generator import ChartGenerator
from ..models import PDFReport, ChartDefinition


class PDFBuilder:
    """Construye reportes PDF ejecutivos.
    
    Patrón: Builder Pattern
    Responsabilidad: Orquestar construcción de reportes complejos
    """
    
    def __init__(self, report_id: str, location: str):
        """Initialize report builder."""
        self.report = PDFReport(
            report_id=report_id,
            title=f"Fleet Operations Report - {location}",
            period_start=__import__('datetime').datetime.utcnow(),
            period_end=__import__('datetime').datetime.utcnow(),
            fleet_location=location,
        )
    
    def add_availability_chart(self, chart: ChartDefinition) -> "PDFBuilder":
        """Add availability chart to report."""
        self.report.chart_ids.append(chart.chart_id)
        return self
    
    def add_incident_chart(self, chart: ChartDefinition) -> "PDFBuilder":
        """Add incident chart to report."""
        self.report.chart_ids.append(chart.chart_id)
        return self
    
    def add_kpi_summary(self, kpis: Dict) -> "PDFBuilder":
        """Add KPI summary to report."""
        self.report.kpi_summary = kpis
        return self
    
    def set_minio_url(self, url: str) -> "PDFBuilder":
        """Set MinIO storage URL."""
        self.report.minio_url = url
        return self
    
    def build(self) -> PDFReport:
        """Build and return the report."""
        if not self.report.is_complete():
            raise ValueError("Report is incomplete. Add charts and KPIs before building.")
        return self.report
