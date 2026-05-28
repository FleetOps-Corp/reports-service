"""Infrastructure Layer - MongoDB Connection
Responsabilidad: Gestionar conexión a MongoDB
Patrón: Singleton, Connection Pool
Capa: Infrastructure
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..config import get_settings

logger = logging.getLogger(__name__)

_db_instance: AsyncIOMotorDatabase = None


async def connect_to_mongo() -> AsyncIOMotorDatabase:
    """Establecer conexión a MongoDB."""
    global _db_instance
    
    settings = get_settings()
    
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        _db_instance = client[settings.MONGODB_DATABASE]
        
        # Verify connection
        await client.admin.command('ping')
        logger.info(f"Connected to MongoDB: {settings.MONGODB_DATABASE}")
        
        return _db_instance
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Cerrar conexión a MongoDB."""
    global _db_instance
    
    if _db_instance:
        try:
            _db_instance.client.close()
            logger.info("Closed MongoDB connection")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")


def get_mongodb() -> AsyncIOMotorDatabase:
    """Obtener instancia de MongoDB."""
    return _db_instance
