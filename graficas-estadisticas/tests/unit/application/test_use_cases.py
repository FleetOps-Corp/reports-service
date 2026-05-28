"""Unit Tests - Application Layer (Gráficas y Estadísticas)
Responsabilidad: Tests de casos de uso
"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from src.application.use_cases import (
    GenerateGeneralReportUseCase,
    GetAvailabilityDataUseCase,
    GetIncidentDataUseCase,
    GetMaintenanceDataUseCase,
    GetMTTRDataUseCase,
)
from src.application.dto import GeneralReportRequestDTO


class TestGenerateGeneralReportUseCase:
    """Test GenerateGeneralReportUseCase."""
    
    @pytest.mark.asyncio
    async def test_execute_generates_report(self):
        """Arrange: Mock repositories"""
        mock_mongodb = AsyncMock()
        mock_minio = AsyncMock()
        mock_minio.store_report.return_value = "http://minio:9000/report.pdf"
        
        use_case = GenerateGeneralReportUseCase(mock_mongodb, mock_minio)
        
        request = GeneralReportRequestDTO(
            location="BOGOTA",
            period_months=1,
            include_charts=["availability", "incidents"]
        )
        
        """Act"""
        result = await use_case.execute(request)
        
        """Assert"""
        assert result.fleet_location == "BOGOTA"
        assert result.chart_count >= 0
        assert result.download_url == "http://minio:9000/report.pdf"


class TestGetAvailabilityDataUseCase:
    """Test availability data retrieval."""
    
    @pytest.mark.asyncio
    async def test_execute_returns_chart_data(self):
        """Test availability data execution."""
        mock_repo = AsyncMock()
        use_case = GetAvailabilityDataUseCase(mock_repo)
        
        """Act"""
        result = await use_case.execute("BOGOTA")
        
        """Assert"""
        assert result.chart_id == "CHART-AVAIL"
        assert result.chart_type == "LINE"


class TestGetIncidentDataUseCase:
    """Test incident data retrieval."""
    
    @pytest.mark.asyncio
    async def test_execute_returns_chart_data(self):
        """Test incident data execution."""
        mock_repo = AsyncMock()
        use_case = GetIncidentDataUseCase(mock_repo)
        
        """Act"""
        result = await use_case.execute("BOGOTA")
        
        """Assert"""
        assert result.chart_id == "CHART-INC"
        assert result.chart_type == "BAR"


class TestGetMaintenanceDataUseCase:
    """Test maintenance data retrieval."""
    
    @pytest.mark.asyncio
    async def test_execute_returns_chart_data(self):
        """Test maintenance data execution."""
        mock_repo = AsyncMock()
        use_case = GetMaintenanceDataUseCase(mock_repo)
        
        """Act"""
        result = await use_case.execute("BOGOTA")
        
        """Assert"""
        assert result.chart_id == "CHART-MAINT"
        assert result.chart_type == "PIE"


class TestGetMTTRDataUseCase:
    """Test MTTR data retrieval."""
    
    @pytest.mark.asyncio
    async def test_execute_returns_chart_data(self):
        """Test MTTR data execution."""
        mock_repo = AsyncMock()
        use_case = GetMTTRDataUseCase(mock_repo)
        
        """Act"""
        result = await use_case.execute("BOGOTA")
        
        """Assert"""
        assert result.chart_id == "CHART-MTTR"
        assert result.chart_type == "LINE"
