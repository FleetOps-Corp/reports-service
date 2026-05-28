# Software Architecture Document (SAD)
## FleetCorp S.A. — Analytical Platform

---

# 1. Architectural Decisions

| ID | Decision | Rationale |
|---|---|---|
| AD-01 | Use a microservices architecture divided into `API Reportes` and `Gráficas y Estadísticas`. | Separation of responsibilities, scalability and maintainability. |
| AD-02 | Use gRPC for internal communication. | Efficient and strongly-typed service-to-service communication. |
| AD-03 | Use MongoDB Atlas as the analytical persistence layer. | Flexible schema design and efficient historical aggregation queries. |
| AD-04 | Use MinIO for document storage. | Centralized object storage for generated executive reports. |
| AD-05 | Keep API Gateway external to the project scope. | Responsibility isolation and centralized authentication management. |
| AD-06 | Apply Database per Service principles. | Service decoupling and independent persistence management. |

---

# 2. Quality Attributes

| Attribute | Priority | Goal |
|---|---|---|
| Scalability | High | Independent horizontal scaling of services. |
| Maintainability | High | Modular and decoupled architecture. |
| Availability | High | Tolerance to partial service failures. |
| Traceability | High | Historical operational visibility. |
| Observability | High | Real-time monitoring and diagnostics. |
| Performance | Medium | Efficient KPI aggregation and reporting. |
| Extensibility | Medium | Easy addition of new reports and KPIs. |

---

# 3. Design Patterns and Architectural Styles

| Pattern / Style | Purpose |
|---|---|
| Microservices Architecture | Independent analytical services. |
| Aggregator Pattern | Consolidate distributed operational data. |
| API Composition Pattern | Build complex analytical responses. |
| Repository Pattern | Decouple persistence access logic. |
| DTO Pattern | Standardize inter-service data transfer. |
| Adapter Pattern | Normalize external service responses. |
| Builder Pattern | Construct consolidated PDF reports. |
| Strategy Pattern | Support multiple KPI calculation strategies. |
| Circuit Breaker Pattern | Prevent cascading service failures. |
| Sidecar Pattern | Externalize observability tooling. |
| Database per Service | Isolate analytical persistence responsibilities. |

---

# 4. Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| Backend Framework | FastAPI |
| Internal Communication | gRPC |
| Database | MongoDB Atlas |
| ODM | Beanie ODM |
| Validation | Pydantic v2 |
| Statistical Processing | Pandas |
| PDF Generation | ReportLab / WeasyPrint |
| Templates | Jinja2 |
| Object Storage | MinIO |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Logging | Loki |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Testing | Pytest |

---

# 5. Microservice Responsibilities

| Microservice | Responsibilities |
|---|---|
| API Reportes | Consume operational data via gRPC, aggregate information, calculate KPIs, consolidate traceability, and store analytical snapshots in MongoDB Atlas. |
| Gráficas y Estadísticas | Consume analytical data from MongoDB Atlas, generate statistics and graphs, build a consolidated executive PDF report, and store reports in MinIO. |

---

# 6. Persistence and Storage Strategy

| Technology | Stored Data |
|---|---|
| MongoDB Atlas | Vehicle snapshots, incident history, maintenance history, assignments, operational KPIs, analytical metrics and traceability data. |
| MinIO | Executive PDF reports, historical reports and embedded analytical visual resources. |

---

# 7. Observability and Monitoring

| Component | Responsibility |
|---|---|
| Prometheus | Metrics collection |
| Grafana | Dashboard visualization |
| Loki | Centralized logging |

Monitored metrics:
- response latency
- gRPC failures
- PDF generation time
- database performance
- report generation throughput

---

# 8. Architectural Constraints

- API Gateway is external to the project scope.
- Internal communication must use gRPC.
- MongoDB Atlas is the analytical persistence layer.
- MinIO is exclusively used for report storage.
- Services must remain decoupled.
- Observability is mandatory across all services.


# 9 Interfaces y Contratos de Integración
## 9.1. Microservicio: API Reportes

