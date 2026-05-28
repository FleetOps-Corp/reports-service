"""Unit Tests - PDF Builder
Responsabilidad: Tests para builder de PDF
Capa: Tests
"""
import pytest
from ..domain.services import PDFBuilder
from ..domain.models import ChartDefinition


class TestPDFBuilder:
    """Test PDFBuilder pattern."""
    
    def test_builder_chain(self):
        """Test builder pattern chaining."""
        builder = PDFBuilder("REPORT-001", "BOGOTA")
        
        chart = ChartDefinition(
            chart_id="CHART-1",
            chart_type="LINE",
            title="Chart 1",
            data_source="MONGODB_KPI",
            x_axis_label="X",
            y_axis_label="Y",
        )
        
        report = (
            builder
            .add_availability_chart(chart)
            .add_kpi_summary({"availability": 84.5})
            .set_minio_url("http://minio:9000/report.pdf")
            .build()
        )
        
        assert report.report_id == "REPORT-001"
        assert len(report.chart_ids) == 1
        assert report.kpi_summary["availability"] == 84.5
        assert report.minio_url == "http://minio:9000/report.pdf"
    
    def test_builder_incomplete_fails(self):
        """Test builder fails when incomplete."""
        builder = PDFBuilder("REPORT-001", "BOGOTA")
        
        with pytest.raises(ValueError):
            builder.build()
