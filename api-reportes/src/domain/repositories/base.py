"""Domain Repository Interfaces - Hexagonal Ports
Responsabilidad: Definir contratos de acceso a datos
Patrón: Repository Pattern, Hexagonal Architecture
Capa: Domain Layer (Port)
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from .models import VehicleSnapshot, OperationalKPI, Incident, Maintenance


class VehicleRepository(ABC):
    """Port: Repositorio para acceso a datos de vehículos."""
    
    @abstractmethod
    async def get_vehicle_snapshot(self, vehicle_id: str) -> Optional[VehicleSnapshot]:
        """Get latest vehicle snapshot."""
        pass
    
    @abstractmethod
    async def get_all_vehicles(self) -> List[VehicleSnapshot]:
        """Get all vehicle snapshots."""
        pass


class KPIRepository(ABC):
    """Port: Repositorio para métricas operativas."""
    
    @abstractmethod
    async def get_kpi(self, location: str, metric: str) -> Optional[OperationalKPI]:
        """Get specific KPI metric."""
        pass
    
    @abstractmethod
    async def get_all_kpis(self, location: str) -> List[OperationalKPI]:
        """Get all KPIs for location."""
        pass
    
    @abstractmethod
    async def save_kpi(self, kpi: OperationalKPI) -> None:
        """Save KPI metric."""
        pass


class SnapshotRepository(ABC):
    """Port: Repositorio para snapshots históricos."""
    
    @abstractmethod
    async def save_snapshot(self, snapshot: VehicleSnapshot) -> None:
        """Save vehicle snapshot."""
        pass
    
    @abstractmethod
    async def get_snapshots(self, vehicle_id: str) -> List[VehicleSnapshot]:
        """Get all snapshots for vehicle."""
        pass


class IncidentRepository(ABC):
    """Port: Repositorio para incidentes."""
    
    @abstractmethod
    async def get_incidents(self, location: str) -> List[Incident]:
        """Get incidents for location."""
        pass
    
    @abstractmethod
    async def save_incident(self, incident: Incident) -> None:
        """Save incident."""
        pass


class MaintenanceRepository(ABC):
    """Port: Repositorio para mantenimientos."""
    
    @abstractmethod
    async def get_maintenances(self, location: str) -> List[Maintenance]:
        """Get maintenance records."""
        pass
    
    @abstractmethod
    async def save_maintenance(self, maintenance: Maintenance) -> None:
        """Save maintenance record."""
        pass
