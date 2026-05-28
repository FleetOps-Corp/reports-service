"""Infrastructure - MongoDB Analytics Repository
Responsabilidad: Lectura de datos analíticos desde MongoDB
Patrón: Repository (Adapter)
Capa: Infrastructure
"""
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase


class MongoDBAnalyticsRepository:
    """MongoDB adapter para lectura de datos analíticos."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def get_kpis(self, location: str, months_back: int = 1) -> Dict:
        """Get KPI metrics for location."""
        collection = self.db["operational_kpis"]
        doc = await collection.find_one(
            {"fleet_location": location},
            sort=[("calculated_at", -1)]
        )
        if doc:
            doc.pop("_id", None)
            return doc
        return {}
    
    async def get_availability_metrics(self, location: str) -> List[Dict]:
        """Get availability historical data."""
        collection = self.db["operational_kpis"]
        cursor = collection.find({"fleet_location": location})
        docs = []
        async for doc in cursor:
            doc.pop("_id", None)
            docs.append(doc)
        return docs
    
    async def get_incident_metrics(self, location: str) -> List[Dict]:
        """Get incident historical data."""
        collection = self.db["incidents"]
        cursor = collection.find({})
        docs = []
        async for doc in cursor:
            doc.pop("_id", None)
            docs.append(doc)
        return docs
    
    async def get_maintenance_metrics(self, location: str) -> List[Dict]:
        """Get maintenance historical data."""
        collection = self.db["maintenances"]
        cursor = collection.find({})
        docs = []
        async for doc in cursor:
            doc.pop("_id", None)
            docs.append(doc)
        return docs
