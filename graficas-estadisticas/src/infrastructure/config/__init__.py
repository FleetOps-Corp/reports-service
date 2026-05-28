"""Infrastructure Layer - Configuration
Responsabilidad: Configuración externalized.
Patrón: Externalized Configuration
Capa: Infrastructure
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración centralizada."""
    
    APP_NAME: str = "Gráficas y Estadísticas"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8002
    
    MONGODB_URL: str = "mongodb+srv://user:password@cluster.mongodb.net"
    MONGODB_DATABASE: str = "reports_analytics"
    
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "reports"
    MINIO_USE_SSL: bool = False
    
    PROMETHEUS_PORT: int = 8003
    ENABLE_METRICS: bool = True
    
    SERVICE_NAME: str = "graficas-estadisticas"
    SERVICE_INSTANCE_ID: str = "graficas-estadisticas-1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """Get settings singleton."""
    return Settings()
