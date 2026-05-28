"""Infrastructure - MinIO Configuration
Responsabilidad: Configuración de MinIO
Capa: Infrastructure
"""
from pydantic_settings import BaseSettings


class MinIOConfig(BaseSettings):
    """Configuración de MinIO."""
    
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "reports"
    MINIO_USE_SSL: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True
