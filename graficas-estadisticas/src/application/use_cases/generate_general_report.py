"""Application Use Case - Generate General Report
Responsabilidad: Orquestar generación de reportes
Capa: Application
"""
from typing import List, Dict
from datetime import datetime, timedelta
from ..dto import ReportDTO
from ...domain.models import ChartDefinition, PDFReport
from ...domain.services import ChartGenerator, PDFBuilder, ReportAssembler


class GenerateGeneralReportUseCase:
    """Use Case: Generar reporte general consolidado.
    
    Patrón: Use Case / Application Service
    """
    
    def __init__(self, mongodb_repo, minio_storage):
        """Initialize use case with dependencies."""
        self.mongodb_repo = mongodb_repo
        self.minio_storage = minio_storage
    
    async def execute(self, location: str, period_months: int = 1) -> ReportDTO:
        """Execute: Generar reporte consolidado."""
        # Step 1: Get KPI data from MongoDB
        kpis = await self._fetch_kpis(location, period_months)
        
        # Step 2: Generate charts
        charts = []
        availability_data = await self._fetch_availability_data(location)
        charts.append(
            await ChartGenerator.generate_availability_chart(location, availability_data)
        )
        
        # Step 3: Assemble report
        pdf_report = await ReportAssembler.assemble_executive_report(
            location,
            kpis,
            charts
        )
        
        # Step 4: Store in MinIO
        minio_url = await self.minio_storage.store_report(pdf_report)
        
        # Step 5: Return DTO
        return ReportDTO(
            report_id=pdf_report.report_id,
            title=pdf_report.title,
            period_start=pdf_report.period_start,
            period_end=pdf_report.period_end,
            fleet_location=pdf_report.fleet_location,
            chart_count=len(pdf_report.chart_ids),
            kpi_summary=pdf_report.kpi_summary,
            generated_at=pdf_report.generated_at,
            download_url=minio_url,
        )
    
    async def _fetch_kpis(self, location: str, months: int) -> Dict:
        """Fetch KPI data from MongoDB."""
        return {
            "availability": 84.5,
            "mttr": 4.2,
            "incident_count": 12,
        }
    
    async def _fetch_availability_data(self, location: str) -> List[Dict]:
        """Fetch availability metrics."""
        return []
