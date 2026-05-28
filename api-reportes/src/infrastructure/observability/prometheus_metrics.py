"""Infrastructure Layer - Observability / Prometheus Metrics
Responsabilidad: Exponer métricas de la aplicación
Capa: Infrastructure
"""
from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps


# Metrics for API endpoints
api_request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['endpoint']
)

# Metrics for use cases
use_case_execution_count = Counter(
    'use_case_executions_total',
    'Total use case executions',
    ['use_case', 'status']
)

use_case_execution_duration = Histogram(
    'use_case_execution_duration_seconds',
    'Use case execution duration',
    ['use_case']
)

# Metrics for external services
grpc_call_count = Counter(
    'grpc_calls_total',
    'Total gRPC calls',
    ['service', 'method', 'status']
)

grpc_call_duration = Histogram(
    'grpc_call_duration_seconds',
    'gRPC call duration',
    ['service']
)

# Metrics for business logic
availability_gauge = Gauge(
    'fleet_availability_percentage',
    'Current fleet availability',
    ['location']
)

mttr_gauge = Gauge(
    'fleet_mttr_hours',
    'Mean Time To Repair',
    ['location']
)


def track_api_request(endpoint: str):
    """Decorator to track API request metrics."""
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
                api_request_count.labels(
                    method="GET",
                    endpoint=endpoint,
                    status=status
                ).inc()
                api_request_duration.labels(endpoint=endpoint).observe(duration)
        return wrapper
    return decorator


def track_use_case(use_case_name: str):
    """Decorator to track use case execution."""
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
                use_case_execution_count.labels(
                    use_case=use_case_name,
                    status=status
                ).inc()
                use_case_execution_duration.labels(
                    use_case=use_case_name
                ).observe(duration)
        return wrapper
    return decorator
