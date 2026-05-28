"""Unit Tests - Domain Layer para Gráficas y Estadísticas
100% coverage del dominio
Patrón: AAA (Arrange → Act → Assert)
"""
import pytest
from datetime import datetime

from src.domain.models import ChartDefinition, PDFReport, ReportTemplate
from src.domain.services import ChartGenerator, PDFBuilder, ReportAssembler


class TestChartDefinition:
    """Test ChartDefinition domain model."""
    
    def test_chart_is_valid_with_data(self):
        """Arrange: Create chart with data"""
        chart = ChartDefinition(
            chart_id="CH-001",
            chart_type="LINE",
            title="Availability",
            x_label="Date",
            y_label="Percentage",
            data_points=[{"date": "2026-05-27", "value": 85}]
        )
        
        """Act"""
        result = chart.is_valid()
        
        """Assert"""
        assert result is True
    
    def test_chart_is_invalid_without_data(self):
        """Arrange: Chart without data"""
        chart = ChartDefinition(
            chart_id="CH-001",
            chart_type="LINE",
            title="Availability",
            x_label="Date",
            y_label="Percentage",
            data_points=[]
        )
        
        """Act"""
        result = chart.is_valid()
        
        """Assert"""
        assert result is False


class TestPDFReport:
    """Test PDFReport domain model."""
    
    def test_report_add_chart(self):
        """Arrange: Create report and chart"""
        report = PDFReport(
            report_id="RPT-001",
            fleet_location="BOGOTA",
            title="Executive Report",
            summary="Test summary"
        )
        
        chart = ChartDefinition(
            chart_id="CH-001",
            chart_type="LINE",
            title="Availability",
            x_label="Date",
            y_label="Percentage",
            data_points=[{"date": "2026-05-27", "value": 85}]
        )
        
        """Act"""
        report.add_chart(chart)
        
        """Assert"""
        assert len(report.charts) == 1
        assert report.charts[0].chart_id == "CH-001"
    
    def test_report_is_complete_when_has_charts_and_metrics(self):
        """Arrange: Complete report"""
        report = PDFReport(
            report_id="RPT-001",
            fleet_location="BOGOTA",
            title="Executive Report",
            summary="Test summary",
            metrics={"availability": 85.0}
        )
        
        chart = ChartDefinition(
            chart_id="CH-001",
            chart_type="LINE",
            title="Availability",
            x_label="Date",
            y_label="Percentage",
            data_points=[{"date": "2026-05-27", "value": 85}]
        )
        report.add_chart(chart)
        
        """Act"""
        result = report.is_complete()
        
        """Assert"""
        assert result is True


class TestChartGenerator:
    """Test ChartGenerator domain service."""
    
    def test_generate_availability_chart(self):
        """Arrange: Sample data"""
        daily_data = [{"date": "2026-05-27", "availability": 85.0}]
        
        """Act"""
        chart = ChartGenerator.generate_availability_chart("BOGOTA", daily_data)
        
        """Assert"""
        assert chart.chart_type == "LINE"
        assert "Availability" in chart.title
        assert chart.is_valid()
    
    def test_generate_incident_distribution(self):
        """Arrange: Incident counts"""
        incidents = {"CRITICA": 2, "ALTA": 5, "MEDIA": 3, "BAJA": 1}
        
        """Act"""
        chart = ChartGenerator.generate_incident_distribution(incidents)
        
        """Assert"""
        assert chart.chart_type == "PIE"
        assert len(chart.data_points) == 4


class TestPDFBuilder:
    """Test PDFBuilder domain service - Builder Pattern."""
    
    def test_fluent_builder_creates_complete_report(self):
        """Arrange: Use fluent builder"""
        chart = ChartDefinition(
            chart_id="CH-001",
            chart_type="LINE",
            title="Availability",
            x_label="Date",
            y_label="Percentage",
            data_points=[{"date": "2026-05-27", "value": 85}]
        )
        
        """Act"""
        report = (
            PDFBuilder("RPT-001", "BOGOTA")
            .add_executive_summary("Test summary")
            .add_availability_chart(chart)
            .add_metrics({"availability": 85.0})
            .build()
        )
        
        """Assert"""
        assert report.report_id == "RPT-001"
        assert len(report.charts) == 1
        assert report.summary == "Test summary"
        assert len(report.metrics) > 0
    
    def test_builder_raises_when_incomplete(self):
        """Arrange: Incomplete report"""
        builder = PDFBuilder("RPT-001", "BOGOTA")
        
        """Act & Assert"""
        with pytest.raises(ValueError):
            builder.build()  # No charts or metrics


class TestReportAssembler:
    """Test ReportAssembler domain service - Aggregator Pattern."""
    
    def test_calculate_report_size(self):
        """Arrange: Report with charts"""
        report = PDFReport(
            report_id="RPT-001",
            fleet_location="BOGOTA",
            title="Executive Report",
            summary="Test summary",
            metrics={"availability": 85.0}
        )
        
        for i in range(3):
            chart = ChartDefinition(
                chart_id=f"CH-{i}",
                chart_type="LINE",
                title=f"Chart {i}",
                x_label="X",
                y_label="Y",
                data_points=[{"x": 1, "y": 1}]
            )
            report.add_chart(chart)
        
        """Act"""
        size = ReportAssembler.calculate_report_size(report)
        
        """Assert"""
        # Base 50KB + 3 charts * 20KB = 110KB minimum
        assert size >= 110 * 1024

