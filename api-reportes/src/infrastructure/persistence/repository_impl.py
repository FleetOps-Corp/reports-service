"""Infrastructure Layer - MongoDB Repository Implementations
Responsabilidad: Implementación de repositorios con MongoDB
Patrón: Adapter Pattern
Capa: Infrastructure
"""
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from ...domain.repositories import VehicleRepository, KPIRepository, SnapshotRepository
from ...domain.models import VehicleSnapshot, OperationalKPI, Incident, Maintenance


class VehicleSnapshotRepositoryImpl(VehicleRepository):
    """Implementación de VehicleRepository con MongoDB."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db["vehicle_snapshots"]
    
    async def get_vehicle_snapshot(self, vehicle_id: str) -> Optional[VehicleSnapshot]:
        """Get latest vehicle snapshot."""
        doc = await self.collection.find_one(
            {"vehicle_id": vehicle_id},
            sort=[("timestamp", -1)]
        )
        if doc:
            return VehicleSnapshot(**doc)
        return None
    
    async def get_all_vehicles(self) -> List[VehicleSnapshot]:
        """Get all vehicle snapshots."""
        cursor = self.collection.find()
        docs = []
        async for doc in cursor:
            docs.append(VehicleSnapshot(**doc))
        return docs


class KPIRepositoryImpl(KPIRepository):
    """Implementación de KPIRepository con MongoDB."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db["operational_kpis"]
    
    async def get_kpi(self, location: str, metric: str) -> Optional[OperationalKPI]:
        """Get specific KPI metric."""
        doc = await self.collection.find_one({
            "fleet_location": location,
            "metric_name": metric
        })
        if doc:
            return OperationalKPI(**doc)
        return None
    
    async def get_all_kpis(self, location: str) -> List[OperationalKPI]:
        """Get all KPIs for location."""
        cursor = self.collection.find({"fleet_location": location})
        docs = []
        async for doc in cursor:
            docs.append(OperationalKPI(**doc))
        return docs
    
    async def save_kpi(self, kpi: OperationalKPI) -> None:
        """Save KPI metric."""
        await self.collection.insert_one(kpi.dict())


class SnapshotRepositoryImpl(SnapshotRepository):
    """Implementación de SnapshotRepository con MongoDB."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db["vehicle_snapshots"]
    
    async def save_snapshot(self, snapshot: VehicleSnapshot) -> None:
        """Save vehicle snapshot."""
        await self.collection.insert_one(snapshot.dict())
    
    async def get_snapshots(self, vehicle_id: str) -> List[VehicleSnapshot]:
        """Get all snapshots for vehicle."""
        cursor = self.collection.find({"vehicle_id": vehicle_id})
        docs = []
        async for doc in cursor:
            docs.append(VehicleSnapshot(**doc))
        return docs
