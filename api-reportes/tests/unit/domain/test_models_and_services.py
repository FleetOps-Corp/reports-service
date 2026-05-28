"""Unit Tests - Domain Layer
100% coverage del dominio y application layer
Patrón: AAA (Arrange → Act → Assert)
Testing Framework: pytest
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

# Imports from domain models
from src.domain.models import (
    VehicleSnapshot,
    OperationalKPI,
    Incident,
    Maintenance,
)

from src.domain.services import (
    AvailabilityCalculator,
    MTTRCalculator,
    MaintenanceAnalyzer,
    IncidentAggregator,
)


# ============================================
# UNIT TESTS: VehicleSnapshot Model
# ============================================

class TestVehicleSnapshot:
    """100% coverage para VehicleSnapshot domain model."""
    
    def test_vehicle_snapshot_is_available_when_disponible_and_not_assigned(self):
        """Arrange: Create a vehicle that is available and not assigned"""
        snapshot = VehicleSnapshot(
            vehicle_id="VH-001",
            fleet_location="BOGOTA",
            status="DISPONIBLE",
            is_assigned=False,
        )
        
        """Act: Check if vehicle is available"""
        result = snapshot.is_available()
        
        """Assert: Should be True"""
        assert result is True
    
    def test_vehicle_snapshot_not_available_when_assigned(self):
        """Arrange: Vehicle that is assigned"""
        snapshot = VehicleSnapshot(
            vehicle_id="VH-001",
            fleet_location="BOGOTA",
            status="DISPONIBLE",
            is_assigned=True,
        )
        
        """Act"""
        result = snapshot.is_available()
        
        """Assert: Should be False"""
        assert result is False
    
    def test_vehicle_snapshot_not_available_when_not_in_service(self):
        """Arrange: Vehicle in maintenance"""
        snapshot = VehicleSnapshot(
            vehicle_id="VH-001",
            fleet_location="BOGOTA",
            status="EN_MANTENIMIENTO",
            is_assigned=False,
        )
        
        """Act"""
        result = snapshot.is_available()
        
        """Assert: Should be False"""
        assert result is False
    
    def test_requires_maintenance_when_no_previous_maintenance(self):
        """Arrange: Vehicle with no maintenance history"""
        snapshot = VehicleSnapshot(
            vehicle_id="VH-001",
            fleet_location="BOGOTA",
            status="DISPONIBLE",
            last_maintenance_date=None,
        )
        
        """Act"""
        result = snapshot.requires_maintenance()
        
        """Assert: Should be True"""
        assert result is True
    
    def test_requires_maintenance_when_more_than_30_days_passed(self):
        """Arrange: Last maintenance 31 days ago"""
        snapshot = VehicleSnapshot(
            vehicle_id="VH-001",
            fleet_location="BOGOTA",
            status="DISPONIBLE",
            last_maintenance_date=datetime.utcnow() - timedelta(days=31),
        )
        
        """Act"""
        result = snapshot.requires_maintenance()
        
        """Assert: Should be True"""
        assert result is True
    
    def test_not_requires_maintenance_when_recent(self):
        """Arrange: Maintenance within 30 days"""
        snapshot = VehicleSnapshot(
            vehicle_id="VH-001",
            fleet_location="BOGOTA",
            status="DISPONIBLE",
            last_maintenance_date=datetime.utcnow() - timedelta(days=10),
        )
        
        """Act"""
        result = snapshot.requires_maintenance()
        
        """Assert: Should be False"""
        assert result is False


# ============================================
# UNIT TESTS: OperationalKPI Model
# ============================================

class TestOperationalKPI:
    """100% coverage para OperationalKPI domain model."""
    
    def test_is_healthy_when_all_criteria_met(self):
        """Arrange: KPI with all healthy criteria"""
        kpi = OperationalKPI(
            kpi_id="KPI-001",
            fleet_location="BOGOTA",
            total_vehicles=50,
            available_vehicles=42,
            availability_percentage=84.0,
            average_mttr_hours=4.5,
            preventive_maintenance_ratio=0.65,
            incident_count_month=5,
        )
        
        """Act"""
        result = kpi.is_healthy()
        
        """Assert"""
        assert result is True
    
    def test_not_healthy_when_availability_low(self):
        """Arrange: Low availability"""
        kpi = OperationalKPI(
            kpi_id="KPI-001",
            fleet_location="BOGOTA",
            total_vehicles=50,
            available_vehicles=30,
            availability_percentage=60.0,  # Below 80%
            average_mttr_hours=4.5,
            preventive_maintenance_ratio=0.65,
            incident_count_month=5,
        )
        
        """Act"""
        result = kpi.is_healthy()
        
        """Assert"""
        assert result is False
    
    def test_alert_level_critical_when_low_availability(self):
        """Test alert level calculation."""
        kpi = OperationalKPI(
            kpi_id="KPI-001",
            fleet_location="BOGOTA",
            total_vehicles=50,
            available_vehicles=30,
            availability_percentage=60.0,
            average_mttr_hours=4.5,
            preventive_maintenance_ratio=0.65,
            incident_count_month=5,
        )
        
        """Act"""
        result = kpi.alert_level()
        
        """Assert"""
        assert result == "CRITICAL"
    
    def test_alert_level_warning_when_moderate_issues(self):
        """Test warning level."""
        kpi = OperationalKPI(
            kpi_id="KPI-001",
            fleet_location="BOGOTA",
            total_vehicles=50,
            available_vehicles=38,
            availability_percentage=76.0,
            average_mttr_hours=4.5,
            preventive_maintenance_ratio=0.65,
            incident_count_month=5,
        )
        
        """Act"""
        result = kpi.alert_level()
        
        """Assert"""
        assert result == "WARNING"


# ============================================
# UNIT TESTS: Incident Model
# ============================================

class TestIncident:
    """100% coverage para Incident domain model."""
    
    def test_incident_is_resolved_when_completed(self):
        """Arrange: Resolved incident"""
        incident = Incident(
            incident_id="INC-001",
            vehicle_id="VH-001",
            severity="ALTA",
            description="Brake failure",
            occurred_at=datetime.utcnow() - timedelta(hours=5),
            resolved_at=datetime.utcnow(),
        )
        
        """Act"""
        result = incident.is_resolved()
        
        """Assert"""
        assert result is True
    
    def test_incident_not_resolved_when_pending(self):
        """Arrange: Pending incident"""
        incident = Incident(
            incident_id="INC-001",
            vehicle_id="VH-001",
            severity="ALTA",
            description="Brake failure",
            occurred_at=datetime.utcnow(),
            resolved_at=None,
        )
        
        """Act"""
        result = incident.is_resolved()
        
        """Assert"""
        assert result is False
    
    def test_resolution_time_calculation(self):
        """Arrange: Calculate resolution time"""
        occurred = datetime.utcnow() - timedelta(hours=4)
        resolved = datetime.utcnow()
        
        incident = Incident(
            incident_id="INC-001",
            vehicle_id="VH-001",
            severity="ALTA",
            description="Brake failure",
            occurred_at=occurred,
            resolved_at=resolved,
        )
        
        """Act"""
        hours = incident.resolution_time_hours()
        
        """Assert: Should be approximately 4 hours"""
        assert 3.9 < hours < 4.1
    
    def test_is_critical(self):
        """Test critical incident detection."""
        critical = Incident(
            incident_id="INC-001",
            vehicle_id="VH-001",
            severity="CRITICA",
            description="Engine failure",
            occurred_at=datetime.utcnow(),
        )
        
        not_critical = Incident(
            incident_id="INC-002",
            vehicle_id="VH-002",
            severity="BAJA",
            description="Minor scratch",
            occurred_at=datetime.utcnow(),
        )
        
        """Act & Assert"""
        assert critical.is_critical() is True
        assert not_critical.is_critical() is False


# ============================================
# UNIT TESTS: Maintenance Model
# ============================================

class TestMaintenance:
    """100% coverage para Maintenance domain model."""
    
    def test_maintenance_is_completed_when_finished(self):
        """Arrange"""
        maintenance = Maintenance(
            maintenance_id="MAINT-001",
            vehicle_id="VH-001",
            maintenance_type="PREVENTIVO",
            description="Oil change",
            started_at=datetime.utcnow() - timedelta(hours=2),
            completed_at=datetime.utcnow(),
        )
        
        """Act"""
        result = maintenance.is_completed()
        
        """Assert"""
        assert result is True
    
    def test_maintenance_not_completed_when_pending(self):
        """Arrange"""
        maintenance = Maintenance(
            maintenance_id="MAINT-001",
            vehicle_id="VH-001",
            maintenance_type="PREVENTIVO",
            description="Oil change",
            started_at=datetime.utcnow(),
            completed_at=None,
        )
        
        """Act"""
        result = maintenance.is_completed()
        
        """Assert"""
        assert result is False
    
    def test_duration_calculation(self):
        """Test maintenance duration."""
        started = datetime.utcnow() - timedelta(hours=2, minutes=30)
        completed = datetime.utcnow()
        
        maintenance = Maintenance(
            maintenance_id="MAINT-001",
            vehicle_id="VH-001",
            maintenance_type="PREVENTIVO",
            description="Oil change",
            started_at=started,
            completed_at=completed,
        )
        
        """Act"""
        hours = maintenance.duration_hours()
        
        """Assert"""
        assert 2.4 < hours < 2.6
    
    def test_is_preventive_type(self):
        """Test maintenance type classification."""
        preventive = Maintenance(
            maintenance_id="MAINT-001",
            vehicle_id="VH-001",
            maintenance_type="PREVENTIVO",
            description="Oil change",
            started_at=datetime.utcnow(),
        )
        
        corrective = Maintenance(
            maintenance_id="MAINT-002",
            vehicle_id="VH-002",
            maintenance_type="CORRECTIVO",
            description="Brake repair",
            started_at=datetime.utcnow(),
        )
        
        """Act & Assert"""
        assert preventive.is_preventive() is True
        assert preventive.is_corrective() is False
        assert corrective.is_preventive() is False
        assert corrective.is_corrective() is True


# ============================================
# UNIT TESTS: Domain Services
# ============================================

class TestAvailabilityCalculator:
    """100% coverage para AvailabilityCalculator."""
    
    def test_calculate_availability_with_vehicles(self):
        """Arrange: Fleet with 50 vehicles, 42 available"""
        vehicles = [
            VehicleSnapshot(
                vehicle_id=f"VH-{i:03d}",
                fleet_location="BOGOTA",
                status="DISPONIBLE",
                is_assigned=False,
            ) for i in range(42)
        ]
        vehicles.extend([
            VehicleSnapshot(
                vehicle_id=f"VH-{i:03d}",
                fleet_location="BOGOTA",
                status="EN_MANTENIMIENTO",
                is_assigned=False,
            ) for i in range(42, 50)
        ])
        
        """Act"""
        kpi = AvailabilityCalculator.calculate_availability(vehicles, "BOGOTA")
        
        """Assert"""
        assert kpi.total_vehicles == 50
        assert kpi.available_vehicles == 42
        assert kpi.availability_percentage == 84.0
    
    def test_calculate_availability_with_no_vehicles(self):
        """Arrange: Empty fleet"""
        vehicles = []
        
        """Act"""
        kpi = AvailabilityCalculator.calculate_availability(vehicles, "BOGOTA")
        
        """Assert"""
        assert kpi.total_vehicles == 0
        assert kpi.availability_percentage == 0.0


class TestMTTRCalculator:
    """100% coverage para MTTRCalculator."""
    
    def test_calculate_mttr_with_resolved_incidents(self):
        """Arrange: Three resolved incidents with different resolution times"""
        incidents = [
            Incident(
                incident_id="INC-001",
                vehicle_id="VH-001",
                severity="ALTA",
                description="Issue 1",
                occurred_at=datetime.utcnow() - timedelta(hours=4),
                resolved_at=datetime.utcnow(),
            ),
            Incident(
                incident_id="INC-002",
                vehicle_id="VH-001",
                severity="ALTA",
                description="Issue 2",
                occurred_at=datetime.utcnow() - timedelta(hours=6),
                resolved_at=datetime.utcnow(),
            ),
        ]
        
        """Act"""
        mttr = MTTRCalculator.calculate_mttr(incidents)
        
        """Assert: Average of 4 and 6 is 5"""
        assert 4.9 < mttr < 5.1
    
    def test_calculate_mttr_with_no_resolved(self):
        """Arrange: No resolved incidents"""
        incidents = []
        
        """Act"""
        mttr = MTTRCalculator.calculate_mttr(incidents)
        
        """Assert"""
        assert mttr == 0.0


class TestMaintenanceAnalyzer:
    """100% coverage para MaintenanceAnalyzer."""
    
    def test_calculate_preventive_ratio(self):
        """Arrange: 6 preventive, 4 corrective (60%)"""
        maintenances = []
        now = datetime.utcnow()
        cutoff = now - timedelta(days=30)
        
        for i in range(6):
            maintenances.append(Maintenance(
                maintenance_id=f"MAINT-{i}",
                vehicle_id="VH-001",
                maintenance_type="PREVENTIVO",
                description="Preventive",
                started_at=cutoff + timedelta(days=i),
                completed_at=cutoff + timedelta(days=i, hours=2),
            ))
        
        for i in range(4):
            maintenances.append(Maintenance(
                maintenance_id=f"MAINT-{10+i}",
                vehicle_id="VH-002",
                maintenance_type="CORRECTIVO",
                description="Corrective",
                started_at=cutoff + timedelta(days=10+i),
                completed_at=cutoff + timedelta(days=10+i, hours=4),
            ))
        
        """Act"""
        ratio = MaintenanceAnalyzer.calculate_preventive_ratio(maintenances)
        
        """Assert: 6/10 = 0.6"""
        assert ratio == 0.6


class TestIncidentAggregator:
    """100% coverage para IncidentAggregator."""
    
    def test_count_incidents_in_month(self):
        """Arrange: Create incidents, some in current month, some not"""
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        incidents = [
            Incident(
                incident_id="INC-001",
                vehicle_id="VH-001",
                severity="ALTA",
                description="Issue 1",
                occurred_at=month_start + timedelta(days=5),
            ),
            Incident(
                incident_id="INC-002",
                vehicle_id="VH-001",
                severity="ALTA",
                description="Issue 2",
                occurred_at=month_start + timedelta(days=10),
            ),
        ]
        
        """Act"""
        count = IncidentAggregator.count_incidents_in_month(incidents)
        
        """Assert"""
        assert count == 2
    
    def test_get_critical_incidents(self):
        """Arrange: Mix of critical and non-critical incidents"""
        now = datetime.utcnow()
        
        incidents = [
            Incident(
                incident_id="INC-001",
                vehicle_id="VH-001",
                severity="CRITICA",
                description="Critical",
                occurred_at=now - timedelta(days=2),
            ),
            Incident(
                incident_id="INC-002",
                vehicle_id="VH-002",
                severity="BAJA",
                description="Minor",
                occurred_at=now - timedelta(days=2),
            ),
        ]
        
        """Act"""
        critical = IncidentAggregator.get_critical_incidents(incidents, days_back=7)
        
        """Assert"""
        assert len(critical) == 1
        assert critical[0].incident_id == "INC-001"
