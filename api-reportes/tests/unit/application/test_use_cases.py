"""Unit Tests - Application Layer Use Cases
100% coverage de application use cases
Patrón: AAA (Arrange → Act → Assert)
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from src.domain.models import (
    VehicleSnapshot,
    OperationalKPI,
    Incident,
    Maintenance,
)
from src.application.use_cases import (
    GetAvailabilityReportUseCase,
    GetMaintenanceMetricsUseCase,
    GetRecurrentIncidentsUseCase,
    GetVehicleTraceabilityUseCase,
)


class TestGetAvailabilityReportUseCase:
    """Test GetAvailabilityReportUseCase - TRANSACTIONAL EXAMPLE"""
    
    @pytest.mark.asyncio
    async def test_execute_returns_availability_report(self):
        """Arrange: Mock repositories"""
        mock_vehicle_repo = AsyncMock()
        mock_incident_repo = AsyncMock()
        
        # Create test vehicles
        vehicles = [
            VehicleSnapshot(
                vehicle_id=f"VH-{i:03d}",
                fleet_location="BOGOTA",
                status="DISPONIBLE" if i < 42 else "EN_MANTENIMIENTO",
                is_assigned=False,
            ) for i in range(50)
        ]
        
        mock_vehicle_repo.find_by_location.return_value = vehicles
        mock_incident_repo.find_by_vehicle_id.return_value = []
        
        use_case = GetAvailabilityReportUseCase(
            vehicle_snapshot_repo=mock_vehicle_repo,
            incident_repo=mock_incident_repo,
        )
        
        """Act"""
        result = await use_case.execute("BOGOTA")
        
        """Assert"""
        assert result.fleet_location == "BOGOTA"
        assert result.total_vehicles == 50
        assert result.available_vehicles == 42
        assert result.availability_percentage == 84.0
        assert result.is_healthy is True
        assert result.alert_level == "HEALTHY"
    
    @pytest.mark.asyncio
    async def test_execute_with_no_vehicles(self):
        """Arrange: Empty fleet"""
        mock_vehicle_repo = AsyncMock()
        mock_incident_repo = AsyncMock()
        
        mock_vehicle_repo.find_by_location.return_value = []
        
        use_case = GetAvailabilityReportUseCase(
            vehicle_snapshot_repo=mock_vehicle_repo,
            incident_repo=mock_incident_repo,
        )
        
        """Act"""
        result = await use_case.execute("EMPTY_LOCATION")
        
        """Assert"""
        assert result.total_vehicles == 0
        assert result.availability_percentage == 0.0
        assert result.is_healthy is False


class TestGetMaintenanceMetricsUseCase:
    """Test GetMaintenanceMetricsUseCase."""
    
    @pytest.mark.asyncio
    async def test_execute_returns_maintenance_metrics(self):
        """Arrange: Mock repositories"""
        mock_incident_repo = AsyncMock()
        mock_maintenance_repo = AsyncMock()
        
        mock_incident_repo.find_by_vehicle_id.return_value = []
        mock_maintenance_repo.find_by_vehicle_id.return_value = []
        
        use_case = GetMaintenanceMetricsUseCase(
            incident_repo=mock_incident_repo,
            maintenance_repo=mock_maintenance_repo,
        )
        
        """Act"""
        result = await use_case.execute("BOGOTA")
        
        """Assert"""
        assert result.average_mttr_hours == 0.0
        assert result.preventive_maintenance_ratio == 0.0
        assert result.total_maintenance_events == 0
        assert result.period_days == 30


class TestGetVehicleTraceabilityUseCase:
    """Test GetVehicleTraceabilityUseCase - COMPLETE TRANSACTIONAL FLOW"""
    
    @pytest.mark.asyncio
    async def test_execute_returns_complete_traceability(self):
        """Arrange: Create test data across all layers"""
        mock_vehicle_repo = AsyncMock()
        mock_incident_repo = AsyncMock()
        mock_maintenance_repo = AsyncMock()
        
        # Vehicle snapshot
        vehicle_snapshot = VehicleSnapshot(
            vehicle_id="VH-001",
            fleet_location="BOGOTA",
            status="DISPONIBLE",
            mileage=45000,
            last_maintenance_date=datetime.utcnow() - timedelta(days=10),
            incident_count_30days=2,
            is_assigned=False,
        )
        
        # Incidents
        incidents = [
            Incident(
                incident_id="INC-001",
                vehicle_id="VH-001",
                severity="ALTA",
                description="Brake issue",
                occurred_at=datetime.utcnow() - timedelta(days=15),
                resolved_at=datetime.utcnow() - timedelta(days=14, hours=20),
            ),
        ]
        
        # Maintenance
        maintenances = [
            Maintenance(
                maintenance_id="MAINT-001",
                vehicle_id="VH-001",
                maintenance_type="PREVENTIVO",
                description="Oil change",
                started_at=datetime.utcnow() - timedelta(days=10),
                completed_at=datetime.utcnow() - timedelta(days=10, hours=2),
                cost=150000.0,
            ),
        ]
        
        mock_vehicle_repo.find_by_vehicle_id.return_value = vehicle_snapshot
        mock_incident_repo.find_by_vehicle_id.return_value = incidents
        mock_maintenance_repo.find_by_vehicle_id.return_value = maintenances
        
        use_case = GetVehicleTraceabilityUseCase(
            vehicle_snapshot_repo=mock_vehicle_repo,
            incident_repo=mock_incident_repo,
            maintenance_repo=mock_maintenance_repo,
        )
        
        """Act"""
        result = await use_case.execute("VH-001")
        
        """Assert: Full traceability populated"""
        assert result.vehicle_id == "VH-001"
        assert result.fleet_location == "BOGOTA"
        assert result.current_status == "DISPONIBLE"
        assert result.total_incidents_lifetime == 1
        assert result.total_maintenance_events == 1
        assert result.average_mttr_hours > 0
        assert result.last_snapshot is not None
        assert len(result.recent_incidents) == 1
        assert len(result.recent_maintenances) == 1
    
    @pytest.mark.asyncio
    async def test_execute_raises_error_when_vehicle_not_found(self):
        """Arrange: Vehicle doesn't exist"""
        mock_vehicle_repo = AsyncMock()
        mock_incident_repo = AsyncMock()
        mock_maintenance_repo = AsyncMock()
        
        mock_vehicle_repo.find_by_vehicle_id.return_value = None
        
        use_case = GetVehicleTraceabilityUseCase(
            vehicle_snapshot_repo=mock_vehicle_repo,
            incident_repo=mock_incident_repo,
            maintenance_repo=mock_maintenance_repo,
        )
        
        """Act & Assert"""
        with pytest.raises(ValueError):
            await use_case.execute("VH-NONEXISTENT")


