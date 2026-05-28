#!/bin/bash
# Script para generar reporte de cobertura de tests

set -e

echo "📊 Generando reportes de cobertura..."

SERVICES=("api-reportes" "graficas-estadisticas")

for service in "${SERVICES[@]}"; do
    echo ""
    echo "🔍 Analizando cobertura para $service..."
    
    cd "$service"
    
    # Generate coverage report
    pytest tests/ \
        --cov=src \
        --cov-report=html:coverage_report \
        --cov-report=term \
        --cov-report=xml \
        -q
    
    echo "✅ Reporte de cobertura generado en $service/coverage_report/index.html"
    
    cd ..
done

echo ""
echo "📈 Todos los reportes han sido generados"
