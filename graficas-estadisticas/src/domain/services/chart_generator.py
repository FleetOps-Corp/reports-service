"""Domain Services - Chart Generator
Responsabilidad: Generar gráficas a partir de datos
Patrón: Strategy Pattern, Service
Capa: Domain
"""
from typing import List, Dict
from .chart_definition import ChartDefinition


class ChartGenerator:
    """Genera gráficas a partir de datos.
    
    Patrón: Strategy Pattern
    Responsabilidad: Encapsular lógica de generación de gráficas
    """
    
    @staticmethod
    async def generate_availability_chart(
        location: str,
        data_points: List[Dict]
    ) -> ChartDefinition:
        """Generate availability trend chart."""
        return ChartDefinition(
            chart_id=f"CHART-AVAIL-{location}",
            chart_type="LINE",
            title=f"Fleet Availability Trend - {location}",
            data_source="MONGODB_KPI",
            x_axis_label="Date",
            y_axis_label="Availability %",
        )
    
    @staticmethod
    async def generate_incident_chart(
        location: str,
        incident_data: List[Dict]
    ) -> ChartDefinition:
        """Generate incident analysis chart."""
        return ChartDefinition(
            chart_id=f"CHART-INC-{location}",
            chart_type="BAR",
            title=f"Incident Distribution - {location}",
            data_source="INCIDENTS",
            x_axis_label="Severity Level",
            y_axis_label="Count",
        )
    
    @staticmethod
    async def generate_maintenance_chart(
        location: str,
        maintenance_data: List[Dict]
    ) -> ChartDefinition:
        """Generate preventive vs corrective maintenance chart."""
        return ChartDefinition(
            chart_id=f"CHART-MAINT-{location}",
            chart_type="PIE",
            title=f"Maintenance Type Distribution - {location}",
            data_source="MAINTENANCE",
            x_axis_label="Type",
            y_axis_label="Percentage",
        )
    
    @staticmethod
    async def generate_mttr_chart(
        location: str,
        mttr_data: List[Dict]
    ) -> ChartDefinition:
        """Generate MTTR evolution chart."""
        return ChartDefinition(
            chart_id=f"CHART-MTTR-{location}",
            chart_type="LINE",
            title=f"MTTR Evolution - {location}",
            data_source="MONGODB_KPI",
            x_axis_label="Month",
            y_axis_label="Hours",
        )