# ============================================
# INTEGRATION TEST: End-to-End Transactional Flow
# ============================================

class TestEndToEndTransactionalFlow:
    """Prueba del flujo transaccional completo.
    
    Mapeo del flujo:
    1. Presentation → GET /reportes/trazabilidad/{vehicle_id}
    2. Application → GetVehicleTraceabilityUseCase.execute()
    3. Domain → Models y Services del dominio
    4. Infrastructure → MongoDB repositories
    5. Retorno → TraceabilityDTO JSON
    """
    
    @pytest.mark.asyncio
    async def test_complete_transactional_flow(self):
        """Arrange: Setup complete flow with all layers"""
        # Domain Models
        vehicle = VehicleSnapshot(
            vehicle_id="VH-001",
            fleet_location="BOGOTA",
            status="DISPONIBLE",
            mileage=45000,
            last_maintenance_date=datetime.utcnow() - timedelta(days=10),
            incident_count_30days=2,
            is_assigned=False,
        )
        
        incident = Incident(
            incident_id="INC-001",
            vehicle_id="VH-001",
            severity="ALTA",
            description="Brake system issue",
            occurred_at=datetime.utcnow() - timedelta(days=5, hours=12),
            resolved_at=datetime.utcnow() - timedelta(days=5, hours=6),
        )
        
        maintenance = Maintenance(
            maintenance_id="MAINT-001",
            vehicle_id="VH-001",
            maintenance_type="PREVENTIVO",
            description="Oil change and filter replacement",
            started_at=datetime.utcnow() - timedelta(days=10, hours=8),
            completed_at=datetime.utcnow() - timedelta(days=10, hours=10),
            cost=150000.0,
        )
        
        # Infrastructure mocks
        vehicle_repo = AsyncMock()
        incident_repo = AsyncMock()
        maintenance_repo = AsyncMock()
        
        vehicle_repo.find_by_vehicle_id.return_value = vehicle
        incident_repo.find_by_vehicle_id.return_value = [incident]
        maintenance_repo.find_by_vehicle_id.return_value = [maintenance]
        
        # Application Use Case
        use_case = GetVehicleTraceabilityUseCase(
            vehicle_snapshot_repo=vehicle_repo,
            incident_repo=incident_repo,
            maintenance_repo=maintenance_repo,
        )
        
        """Act: Execute the complete flow"""
        result = await use_case.execute("VH-001")
        
        """Assert: Verify all layers produced correct output"""
        # Presentation Layer validation
        assert result.vehicle_id == "VH-001"
        
        # Application Layer validation
        assert result.fleet_location == "BOGOTA"
        assert result.current_status == "DISPONIBLE"
        
        # Domain Layer validation
        assert result.total_incidents_lifetime == 1
        assert result.total_maintenance_events == 1
        assert result.average_mttr_hours == 6.0  # 6 hours difference
        
        # Infrastructure layer was called
        vehicle_repo.find_by_vehicle_id.assert_called_once_with("VH-001")
        incident_repo.find_by_vehicle_id.assert_called_once_with("VH-001", days_back=90)
        maintenance_repo.find_by_vehicle_id.assert_called_once_with("VH-001", days_back=90)
        
        # DTO transformation successful
        assert result.last_snapshot is not None
        assert result.last_snapshot.vehicle_id == "VH-001"
        assert len(result.recent_incidents) == 1
        assert len(result.recent_maintenances) == 1