| Tipo            | Endpoint / Operación                      | Protocolo     | Consumido desde              | Entrada Principal                     | Procesamiento / Responsabilidad                      | Salida                              |
| --------------- | ----------------------------------------- | ------------- | ---------------------------- | ------------------------------------- | ---------------------------------------------------- | ----------------------------------- |
| Consumo Externo | `/vehiculos`                              | gRPC          | Microservicio Vehículos      | `sede_id`, filtros operativos         | Obtener estado y censo de vehículos                  | Dataset operacional de vehículos    |
| Consumo Externo | `/asignaciones`                           | gRPC          | Microservicio Asignaciones   | `vehicle_id`, estado asignación       | Identificar vehículos actualmente asignados          | Dataset de asignaciones activas     |
| Consumo Externo | `/incidentes`                             | gRPC          | Microservicio Incidentes     | `vehicle_id`, severidad, rango fechas | Consolidar recurrencia y criticidad                  | Dataset histórico de incidentes     |
| Consumo Externo | `/mantenimientos`                         | gRPC          | Microservicio Mantenimientos | `vehicle_id`, tipo mantenimiento      | Diferenciar mantenimientos preventivos y correctivos | Dataset histórico de mantenimientos |
| Endpoint Propio | `GET /reportes/disponibilidad`            | REST          | Interno                      | `sede_id` opcional                    | Calcular disponibilidad global y por sede            | KPI de disponibilidad               |
| Endpoint Propio | `GET /reportes/mantenimiento`             | REST          | Interno                      | filtros temporales                    | Calcular MTTR y relación preventivo/correctivo       | Métricas operativas                 |
| Endpoint Propio | `GET /reportes/incidentes/recurrentes`    | REST          | Interno                      | filtros de recurrencia                | Detectar vehículos con mayor cantidad de incidentes  | Ranking de recurrencia              |
| Endpoint Propio | `GET /reportes/trazabilidad/{vehicle_id}` | REST          | Interno                      | `vehicle_id`                          | Consolidar historial completo del vehículo           | Trazabilidad 360°                   |
| Persistencia    | `vehiculos_snapshot`                      | MongoDB Atlas | Interno                      | snapshots operacionales               | Persistir histórico operativo                        | Históricos analíticos               |
| Persistencia    | `metricas_operativas`                     | MongoDB Atlas | Interno                      | KPIs calculados                       | Persistir métricas analíticas                        | KPIs históricos                     |
| Observabilidad  | `/metrics`                                | HTTP          | Prometheus                   | métricas runtime                      | Exponer observabilidad del servicio                  | Métricas Prometheus                 |


## 9.1. Microservicio: Gráficas y Estadísticas

| Tipo                  | Endpoint / Operación                 | Protocolo | Consumido desde              | Entrada Principal           | Procesamiento / Responsabilidad                  | Salida                |
| --------------------- | ------------------------------------ | --------- | ---------------------------- | --------------------------- | ------------------------------------------------ | --------------------- |
| Consulta Interna      | `/datos/disponibilidad`              | REST      | API Reportes + MongoDB Atlas | métricas históricas         | Obtener disponibilidad consolidada               | Dataset analítico     |
| Consulta Interna      | `/datos/incidentes`                  | REST      | API Reportes + MongoDB Atlas | incidentes históricos       | Obtener recurrencia y severidad                  | Dataset estadístico   |
| Consulta Interna      | `/datos/mantenimientos`              | REST      | API Reportes + MongoDB Atlas | mantenimientos históricos   | Obtener mantenimientos preventivos/correctivos   | Dataset operativo     |
| Consulta Interna      | `/datos/mttr`                        | REST      | API Reportes + MongoDB Atlas | tiempos históricos          | Obtener evolución MTTR                           | Dataset temporal      |
| Procesamiento Interno | Generación gráficas disponibilidad   | Interno   | MongoDB Atlas                | KPIs históricos             | Construir visualizaciones operativas             | Gráficas analíticas   |
| Procesamiento Interno | Generación gráficas incidentes       | Interno   | MongoDB Atlas                | recurrencia y severidad     | Construir análisis visual de fallas              | Gráficas comparativas |
| Procesamiento Interno | Generación gráficas mantenimiento    | Interno   | MongoDB Atlas                | mantenimientos históricos   | Comparar preventivos vs correctivos              | Indicadores visuales  |
| Procesamiento Interno | Generación gráficas MTTR             | Interno   | MongoDB Atlas                | tiempos promedio reparación | Construir evolución histórica MTTR               | Gráficas temporales   |
| Endpoint Propio       | `POST /estadisticas/reporte-general` | REST      | MongoDB Atlas                | parámetros de reporte       | Consolidar KPIs, gráficas y métricas             | PDF ejecutivo         |
| Almacenamiento        | `POST /storage/minio`                | MinIO SDK | MinIO                        | PDF consolidado             | Persistir documento ejecutivo                    | URL / metadata        |
| Consulta Interna      | `GET /storage/reportes/{id}`         | REST      | MinIO                        | `report_id`                 | Recuperar reporte histórico                      | Documento PDF         |
| Observabilidad        | `/metrics`                           | HTTP      | Prometheus                   | métricas runtime            | Exponer métricas de renderizado y almacenamiento | Métricas Prometheus   |
