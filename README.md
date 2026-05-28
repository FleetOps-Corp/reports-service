# FleetOps Reports Service - Root README

## Project Overview

**reports-service** es un sistema de microservicios diseñado para la agregación y generación de reportes operacionales en tiempo real de flotas vehiculares.

Implementa una arquitectura hexagonal con separación clara de responsabilidades:

1. **API Reportes** (Puerto 8001): Agregación de datos operacionales y cálculo de KPIs
2. **Gráficas y Estadísticas** (Puerto 8003): Generación de reportes PDF y gráficas

## Architecture

```
┌─────────────────────────────────────────────┐
│         External Services (gRPC)             │
│  Vehículos │ Incidentes │ Asignaciones      │
│         Mantenimientos                      │
└──────────────┬──────────────────────────────┘
               │
        ┌──────▼──────┐
        │ API Reportes│ (Microservicio 1)
        │ Port: 8001  │
        └──────┬──────┘
               │
      ┌────────▼────────┐
      │  MongoDB Atlas   │
      │ (Persistencia)   │
      └────────┬─────────┘
               │
        ┌──────▼──────┐
        │Gráficas&    │ (Microservicio 2)
        │Estadísticas │
        │ Port: 8003  │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │    MinIO     │
        │   (Storage)  │
        └─────────────┘
```

## Quick Start

### Prerequisites

- Docker 24.0+
- Docker Compose 2.20+

### Start Services

```bash
# Clone repository
git clone https://github.com/FleetOps-Corp/reports-service.git
cd reports-service

# Build and start all services
docker compose up --build

# Services will be available at:
# - API Reportes: http://localhost:8001
# - Gráficas y Estadísticas: http://localhost:8003
# - MongoDB: localhost:27017
# - MinIO: http://localhost:9001 (admin/minioadmin)
# - Prometheus: http://localhost:9090
```

### View Documentation

```bash
# API Reportes OpenAPI docs
open http://localhost:8001/docs

# API Reportes metrics
open http://localhost:8001/metrics
```

## Project Structure

```
reports-service/
├── api-reportes/                          # Microservicio 1
│   ├── src/
│   │   ├── domain/                        # Domain models + services
│   │   ├── application/                   # Use cases + DTOs
│   │   ├── infrastructure/                # MongoDB, gRPC adapters
│   │   └── presentation/                  # REST API, routes
│   ├── tests/
│   │   └── unit/                          # 100% coverage tests
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── README.md
│
├── graficas-estadisticas/                 # Microservicio 2
│   ├── src/
│   │   ├── domain/                        # Report models
│   │   ├── application/                   # Report generation
│   │   ├── infrastructure/                # MongoDB, MinIO
│   │   └── presentation/                  # REST API
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── proto/                                 # gRPC Protocol Buffers
│   ├── vehicle.proto
│   ├── incident.proto
│   └── ...
│
├── docs/
│   ├── guidelines/
│   │   ├── SAD_Document.md                # Architecture specification
│   │   ├── ReportsDiagram.xml             # Visual architecture
│   │   └── prompt.xml                     # Generation prompt
│   └── ...
│
├── scripts/                               # Build & deployment scripts
│   ├── generate_proto.sh
│   ├── run_tests.sh
│   └── generate_coverage.sh
│
├── docker-compose.yml                     # Orchestration
├── .gitignore
└── README.md                              # This file
```

## Development

### Run Tests

```bash
cd api-reportes
pytest tests/ -v --cov=src --cov-report=html

# View coverage
open htmlcov/index.html
```

### Local Development (No Docker)

```bash
# Setup API Reportes
cd api-reportes
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
cp .env.example .env

# Run with local MongoDB
uvicorn src.presentation.main:app --reload
```

## Architecture Documentation

- **SAD (Software Architecture Document)**: `docs/guidelines/SAD_Document.md`
  - Architectural decisions
  - Quality attributes
  - Design patterns
  - Technology stack
  - Microservice contracts

- **Visual Architecture**: `docs/guidelines/ReportsDiagram.xml`
  - Component diagram
  - Data flows
  - Service boundaries

## Key Features

### API Reportes Service

- **Disponibilidad**: Calculate fleet availability KPI
- **Mantenimiento**: Analyze MTTR and preventive/corrective ratio
- **Incidentes**: Detect recurrent incidents by vehicle
- **Trazabilidad**: Complete 360° vehicle history

### Gráficas y Estadísticas Service

- **Generación de Gráficas**: Availability, incidents, maintenance charts
- **Reportes PDF**: Executive reports with consolidated metrics
- **Almacenamiento**: MinIO for report persistence
- **Descarga**: Retrieve historical reports

## Quality Attributes

| Attribute       | Priority | Approach                                 |
| --------------- | -------- | ---------------------------------------- |
| Scalability     | HIGH     | Horizontal scaling, database per service |
| Maintainability | HIGH     | Hexagonal architecture, DDD              |
| Availability    | HIGH     | Health checks, graceful degradation      |
| Observability   | HIGH     | Prometheus metrics, structured logging   |
| Performance     | MEDIUM   | Efficient queries, caching strategy      |

## Technology Stack

| Layer            | Technology    |
| ---------------- | ------------- |
| Language         | Python 3.12   |
| Web Framework    | FastAPI       |
| Database         | MongoDB Atlas |
| Communication    | gRPC          |
| Object Storage   | MinIO         |
| Monitoring       | Prometheus    |
| Containerization | Docker        |
| Testing          | Pytest        |

## API Contracts

### API Reportes Endpoints

```
GET  /reportes/disponibilidad?sede_id=BOGOTA
GET  /reportes/mantenimiento?sede_id=BOGOTA
GET  /reportes/incidentes/recurrentes?dias=30
GET  /reportes/trazabilidad/{vehicle_id}
GET  /health
GET  /metrics
```

### Gráficas y Estadísticas Endpoints

```
POST /estadisticas/reporte-general
GET  /storage/reportes/{report_id}
GET  /health
```

## Monitoring

### Prometheus Metrics

```
http://localhost:9090
```

View key metrics:

- `api_requests_total`: Request counts by endpoint
- `api_request_duration_seconds`: Response latencies
- `fleet_availability_percentage`: Fleet health by location
- `mttr_hours`: Mean Time To Repair

## Operational Considerations

### Health Checks

```bash
# API Reportes
curl http://localhost:8001/health

# Gráficas y Estadísticas
curl http://localhost:8003/health
```

### Database Backup (MongoDB)

```bash
docker exec reports-mongodb mongodump --username admin --password admin123 --out /backup
```

### MinIO Console

```
http://localhost:9001
User: minioadmin
Pass: minioadmin
```

## Troubleshooting

### Services won't start

```bash
# Check logs
docker compose logs -f api-reportes
docker compose logs -f graficas-estadisticas

# Verify network connectivity
docker compose ps
```

### MongoDB connection timeout

- Ensure MongoDB is healthy: `docker compose logs mongodb`
- Check .env configuration in each service

### MinIO bucket issues

- Create bucket via console: http://localhost:9001
- Ensure proper CORS configuration

## Next Steps

1. Generate gRPC stubs: `./scripts/generate_proto.sh`
2. Implement external service clients
3. Deploy to production infrastructure
4. Set up distributed tracing (Jaeger)
5. Configure AlertManager for metrics

## Support

See individual service READMEs:

- `api-reportes/README.md`
- `graficas-estadisticas/README.md`

Architecture reference:

- `docs/guidelines/SAD_Document.md`
