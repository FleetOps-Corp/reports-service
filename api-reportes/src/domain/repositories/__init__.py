"""Repository Pattern - Abstract Repositories (Hexagonal Ports)
Definen contratos de persistencia sin dependencias de implementación.
Capa: Domain - Puertos del patrón hexagonal
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from ..models import VehicleSnapshot, OperationalKPI, Incident, Maintenance


class VehicleSnapshotRepository(ABC):
    """Contrato para persistencia de snapshots de vehículos.
    
    Patrón: Repository (Hexagonal Port)
    """
    
    @abstractmethod
    async def save(self, snapshot: VehicleSnapshot) -> str:
        """Guardar un snapshot de vehículo.
        
        Args:
            snapshot: VehicleSnapshot a persistir
            
        Returns:
            str: ID del snapshot guardado
        """
        pass
    
    @abstractmethod
    async def find_by_vehicle_id(self, vehicle_id: str) -> Optional[VehicleSnapshot]:
        """Obtener snapshot más reciente de un vehículo.
        
        Args:
            vehicle_id: Identificador del vehículo
            
        Returns:
            VehicleSnapshot: Snapshot más reciente o None
        """
        pass
    
    @abstractmethod
    async def find_by_location(self, location: str) -> List[VehicleSnapshot]:
        """Obtener todos los snapshots recientes de una ubicación.
        
        Args:
            location: Ubicación/sede
            
        Returns:
            List[VehicleSnapshot]: Snapshots de esa ubicación
        """
        pass


class OperationalKPIRepository(ABC):
    """Contrato para persistencia de KPIs operativos.
    
    Patrón: Repository (Hexagonal Port)
    """
    
    @abstractmethod
    async def save(self, kpi: OperationalKPI) -> str:
        """Guardar un KPI operativo.
        
        Args:
            kpi: OperationalKPI a persistir
            
        Returns:
            str: ID del KPI guardado
        """
        pass
    
    @abstractmethod
    async def find_latest_by_location(self, location: str) -> Optional[OperationalKPI]:
        """Obtener KPI más reciente de una ubicación.
        
        Args:
            location: Ubicación/sede
            
        Returns:
            OperationalKPI: KPI más reciente o None
        """
        pass


class IncidentRepository(ABC):
    """Contrato para persistencia de incidentes históricos.
    
    Patrón: Repository (Hexagonal Port)
    """
    
    @abstractmethod
    async def save(self, incident: Incident) -> str:
        """Guardar un incidente.
        
        Args:
            incident: Incident a persistir
            
        Returns:
            str: ID del incidente guardado
        """
        pass
    
    @abstractmethod
    async def find_by_vehicle_id(self, vehicle_id: str, days_back: int = 30) -> List[Incident]:
        """Obtener incidentes de un vehículo en el período especificado.
        
        Args:
            vehicle_id: Identificador del vehículo
            days_back: Días hacia atrás a consultar
            
        Returns:
            List[Incident]: Incidentes encontrados
        """
        pass


class MaintenanceRepository(ABC):
    """Contrato para persistencia de mantenimientos históricos.
    
    Patrón: Repository (Hexagonal Port)
    """
    
    @abstractmethod
    async def save(self, maintenance: Maintenance) -> str:
        """Guardar un registro de mantenimiento.
        
        Args:
            maintenance: Maintenance a persistir
            
        Returns:
            str: ID del mantenimiento guardado
        """
        pass
    
    @abstractmethod
    async def find_by_vehicle_id(self, vehicle_id: str, days_back: int = 90) -> List[Maintenance]:
        """Obtener mantenimientos de un vehículo en el período especificado.
        
        Args:
            vehicle_id: Identificador del vehículo
            days_back: Días hacia atrás a consultar
            
        Returns:
            List[Maintenance]: Mantenimientos encontrados
        """
        pass
