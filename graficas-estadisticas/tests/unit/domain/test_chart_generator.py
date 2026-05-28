"""Unit Tests - Chart Generator
Responsabilidad: Tests para generador de gráficas
Capa: Tests
"""
import pytest
from ..domain.services import ChartGenerator


class TestChartGenerator:
    """Test ChartGenerator service."""
    
    @pytest.mark.asyncio
    async def test_generate_availability_chart(self):
        """Test availability chart generation."""
        data_points = [
            {"date": "2026-05-01", "availability": 80.0},
            {"date": "2026-05-02", "availability": 82.5},
        ]
        
        chart = await ChartGenerator.generate_availability_chart(
            "BOGOTA",
            data_points
        )
        
        assert chart.chart_type == "LINE"
        assert "Availability" in chart.title
        assert chart.data_source == "MONGODB_KPI"
    
    @pytest.mark.asyncio
    async def test_generate_incident_chart(self):
        """Test incident chart generation."""
        incident_data = [
            {"severity": "CRITICA", "count": 2},
            {"severity": "ALTA", "count": 5},
        ]
        
        chart = await ChartGenerator.generate_incident_chart(
            "BOGOTA",
            incident_data
        )
        
        assert chart.chart_type == "BAR"
        assert "Incident" in chart.title
        assert chart.data_source == "INCIDENTS"
    
    @pytest.mark.asyncio
    async def test_generate_maintenance_chart(self):
        """Test maintenance chart generation."""
        maintenance_data = [
            {"type": "PREVENTIVO", "count": 15},
            {"type": "CORRECTIVO", "count": 8},
        ]
        
        chart = await ChartGenerator.generate_maintenance_chart(
            "BOGOTA",
            maintenance_data
        )
        
        assert chart.chart_type == "PIE"
        assert "Maintenance" in chart.title
