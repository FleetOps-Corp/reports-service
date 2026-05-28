# API Reportes Microservice

## Overview

**API Reportes** es un microservicio de agregación de reportes operacionales diseñado según la arquitectura definida en el SAD (Software Architecture Document). Su responsabilidad es:

- Consumir datos operacionales vía gRPC desde servicios externos (Vehículos, Asignaciones, Incidentes, Mantenimientos)
- Calcular KPIs y métricas operativas (disponibilidad, MTTR, ratios de mantenimiento)
- Persistir snapshots históricos en MongoDB Atlas
- Exponer endpoints REST para consultas de reportes y análisis

## Architecture

### Layers (Hexagonal Architecture)

```
Presentation Layer (REST API)
    ↓
Application Layer (Use Cases)
    ↓
Domain Layer (Business Logic)
    ↓
Infrastructure Layer (MongoDB, gRPC)
```

### Key Design Patterns

- **Hexagonal Architecture**: Puertos y adaptadores para desacoplamiento
- **Repository Pattern**: Abstracción de persistencia
- **DTO Pattern**: Transferencia de datos entre capas
- **Strategy Pattern**: Cálculo flexible de KPIs
- **Aggregator Pattern**: Consolidación de datos distribuidos

## Prerequisites

- Docker 24.0+
- Docker Compose 2.20+
- Python 3.12+ (para desarrollo local sin Docker)
- MongoDB Atlas account (o MongoDB local)

## Quick Start

### With Docker Compose

```bash
# Clone the repository
git clone https://github.com/FleetOps-Corp/reports-service.git
cd reports-service/api-reportes

# Copy environment template
cp .env.example .env

# Configure .env with your MongoDB URL and gRPC service addresses

# Build and start services
docker compose up --build

# Service will be available at http://localhost:8001
# API Documentation: http://localhost:8001/docs
# Metrics: http://localhost:8001/metrics
```

### Local Development (Without Docker)

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Copy and configure .env
cp .env.example .env

# Run application
uvicorn src.presentation.main:app --reload --host 0.0.0.0 --port 8001

# In another terminal, run tests
pytest tests/
```

## Running Tests

### Unit Tests (100% coverage target)

```bash
# Run all unit tests with coverage
pytest tests/unit/ -v --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov\index.html  # Windows
```

### Specific test categories

```bash
# Domain layer tests only
pytest tests/unit/domain/ -v

# Application layer tests only
pytest tests/unit/application/ -v

