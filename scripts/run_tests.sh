#!/bin/bash
# Script para ejecutar tests con cobertura

cd "$(dirname "$0")/../api-reportes"

echo "🧪 Running unit tests with coverage..."
python -m pytest tests/unit/ \
    -v \
    --cov=src \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-fail-under=80

if [ $? -eq 0 ]; then
    echo "✅ Tests passed!"
    echo "📊 Coverage report: htmlcov/index.html"
else
    echo "❌ Tests failed!"
    exit 1
fi
