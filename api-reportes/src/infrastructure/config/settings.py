"""Pydantic Settings for API Reportes
Responsabilidad: Configuración externalized con validación
Patrón: Externalized Configuration
Capa: Infrastructure
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración centralizada para api-reportes."""
    
    APP_NAME: str = "API Reportes"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8001
    
    MONGODB_URL: str = "mongodb+srv://user:password@cluster.mongodb.net"
    MONGODB_DATABASE: str = "reports_db"
    
    GRPC_PORT: int = 50051
    
    PROMETHEUS_PORT: int = 8004
    ENABLE_METRICS: bool = True
    
    SERVICE_NAME: str = "api-reportes"
    SERVICE_INSTANCE_ID: str = "api-reportes-1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """Get settings singleton."""
    return Settings()
