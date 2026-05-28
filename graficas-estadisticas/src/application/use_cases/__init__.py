"""Application Layer - Use Cases for Report Generation
Responsabilidad: Orquestar generación de reportes.
Patrón: Use Case / Application Service
Capa: Application
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..dto import ReportDTO, GeneralReportRequestDTO, ChartDataDTO
from ...domain.models import ChartDefinition, PDFReport
from ...domain.services import ChartGenerator, PDFReportBuilder, ReportAssembler


class GenerateGeneralReportUseCase:
    """Use Case: Generar reporte general consolidado.
    
    Patrón: Use Case / Application Service
    Responsabilidad: Orquestar flujo completo de generación
    """
    
    def __init__(self, mongodb_repo, minio_storage):
        """Initialize use case with dependencies.
        
        Args:
            mongodb_repo: Repository para leer datos de MongoDB
            minio_storage: Adapter para escribir en MinIO
        """
        self.mongodb_repo = mongodb_repo
        self.minio_storage = minio_storage
    
    async def execute(self, request: GeneralReportRequestDTO) -> ReportDTO:
        """Execute: Generar reporte consolidado.
        
        Flujo:
        1. Obtener datos de MongoDB
        2. Generar gráficas según especificación
        3. Construir PDF con builder pattern
        4. Persistir en MinIO
        5. Retornar DTO con URL
        
        Args:
            request: Solicitud de reporte
            
        Returns:
            ReportDTO: Reporte generado
        """
        # Step 1: Get KPI data from MongoDB
        kpis = await self._fetch_kpis(request.location, request.period_months)
        
        # Step 2: Generate charts
        charts = []
        if "availability" in request.include_charts:
            availability_data = await self._fetch_availability_data(request.location)
            charts.append(
                ChartGenerator.generate_availability_chart(
                    request.location,
                    availability_data
                )
            )
        
        if "incidents" in request.include_charts:
            incident_data = await self._fetch_incident_data(request.location)
            charts.append(
                ChartGenerator.generate_incident_chart(
                    request.location,
                    incident_data
                )
            )
        
        if "maintenance" in request.include_charts:
            maintenance_data = await self._fetch_maintenance_data(request.location)
            charts.append(
                ChartGenerator.generate_maintenance_chart(
                    request.location,
                    maintenance_data
                )
            )
        
        if "mttr" in request.include_charts:
            mttr_data = await self._fetch_mttr_data(request.location)
            charts.append(
                ChartGenerator.generate_mttr_chart(
                    request.location,
                    mttr_data
                )
            )
        
        # Step 3: Assemble report
        pdf_report = await ReportAssembler.assemble_executive_report(
            request.location,
            kpis,
            charts
        )
        
        # Step 4: Store in MinIO
        minio_url = await self.minio_storage.store_report(pdf_report)
        pdf_report.minio_url = minio_url
        
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
        # Implementation would query MongoDB
        return {
            "availability": 84.5,
            "mttr": 4.2,
            "incident_count": 12,
            "preventive_ratio": 0.65,
        }
    
    async def _fetch_availability_data(self, location: str) -> List[Dict]:
        """Fetch availability metrics."""
        return []
    
    async def _fetch_incident_data(self, location: str) -> List[Dict]:
        """Fetch incident data."""
        return []
    
    async def _fetch_maintenance_data(self, location: str) -> List[Dict]:
        """Fetch maintenance data."""
        return []
    
    async def _fetch_mttr_data(self, location: str) -> List[Dict]:
        """Fetch MTTR data."""
        return []


class GetAvailabilityDataUseCase:
    """Use Case: Obtener datos de disponibilidad consolidados."""
    
    def __init__(self, mongodb_repo):
        self.mongodb_repo = mongodb_repo
    
    async def execute(self, location: str) -> ChartDataDTO:
        """Execute: Get availability data.
        
        Args:
            location: Fleet location
            
        Returns:
            ChartDataDTO: Availability data for charting
        """
        # Implementation would query MongoDB
        return ChartDataDTO(
            chart_id="CHART-AVAIL",
            chart_type="LINE",
            title=f"Availability - {location}",
            data_points=[],
            x_axis_label="Date",
            y_axis_label="Availability %",
        )


class GetIncidentDataUseCase:
    """Use Case: Obtener datos de incidentes."""
    
    def __init__(self, mongodb_repo):
        self.mongodb_repo = mongodb_repo
    
    async def execute(self, location: str) -> ChartDataDTO:
        """Execute: Get incident data."""
        return ChartDataDTO(
            chart_id="CHART-INC",
            chart_type="BAR",
            title=f"Incidents - {location}",
            data_points=[],
            x_axis_label="Severity",
            y_axis_label="Count",
        )


class GetMaintenanceDataUseCase:
    """Use Case: Obtener datos de mantenimiento."""
    
    def __init__(self, mongodb_repo):
        self.mongodb_repo = mongodb_repo
    
    async def execute(self, location: str) -> ChartDataDTO:
        """Execute: Get maintenance data."""
        return ChartDataDTO(
            chart_id="CHART-MAINT",
            chart_type="PIE",
            title=f"Maintenance Types - {location}",
            data_points=[],
            x_axis_label="Type",
            y_axis_label="Count",
        )


class GetMTTRDataUseCase:
    """Use Case: Obtener datos de MTTR."""
    
    def __init__(self, mongodb_repo):
        self.mongodb_repo = mongodb_repo
    
    async def execute(self, location: str) -> ChartDataDTO:
        """Execute: Get MTTR data."""
        return ChartDataDTO(
            chart_id="CHART-MTTR",
            chart_type="LINE",
            title=f"MTTR Evolution - {location}",
            data_points=[],
            x_axis_label="Month",
            y_axis_label="Hours",
        )
