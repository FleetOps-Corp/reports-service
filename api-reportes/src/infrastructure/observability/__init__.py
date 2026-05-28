"""Infrastructure Layer - Observability
Responsabilidad: Métrica, logging y monitoring.
Patrón: Sidecar Pattern
Capa: Infrastructure
"""
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps


# Define Prometheus metrics
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

availability_gauge = Gauge(
    'fleet_availability_percentage',
    'Current fleet availability',
    ['location']
)

mttr_gauge = Gauge(
    'mttr_hours',
    'Mean Time To Repair',
    ['location']
)

incident_count = Gauge(
    'incident_count_total',
    'Total incident count',
    ['location']
)


def track_request(method: str, endpoint: str):
    """Decorator para rastrear métricas de requests.
    
    Patrón: Sidecar Pattern
    Responsabilidad: Emitir métricas sin contaminar lógica de negocio
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "success"
            try:
                result = await func(*args, **kwargs)
                status = "success"
                return result
            except Exception as e:
                status = "error"
                raise
            finally:
                duration = time.time() - start_time
                request_count.labels(
                    method=method,
                    endpoint=endpoint,
                    status=status
                ).inc()
                request_duration.labels(
                    method=method,
                    endpoint=endpoint
                ).observe(duration)
        return wrapper
    return decorator


def set_availability_metric(location: str, percentage: float):
    """Actualizar métrica de disponibilidad."""
    availability_gauge.labels(location=location).set(percentage)


def set_mttr_metric(location: str, hours: float):
    """Actualizar métrica MTTR."""
    mttr_gauge.labels(location=location).set(hours)


def set_incident_count_metric(location: str, count: int):
    """Actualizar métrica de incidentes."""
    incident_count.labels(location=location).set(count)
