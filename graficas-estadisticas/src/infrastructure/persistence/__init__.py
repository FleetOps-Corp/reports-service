"""Infrastructure Layer - MongoDB & MinIO Adapters
Responsabilidad: Persistencia y almacenamiento.
Patrón: Adapter Pattern
Capa: Infrastructure
"""
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from minio import Minio
from minio.commonconfig import REPLACE
import io
import json


class MongoDBAnalyticsRepository:
    """MongoDB adapter para lectura de datos analíticos.
    
    Patrón: Repository (Hexagonal Adapter)
    """
    
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
            doc.pop("_id")
            return doc
        return {}
    
    async def get_availability_metrics(self, location: str) -> List[Dict]:
        """Get availability historical data."""
        collection = self.db["operational_kpis"]
        cursor = collection.find({"fleet_location": location})
        docs = []
        async for doc in cursor:
            doc.pop("_id")
            docs.append(doc)
        return docs
    
    async def get_incident_metrics(self, location: str) -> List[Dict]:
        """Get incident historical data."""
        collection = self.db["incidents"]
        cursor = collection.find({})
        docs = []
        async for doc in cursor:
            doc.pop("_id")
            docs.append(doc)
        return docs
    
    async def get_maintenance_metrics(self, location: str) -> List[Dict]:
        """Get maintenance historical data."""
        collection = self.db["maintenances"]
        cursor = collection.find({})
        docs = []
        async for doc in cursor:
            doc.pop("_id")
            docs.append(doc)
        return docs


class MinIOReportStorage:
    """MinIO adapter para almacenamiento de reportes PDF.
    
    Patrón: Adapter Pattern
    """
    
    def __init__(self, settings):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL,
        )
        self.bucket = settings.MINIO_BUCKET
    
    async def store_report(self, pdf_report) -> str:
        """Store PDF report in MinIO.
        
        Args:
            pdf_report: PDFReport domain model
            
        Returns:
            str: MinIO presigned URL
        """
        # In production, would generate actual PDF bytes
        pdf_bytes = b"%PDF-1.4\n... report content ..."
        
        key = pdf_report.get_minio_key()
        data = io.BytesIO(pdf_bytes)
        
        try:
            # Ensure bucket exists
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
            
            # Upload object
            self.client.put_object(
                self.bucket,
                key,
                data,
                length=len(pdf_bytes),
                content_type="application/pdf",
            )
            
            # Generate presigned URL
            url = self.client.get_presigned_download_url(self.bucket, key)
            return url
        
        except Exception as e:
            raise RuntimeError(f"Failed to store report in MinIO: {e}")
    
    async def get_report(self, report_id: str) -> bytes:
        """Retrieve PDF report from MinIO.
        
        Args:
            report_id: Report identifier
            
        Returns:
            bytes: PDF file content
        """
        try:
            response = self.client.get_object(
                self.bucket,
                f"reports/{report_id}.pdf"
            )
            return response.read()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve report from MinIO: {e}")