# End-to-end transactional tests
pytest tests/unit/application/test_use_cases.py::TestEndToEndTransactionalFlow -v
```

### Coverage Requirements

- **Minimum**: 80% overall coverage
- **Target**: 100% coverage on domain and application layers
- **Exclusions**: Infrastructure adapters, presentation routes (mocked in tests)

## API Endpoints

### Reportes

#### Disponibilidad

```
GET /reportes/disponibilidad?sede_id=BOGOTA
Response: AvailabilityReportDTO
```

Calcula disponibilidad de flota: vehículos disponibles / total vehículos

#### Mantenimiento

```
GET /reportes/mantenimiento?sede_id=BOGOTA&dias=30
Response: MaintenanceMetricsDTO
```

Métricas: MTTR promedio, ratio mantenimiento preventivo/correctivo

#### Incidentes Recurrentes

```
GET /reportes/incidentes/recurrentes?dias=30
Response: List[dict]
```

Ranking de vehículos con mayor cantidad de incidentes

#### Trazabilidad (TRANSACTIONAL EXAMPLE)

```
GET /reportes/trazabilidad/{vehicle_id}
Response: TraceabilityDTO
```

Historial 360° completo de un vehículo: snapshots, incidentes, mantenimientos

### Health & Monitoring

```
GET /health
GET /metrics (Prometheus format)
```

## Project Structure

```
api-reportes/
├── src/
│   ├── domain/                    # Domain Layer (DDD)
│   │   ├── models/                # Domain entities
│   │   │   ├── vehicle_snapshot.py
│   │   │   ├── operational_kpi.py
│   │   │   ├── incident.py
│   │   │   └── maintenance.py
│   │   ├── repositories/          # Hexagonal ports (abstractions)
│   │   └── services/              # Domain services (Strategy pattern)
│   │       ├── availability_calculator.py
│   │       ├── mttr_calculator.py
│   │       ├── maintenance_analyzer.py
│   │       └── incident_aggregator.py
│   │
│   ├── application/               # Application Layer (Use Cases)
│   │   ├── dto/                   # Data Transfer Objects
│   │   └── use_cases/             # Application services
│   │       ├── get_availability_report.py
│   │       ├── get_maintenance_metrics.py
│   │       ├── get_recurrent_incidents.py
│   │       └── get_vehicle_traceability.py
│   │
│   ├── infrastructure/            # Infrastructure Layer (Adapters)
│   │   ├── persistence/           # MongoDB adapters
│   │   │   ├── mongodb_connection.py
│   │   │   └── *_repository_impl.py
│   │   ├── grpc_clients/          # gRPC client stubs
│   │   ├── observability/         # Prometheus metrics
│   │   └── config/                # Configuration (Pydantic Settings)
│   │
│   └── presentation/              # Presentation Layer (REST API)
│       ├── main.py                # FastAPI application
│       ├── routes/                # REST endpoints
│       └── middleware/            # Error handling, validation
│
├── tests/
│   └── unit/
│       ├── domain/                # 100% coverage: models, services
│       │   └── test_models_and_services.py
│       ├── application/           # 100% coverage: use cases
│       │   └── test_use_cases.py
│       └── infrastructure/        # Mocked dependencies
│
├── Dockerfile                     # Multi-stage build
├── .dockerignore
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Build config, pytest settings
├── pytest.ini                     # Pytest configuration
├── .env.example                   # Environment template
└── README.md                      # This file
```

## Key Architectural Decisions

| Decision                    | Rationale                                                    |
| --------------------------- | ------------------------------------------------------------ |
| **Microservices**           | Separación de responsabilidades, escalabilidad independiente |
| **gRPC internal**           | Comunicación eficiente y tipada entre servicios              |
| **MongoDB**                 | Queries analíticas complejas, flexibilidad de esquema        |
| **Hexagonal Architecture**  | Desacoplamiento de dominio respecto a infraestructura        |
| **100% unit test coverage** | Confiabilidad de lógica de negocio                           |
| **Docker multi-stage**      | Imágenes optimizadas para producción                         |

## Technology Stack

| Category      | Technology | Version |
| ------------- | ---------- | ------- |
| Language      | Python     | 3.12+   |
| Web Framework | FastAPI    | 0.109+  |
| Async Runtime | Uvicorn    | 0.27+   |
| Database ODM  | Beanie     | 2.0+    |
| Validation    | Pydantic   | 2.5+    |
| Testing       | Pytest     | 7.4+    |
| Monitoring    | Prometheus | 2.48+   |

## Transactional Example: Get Vehicle Traceability

El endpoint `GET /reportes/trazabilidad/{vehicle_id}` es un ejemplo completo de transacción end-to-end:

1. **Presentation Layer**: Recibe `vehicle_id` en URL, valida parámetro
2. **Application Layer**: `GetVehicleTraceabilityUseCase` orquesta el flujo
3. **Domain Layer**:
   - Modelos de dominio (`VehicleSnapshot`, `Incident`, `Maintenance`)
   - Servicios de dominio (`MTTRCalculator` para cálculos)
4. **Infrastructure Layer**: Repositorios MongoDB consultan datos persistidos
5. **Return**: `TraceabilityDTO` con historial completo en JSON

Ver `/src/application/use_cases/__init__.py` para implementación completa.

## Known Limitations & Next Steps

### Current Limitations

- **gRPC client stubs**: Generados pero requieren .proto files de servicios externos
- **Transacciones distribuidas**: Implementar compensating transactions (saga pattern)
- **Caching**: Caché de memoria para KPIs no implementado, considerar Redis
- **Error recovery**: Circuit breaker básico, mejorar con retry policies

### Recommended Next Steps

1. Generar stubs gRPC desde servicios externos: `./scripts/generate_proto.sh`
2. Implementar client aggregators en `src/application/service_aggregators/`
3. Agregar caching distribuido (Redis) para KPIs frecuentes
4. Implementar transacciones distribuidas con saga pattern
5. Observabilidad avanzada: Jaeger distributed tracing
6. Contract testing con Pact para servicios gRPC

## Monitoring & Observability

### Prometheus Metrics

- `api_requests_total`: Total de requests por endpoint
- `api_request_duration_seconds`: Latencia de requests
- `fleet_availability_percentage`: Disponibilidad por sede
- `mttr_hours`: MTTR promedio por ubicación
- `incident_count_total`: Incidentes por ubicación

### Health Check

```bash
curl http://localhost:8001/health
```

### Logs

Configurar `LOG_LEVEL` en `.env`:

- `DEBUG`: Máximo nivel de detalle
- `INFO`: Eventos importantes
- `WARNING`: Advertencias
- `ERROR`: Solo errores

## Contributing

1. Follow the architectural patterns defined in SAD
2. Maintain 100% unit test coverage
3. Use type hints throughout
4. Document domain concepts with docstrings
5. Follow PEP 8 code style

## Support

- Architecture Document: `docs/guidelines/SAD_Document.md`
- Visual Architecture: `docs/guidelines/ReportsDiagram.xml`
- FastAPI Docs: http://localhost:8001/docs (when running)
