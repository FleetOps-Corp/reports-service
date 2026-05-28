"""Infrastructure Layer - Observability
Responsabilidad: Métricas y monitoring.
Patrón: Sidecar Pattern
Capa: Infrastructure
"""
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps


report_generation_counter = Counter(
    'report_generation_total',
    'Total reports generated',
    ['location', 'status']
)

report_generation_duration = Histogram(
    'report_generation_duration_seconds',
    'Report generation time',
    ['location']
)

pdf_render_time = Histogram(
    'pdf_render_duration_seconds',
    'PDF rendering time',
    ['report_type']
)

chart_generation_counter = Counter(
    'chart_generation_total',
    'Total charts generated',
    ['chart_type']
)

minio_upload_duration = Histogram(
    'minio_upload_duration_seconds',
    'MinIO upload time',
    ['bucket']
)


def track_report_generation(location: str):
    """Decorator para rastrear generación de reportes."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "success"
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                raise
            finally:
                duration = time.time() - start_time
                report_generation_counter.labels(
                    location=location,
                    status=status
                ).inc()
                report_generation_duration.labels(
                    location=location
                ).observe(duration)
        return wrapper
    return decorator


def track_pdf_rendering(report_type: str):
    """Decorator para rastrear renderizado de PDF."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            pdf_render_time.labels(report_type=report_type).observe(duration)
            return result
        return wrapper
    return decorator
