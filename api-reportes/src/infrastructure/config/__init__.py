"""Infrastructure Layer - Configuration
Responsabilidad: Configuración de la aplicación via variables de entorno.
Patrón: Externalized Configuration
Capa: Infrastructure
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración centralizada usando Pydantic Settings.
    
    Todas las variables se cargan desde .env
    
    Patrón: Externalized Configuration
    """
    
    # Application
    APP_NAME: str = "API Reportes"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8001
    RELOAD: bool = False
    
    # MongoDB
    MONGODB_URL: str = "mongodb+srv://user:password@cluster.mongodb.net"
    MONGODB_DATABASE: str = "reports_analytics"
    
    # gRPC Configuration
    GRPC_VEHICLES_HOST: str = "localhost"
    GRPC_VEHICLES_PORT: int = 50051
    GRPC_INCIDENTS_HOST: str = "localhost"
    GRPC_INCIDENTS_PORT: int = 50052
    GRPC_ASSIGNMENTS_HOST: str = "localhost"
    GRPC_ASSIGNMENTS_PORT: int = 50053
    GRPC_MAINTENANCE_HOST: str = "localhost"
    GRPC_MAINTENANCE_PORT: int = 50054
    
    # Observability
    PROMETHEUS_PORT: int = 8002
    ENABLE_METRICS: bool = True
    
    # Service Discovery (if applicable)
    SERVICE_NAME: str = "api-reportes"
    SERVICE_INSTANCE_ID: str = "api-reportes-1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """Get settings singleton."""
    return Settings()
