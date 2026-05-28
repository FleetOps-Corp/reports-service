# Gráficas y Estadísticas Microservice

## Descripción

Microservicio encargado de:

- Consumir datos analíticos desde MongoDB Atlas
- Generar gráficas estadísticas (disponibilidad, incidentes, mantenimiento)
- Construir reportes PDF ejecutivos consolidados
- Almacenar reportes en MinIO

## Quick Start

```bash
cp .env.example .env
docker compose up graficas-estadisticas --build
```

## Architecture

- **Domain Layer**: Modelos de reportes, gráficas
- **Application Layer**: Casos de uso para generación
- **Infrastructure Layer**: MongoDB reader, MinIO writer
- **Presentation Layer**: REST API para generar/descargar reportes

## Endpoints

- `POST /estadisticas/reporte-general` - Generar reporte PDF
- `GET /storage/reportes/{id}` - Descargar reporte
- `GET /health` - Health check

Consultar SAD_Document.md para especificación completa.
