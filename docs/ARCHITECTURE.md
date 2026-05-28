"""Architecture Overview
Visión general de la arquitectura del proyecto
"""

# Architecture Overview - Reports Service

## Sistema de Dos Microservicios

### 1. API Reportes (Port 8001)

**Responsabilidades:**

- Agregar datos de múltiples fuentes (gRPC)
- Calcular métricas operativas (Disponibilidad, MTTR)
- Almacenar snapshots en MongoDB
- Exponer APIs REST para consumo

**Stack:**

- FastAPI (REST)
- MongoDB (Persistence)
- gRPC (External communication)
- Prometheus (Metrics)

**Arquitectura:**

- Hexagonal (4 capas)
- Domain-Driven Design
- Repository Pattern
- Service Aggregator Pattern

---

### 2. Gráficas y Estadísticas (Port 8002)

**Responsabilidades:**

- Generar gráficas analíticas
- Crear reportes PDF ejecutivos
- Almacenar reportes en MinIO
- Exponer datos para visualización

**Stack:**

- FastAPI (REST)
- MongoDB (Data source)
- MinIO (PDF storage)
- Prometheus (Metrics)

**Arquitectura:**

- Hexagonal (4 capas)
- Domain-Driven Design
- Builder Pattern
- Adapter Pattern

---

## Flujo de Datos

```
External Services (gRPC)
        ↓
API Reportes (Aggregation + Calculation)
        ↓
MongoDB (Storage)
        ↓
Gráficas y Estadísticas (Analysis + PDF)
        ↓
MinIO (PDF Storage)
        ↓
REST APIs ← Consumer
```

---

## Deployment Architecture

```
Docker Compose
├── api-reportes (Container)
├── graficas-estadisticas (Container)
├── MongoDB Atlas
├── MinIO
└── Prometheus
```

---

## Design Patterns

| Pattern            | Ubicación               | Propósito                         |
| ------------------ | ----------------------- | --------------------------------- |
| Hexagonal          | Ambos servicios         | Separación clara de capas         |
| Repository         | Domain → Infrastructure | Abstracción de persistencia       |
| Adapter            | Infrastructure          | Integración con externos          |
| Service Aggregator | Application             | Consolidación de datos            |
| Builder            | Gráficas (Domain)       | Construcción de reportes          |
| Strategy           | Domain                  | Diferentes estrategias de cálculo |
| Sidecar            | Infrastructure          | Observabilidad (Prometheus)       |
| Circuit Breaker    | Presentation            | Resiliencia ante fallos           |

---

## Security Considerations

- ✅ JWT Auth (implementar en versión 2)
- ✅ gRPC mTLS (implementar en versión 2)
- ✅ Input validation
- ✅ Error handling sin exposición de internals
- ✅ Logging estructurado (JSON)
