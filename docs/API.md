"""REST API Specification
Documentación de todos los endpoints REST del proyecto
"""

# API Reportes - Port 8001

## Disponibilidad

- `GET /reportes/disponibilidad/` - Reporte de disponibilidad de flota
  - Parámetros: location, days
  - Respuesta: KPIResponseDTO

- `GET /reportes/disponibilidad/trend` - Tendencia de disponibilidad

## Mantenimiento

- `GET /reportes/mantenimiento/` - Métricas de mantenimiento
- `GET /reportes/mantenimiento/breakdown` - Desglose preventivo vs correctivo

## Incidentes

- `GET /reportes/incidentes/` - Reporte de incidentes
- `GET /reportes/incidentes/recurrent` - Problemas recurrentes

## Trazabilidad

- `GET /reportes/trazabilidad/vehiculo/{vehicle_id}` - Historial de vehículo
- `GET /reportes/trazabilidad/flota` - Trazabilidad de flota

## Health

- `GET /health` - Health check
- `GET /ready` - Readiness check

---

# Gráficas y Estadísticas - Port 8002

## Reportes

- `POST /estadisticas/reporte-general` - Generar reporte ejecutivo
- `GET /storage/reportes/{id}` - Descargar PDF

## Datos de Análisis

- `GET /datos/disponibilidad` - Datos de disponibilidad
- `GET /datos/incidentes` - Datos de incidentes
- `GET /datos/mantenimientos` - Datos de mantenimiento
- `GET /datos/mttr` - Datos de MTTR

## Observabilidad

- `GET /health` - Health check
- `GET /metrics` - Métricas Prometheus
