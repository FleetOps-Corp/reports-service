"""Domain Services - Report Assembler
Responsabilidad: Ensamblar datos para generar reportes
Patrón: Aggregator Pattern
Capa: Domain
"""
from typing import List, Dict
from ..models import ChartDefinition, PDFReport
from .pdf_builder import PDFBuilder


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
        """Assemble complete executive report."""
        builder = PDFBuilder(
            report_id=f"REPORT-{location}-{__import__('datetime').datetime.utcnow().strftime('%Y-%m')}",
            location=location,
        )
        
        for chart in charts:
            builder.add_incident_chart(chart)
        
        builder.add_kpi_summary(kpis)
        
        return builder.build()
