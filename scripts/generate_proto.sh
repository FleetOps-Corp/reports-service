#!/bin/bash
# Script para generar stubs gRPC desde archivos .proto

set -e

echo "🔧 Generando stubs gRPC desde archivos .proto..."

# Instalar herramientas si no existen
if ! command -v protoc &> /dev/null; then
    echo "❌ protoc no está instalado. Instálalo con: apt-get install protobuf-compiler"
    exit 1
fi

# Directorio de proto files
PROTO_DIR="proto"
OUTPUT_DIR_API="api-reportes/src/infrastructure/grpc_clients/generated"
OUTPUT_DIR_GFX="graficas-estadisticas/src/infrastructure/grpc_clients/generated"

# Crear directorios de salida
mkdir -p "$OUTPUT_DIR_API"
mkdir -p "$OUTPUT_DIR_GFX"

# Generar para API Reportes
echo "📝 Generando stubs para api-reportes..."
python -m grpc_tools.protoc \
    -I"$PROTO_DIR" \
    --python_out="$OUTPUT_DIR_API" \
    --pyi_out="$OUTPUT_DIR_API" \
    --grpc_python_out="$OUTPUT_DIR_API" \
    "$PROTO_DIR"/*.proto

# Generar para Gráficas
echo "📝 Generando stubs para graficas-estadisticas..."
python -m grpc_tools.protoc \
    -I"$PROTO_DIR" \
    --python_out="$OUTPUT_DIR_GFX" \
    --pyi_out="$OUTPUT_DIR_GFX" \
    --grpc_python_out="$OUTPUT_DIR_GFX" \
    "$PROTO_DIR"/*.proto

echo "✅ Stubs gRPC generados exitosamente"
