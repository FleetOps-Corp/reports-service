"""Domain Services - Chart and Report Generation Logic
Responsabilidad: Generar gráficas y reportes según reglas de negocio.
Patrón: Builder Pattern, Strategy Pattern
Capa: Domain
"""
from typing import List, Dict, Optional
from datetime import datetime
from .models import ChartDefinition, PDFReport


class ChartGenerator:
    """Genera gráficas a partir de datos.
    
    Patrón: Strategy Pattern
    Responsabilidad: Encapsular lógica de generación de gráficas
    """
    
    @staticmethod
    def generate_availability_chart(
        location: str,
        data_points: List[Dict]
    ) -> ChartDefinition:
        """Generate availability trend chart.
        
        Args:
            location: Ubicación/sede
            data_points: Puntos de datos históricos
            
        Returns:
            ChartDefinition: Gráfica definida
        """
        return ChartDefinition(
            chart_id=f"CHART-AVAIL-{location}",
            chart_type="LINE",
            title=f"Fleet Availability Trend - {location}",
            data_source="MONGODB_KPI",
            x_axis_label="Date",
            y_axis_label="Availability %",
        )
    
    @staticmethod
    def generate_incident_chart(
        location: str,
        incident_data: List[Dict]
    ) -> ChartDefinition:
        """Generate incident analysis chart.
        
        Args:
            location: Ubicación
            incident_data: Datos de incidentes
            
        Returns:
            ChartDefinition: Gráfica de incidentes
        """
        return ChartDefinition(
            chart_id=f"CHART-INC-{location}",
            chart_type="BAR",
            title=f"Incident Distribution - {location}",
            data_source="INCIDENTS",
            x_axis_label="Severity Level",
            y_axis_label="Count",
        )
    
    @staticmethod
    def generate_maintenance_chart(
        location: str,
        maintenance_data: List[Dict]
    ) -> ChartDefinition:
        """Generate preventive vs corrective maintenance chart.
        
        Args:
            location: Ubicación
            maintenance_data: Datos de mantenimiento
            
        Returns:
            ChartDefinition: Gráfica de mantenimiento
        """
        return ChartDefinition(
            chart_id=f"CHART-MAINT-{location}",
            chart_type="PIE",
            title=f"Maintenance Type Distribution - {location}",
            data_source="MAINTENANCE",
            x_axis_label="Type",
            y_axis_label="Percentage",
        )
    
    @staticmethod
    def generate_mttr_chart(
        location: str,
        mttr_data: List[Dict]
    ) -> ChartDefinition:
        """Generate MTTR evolution chart.
        
        Args:
            location: Ubicación
            mttr_data: Datos de MTTR histórico
            
        Returns:
            ChartDefinition: Gráfica de MTTR
        """
        return ChartDefinition(
            chart_id=f"CHART-MTTR-{location}",
            chart_type="LINE",
            title=f"MTTR Evolution - {location}",
            data_source="MONGODB_KPI",
            x_axis_label="Month",
            y_axis_label="Hours",
        )


class PDFReportBuilder:
    """Construye reportes PDF ejecutivos.
    
    Patrón: Builder Pattern
    Responsabilidad: Orquestar construcción de reportes complejos
    """
    
    def __init__(self, report_id: str, location: str):
        """Initialize report builder.
        
        Args:
            report_id: ID del reporte
            location: Ubicación/sede
        """
        self.report = PDFReport(
            report_id=report_id,
            title=f"Fleet Operations Report - {location}",
            period_start=datetime.utcnow(),
            period_end=datetime.utcnow(),
            fleet_location=location,
        )
    
    def add_availability_chart(self, chart: ChartDefinition) -> "PDFReportBuilder":
        """Add availability chart to report.
        
        Returns:
            PDFReportBuilder: Self for chaining
        """
        self.report.chart_ids.append(chart.chart_id)
        return self
    
    def add_incident_chart(self, chart: ChartDefinition) -> "PDFReportBuilder":
        """Add incident chart to report.
        
        Returns:
            PDFReportBuilder: Self for chaining
        """
        self.report.chart_ids.append(chart.chart_id)
        return self
    
    def add_kpi_summary(self, kpis: Dict) -> "PDFReportBuilder":
        """Add KPI summary to report.
        
        Args:
            kpis: Dictionary of KPI values
            
        Returns:
            PDFReportBuilder: Self for chaining
        """
        self.report.kpi_summary = kpis
        return self
    
    def set_minio_url(self, url: str) -> "PDFReportBuilder":
        """Set MinIO storage URL.
        
        Args:
            url: MinIO presigned URL
            
        Returns:
            PDFReportBuilder: Self for chaining
        """
        self.report.minio_url = url
        return self
    
    def build(self) -> PDFReport:
        """Build and return the report.
        
        Returns:
            PDFReport: Constructed report
            
        Raises:
            ValueError: If report is incomplete
        """
        if not self.report.is_complete():
            raise ValueError("Report is incomplete. Add charts and KPIs before building.")
        return self.report


class ReportAssembler:
    """Ensambla datos para generar reportes.
    
    Patrón: Aggregator Pattern
    Responsabilidad: Consolidar datos de múltiples fuentes
    """
    
    @staticmethod
    async def assemble_executive_report(
        location: str,
        kpis: Dict,
        charts: List[ChartDefinition]
    ) -> PDFReport:
        """Assemble complete executive report.
        
        Args:
            location: Ubicación/sede
            kpis: KPI metrics
            charts: Gráficas para incluir
            
        Returns:
            PDFReport: Reporte ensamblado
        """
        builder = PDFReportBuilder(
            report_id=f"REPORT-{location}-{datetime.utcnow().strftime('%Y-%m')}",
            location=location,
        )
        
        for chart in charts:
            builder.add_incident_chart(chart)
        
        builder.add_kpi_summary(kpis)
        
        return builder.build()
