"""Infrastructure Layer - MinIO Storage Adapter
Patrón: Adapter Pattern
Capa: Infrastructure
"""
from typing import Optional
from datetime import datetime
from minio import Minio
from minio.error import S3Error
import io


class MinIOStorage:
    """Adaptador para almacenamiento de reportes en MinIO.
    
    Patrón: Adapter (Hexagonal Adapter)
    Responsabilidad: Persistencia de PDFs en objeto storage
    """
    
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str, use_ssl: bool = False):
        """Inicializar cliente MinIO.
        
        Args:
            endpoint: Host:port de MinIO
            access_key: Access key
            secret_key: Secret key
            bucket: Nombre del bucket
            use_ssl: Usar SSL
        """
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=use_ssl
        )
        self.bucket = bucket
        self.endpoint = endpoint
        self.use_ssl = use_ssl
    
    async def store_pdf(self, report_id: str, pdf_data: bytes) -> str:
        """Almacenar PDF en MinIO.
        
        Args:
            report_id: ID del reporte
            pdf_data: Contenido PDF (bytes)
            
        Returns:
            str: URL/path del reporte almacenado
        """
        try:
            # Crear bucket si no existe
            await self._ensure_bucket_exists()
            
            # Preparar objeto
            object_name = f"{report_id}.pdf"
            data_stream = io.BytesIO(pdf_data)
            
            # Subir archivo
            self.client.put_object(
                self.bucket,
                object_name,
                data_stream,
                len(pdf_data),
                content_type="application/pdf"
            )
            
            # Retornar URL
            protocol = "https" if self.use_ssl else "http"
            return f"{protocol}://{self.endpoint}/{self.bucket}/{object_name}"
        
        except S3Error as e:
            raise RuntimeError(f"Failed to store PDF in MinIO: {e}")
    
    async def retrieve_pdf(self, report_id: str) -> bytes:
        """Recuperar PDF desde MinIO.
        
        Args:
            report_id: ID del reporte
            
        Returns:
            bytes: Contenido del PDF
        """
        try:
            object_name = f"{report_id}.pdf"
            response = self.client.get_object(self.bucket, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        
        except S3Error as e:
            raise RuntimeError(f"Failed to retrieve PDF from MinIO: {e}")
    
    async def _ensure_bucket_exists(self):
        """Crear bucket si no existe."""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            raise RuntimeError(f"Failed to check/create bucket: {e}")
