"""Infrastructure Layer - MongoDB Persistence Adapters
Responsabilidad: Implementar repositorios usando MongoDB.
Patrón: Repository Pattern + Adapter Pattern
Capa: Infrastructure
"""
from typing import Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..config import Settings


class MongoDBConnection:
    """Adapter para conexión a MongoDB.
    
    Patrón: Adapter Pattern para driver MongoDB
    Responsabilidad: Gestionar ciclo de vida de conexión
    """
    
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect(cls, settings: Settings):
        """Establish connection to MongoDB."""
        cls._client = AsyncIOMotorClient(settings.MONGODB_URL)
        cls._db = cls._client[settings.MONGODB_DATABASE]
        
        # Verify connection
        await cls._db.command("ping")
        print("✅ Connected to MongoDB Atlas")
    
    @classmethod
    async def disconnect(cls):
        """Close MongoDB connection."""
        if cls._client:
            cls._client.close()
            print("✅ Disconnected from MongoDB")
    
    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if cls._db is None:
            raise RuntimeError("Database not initialized. Call connect() first.")
        return cls._db


class VehicleSnapshotRepositoryMongoDB:
    """Implementación MongoDB del repositorio de snapshots.
    
    Patrón: Repository (Hexagonal Adapter)
    Implementa: VehicleSnapshotRepository
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["vehicle_snapshots"]
    
    async def save(self, snapshot) -> str:
        """Persistir snapshot en MongoDB."""
        result = await self.collection.insert_one(snapshot.dict())
        return str(result.inserted_id)
    
    async def find_by_vehicle_id(self, vehicle_id: str):
        """Obtener snapshot más reciente de un vehículo."""
        from ...domain.models import VehicleSnapshot
        doc = await self.collection.find_one(
            {"vehicle_id": vehicle_id},
            sort=[("captured_at", -1)]
        )
        if doc:
            doc.pop("_id")
            return VehicleSnapshot(**doc)
        return None
    
    async def find_by_location(self, location: str) -> List:
        """Obtener todos los snapshots de una ubicación."""
        from ...domain.models import VehicleSnapshot
        cursor = self.collection.find({"fleet_location": location})
        snapshots = []
        async for doc in cursor:
            doc.pop("_id")
            snapshots.append(VehicleSnapshot(**doc))
        return snapshots


class OperationalKPIRepositoryMongoDB:
    """Implementación MongoDB del repositorio de KPIs.
    
    Patrón: Repository (Hexagonal Adapter)
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["operational_kpis"]
    
    async def save(self, kpi) -> str:
        """Persistir KPI en MongoDB."""
        result = await self.collection.insert_one(kpi.dict())
        return str(result.inserted_id)
    
    async def find_latest_by_location(self, location: str):
        """Obtener KPI más reciente de una ubicación."""
        from ...domain.models import OperationalKPI
        doc = await self.collection.find_one(
            {"fleet_location": location},
            sort=[("calculated_at", -1)]
        )
        if doc:
            doc.pop("_id")
            return OperationalKPI(**doc)
        return None


class IncidentRepositoryMongoDB:
    """Implementación MongoDB del repositorio de incidentes.
    
    Patrón: Repository (Hexagonal Adapter)
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["incidents"]
    
    async def save(self, incident) -> str:
        """Persistir incidente en MongoDB."""
        result = await self.collection.insert_one(incident.dict())
        return str(result.inserted_id)
    
    async def find_by_vehicle_id(self, vehicle_id: str, days_back: int = 30) -> List:
        """Obtener incidentes de un vehículo."""
        from ...domain.models import Incident
        from datetime import datetime, timedelta
        
        cutoff = datetime.utcnow() - timedelta(days=days_back)
        cursor = self.collection.find({
            "vehicle_id": vehicle_id,
            "occurred_at": {"$gte": cutoff}
        })
        
        incidents = []
        async for doc in cursor:
            doc.pop("_id")
            incidents.append(Incident(**doc))
        return incidents


class MaintenanceRepositoryMongoDB:
    """Implementación MongoDB del repositorio de mantenimientos.
    
    Patrón: Repository (Hexagonal Adapter)
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["maintenances"]
    
    async def save(self, maintenance) -> str:
        """Persistir mantenimiento en MongoDB."""
        result = await self.collection.insert_one(maintenance.dict())
        return str(result.inserted_id)
    
    async def find_by_vehicle_id(self, vehicle_id: str, days_back: int = 90) -> List:
        """Obtener mantenimientos de un vehículo."""
        from ...domain.models import Maintenance
        from datetime import datetime, timedelta
        
        cutoff = datetime.utcnow() - timedelta(days=days_back)
        cursor = self.collection.find({
            "vehicle_id": vehicle_id,
            "started_at": {"$gte": cutoff}
        })
        
        maintenances = []
        async for doc in cursor:
            doc.pop("_id")
            maintenances.append(Maintenance(**doc))
        return maintenances
