"""Unit Tests - Domain Layer (Gráficas y Estadísticas)
Responsabilidad: Tests del dominio con 100% coverage
Patrón: AAA (Arrange → Act → Assert)
"""
import pytest
from datetime import datetime

from src.domain.models import ChartDefinition, PDFReport
from src.domain.services import (
    ChartGenerator,
    PDFReportBuilder,
    ReportAssembler,
)


class TestChartDefinition:
    """Test ChartDefinition domain model."""
    
    def test_create_availability_chart(self):
        """Arrange: Create availability chart"""
        chart = ChartDefinition(
            chart_id="CHART-AVAIL-BOGOTA",
            chart_type="LINE",
            title="Fleet Availability Trend",
            data_source="MONGODB_KPI",
            x_axis_label="Date",
            y_axis_label="Availability %",
        )
        
        """Act & Assert"""
        assert chart.chart_id == "CHART-AVAIL-BOGOTA"
        assert chart.chart_type == "LINE"
        assert chart.title == "Fleet Availability Trend"


class TestPDFReport:
    """Test PDFReport domain model."""
    
    def test_pdf_report_incomplete(self):
        """Arrange: Report with no data"""
        report = PDFReport(
            report_id="REPORT-001",
            title="Test Report",
            period_start=datetime.utcnow(),
            period_end=datetime.utcnow(),
            fleet_location="BOGOTA",
        )
        
        """Act"""
        result = report.is_complete()
        
        """Assert"""
        assert result is False
    
    def test_pdf_report_complete(self):
        """Arrange: Complete report"""
        report = PDFReport(
            report_id="REPORT-001",
            title="Test Report",
            period_start=datetime.utcnow(),
            period_end=datetime.utcnow(),
            fleet_location="BOGOTA",
            chart_ids=["CHART-1", "CHART-2"],
            kpi_summary={"availability": 84.5},
            minio_url="http://minio:9000/reports/report.pdf",
        )
        
        """Act"""
        result = report.is_complete()
        
        """Assert"""
        assert result is True
    
    def test_minio_key_generation(self):
        """Test MinIO key generation."""
        report = PDFReport(
            report_id="REPORT-BOGOTA-2026-05",
            title="Test Report",
            period_start=datetime.utcnow(),
            period_end=datetime.utcnow(),
            fleet_location="BOGOTA",
        )
        
        """Act"""
        key = report.get_minio_key()
        
        """Assert"""
        assert key == "reports/BOGOTA/REPORT-BOGOTA-2026-05.pdf"


class TestChartGenerator:
    """Test ChartGenerator domain service."""
    
    def test_generate_availability_chart(self):
        """Test availability chart generation."""
        data_points = [
            {"date": "2026-05-01", "availability": 80.0},
            {"date": "2026-05-02", "availability": 82.5},
        ]
        
        """Act"""
        chart = ChartGenerator.generate_availability_chart(
            "BOGOTA",
            data_points
        )
        
        """Assert"""
        assert chart.chart_type == "LINE"
        assert "Availability" in chart.title
        assert chart.data_source == "MONGODB_KPI"
    
    def test_generate_incident_chart(self):
        """Test incident chart generation."""
        incident_data = [
            {"severity": "CRITICA", "count": 2},
            {"severity": "ALTA", "count": 5},
        ]
        
        """Act"""
        chart = ChartGenerator.generate_incident_chart(
            "BOGOTA",
            incident_data
        )
        
        """Assert"""
        assert chart.chart_type == "BAR"
        assert "Incident" in chart.title
        assert chart.data_source == "INCIDENTS"
    
    def test_generate_maintenance_chart(self):
        """Test maintenance chart generation."""
        maintenance_data = [
            {"type": "PREVENTIVO", "count": 15},
            {"type": "CORRECTIVO", "count": 8},
        ]
        
        """Act"""
        chart = ChartGenerator.generate_maintenance_chart(
            "BOGOTA",
            maintenance_data
        )
        
        """Assert"""
        assert chart.chart_type == "PIE"
        assert "Maintenance" in chart.title
        assert chart.data_source == "MAINTENANCE"
    
    def test_generate_mttr_chart(self):
        """Test MTTR chart generation."""
        mttr_data = [
            {"month": "2026-03", "mttr": 4.5},
            {"month": "2026-04", "mttr": 4.2},
            {"month": "2026-05", "mttr": 4.8},
        ]
        
        """Act"""
        chart = ChartGenerator.generate_mttr_chart(
            "BOGOTA",
            mttr_data
        )
        
        """Assert"""
        assert chart.chart_type == "LINE"
        assert "MTTR" in chart.title
        assert chart.data_source == "MONGODB_KPI"


class TestPDFReportBuilder:
    """Test PDFReportBuilder pattern."""
    
    def test_builder_chain(self):
        """Test builder pattern chaining."""
        builder = PDFReportBuilder("REPORT-001", "BOGOTA")
        
        chart1 = ChartDefinition(
            chart_id="CHART-1",
            chart_type="LINE",
            title="Chart 1",
            data_source="MONGODB_KPI",
            x_axis_label="X",
            y_axis_label="Y",
        )
        
        """Act"""
        report = (
            builder
            .add_availability_chart(chart1)
            .add_kpi_summary({"availability": 84.5})
            .set_minio_url("http://minio:9000/report.pdf")
            .build()
        )
        
        """Assert"""
        assert report.report_id == "REPORT-001"
        assert len(report.chart_ids) == 1
        assert report.kpi_summary["availability"] == 84.5
        assert report.minio_url == "http://minio:9000/report.pdf"
    
    def test_builder_incomplete_fails(self):
        """Test builder fails when incomplete."""
        builder = PDFReportBuilder("REPORT-001", "BOGOTA")
        
        """Act & Assert"""
        with pytest.raises(ValueError):
            builder.build()


class TestReportAssembler:
    """Test ReportAssembler aggregator pattern."""
    
    @pytest.mark.asyncio
    async def test_assemble_executive_report(self):
        """Test assembly of complete executive report."""
        location = "BOGOTA"
        kpis = {
            "availability": 84.5,
            "mttr": 4.2,
            "incident_count": 12,
        }
        charts = [
            ChartDefinition(
                chart_id="CHART-1",
                chart_type="LINE",
                title="Chart 1",
                data_source="MONGODB_KPI",
                x_axis_label="X",
                y_axis_label="Y",
            ),
        ]
        
        """Act"""
        report = await ReportAssembler.assemble_executive_report(
            location,
            kpis,
            charts
        )
        
        """Assert"""
        assert report.fleet_location == location
        assert len(report.chart_ids) == 1
        assert report.kpi_summary == kpis
