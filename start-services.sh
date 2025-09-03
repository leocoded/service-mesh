#!/bin/bash

# Script para ejecutar todos los microservicios del sistema

echo "🚀 Iniciando todos los microservicios..."

# Función para ejecutar un microservicio en background
run_service() {
    local service_name=$1
    local port=$2
    local path=$3
    
    echo "📦 Iniciando $service_name en puerto $port..."
    cd "$path" && python main.py &
    echo "$!" > "${service_name}.pid"
    cd ..
}

# Crear archivo para almacenar PIDs
echo "# PIDs de microservicios" > services.pid

# Ejecutar cada microservicio
run_service "MS-Bodega" 8001 "ms-bodega"
run_service "MS-Lote" 8002 "ms-lote" 
run_service "MS-Producto" 8003 "ms-producto"
run_service "MS-ProyeccionDemanda" 8004 "ms-proyeccion-demanda"
run_service "MS-OrdenCompra" 8005 "ms-orden-compra"
run_service "MS-Proveedor" 8006 "ms-proveedor"

echo ""
echo "✅ Todos los microservicios han sido iniciados"
echo ""
echo "📋 URLs de documentación:"
echo "   MS-Bodega:            http://localhost:8001/docs"
echo "   MS-Lote:              http://localhost:8002/docs"
echo "   MS-Producto:          http://localhost:8003/docs"
echo "   MS-ProyeccionDemanda: http://localhost:8004/docs"
echo "   MS-OrdenCompra:       http://localhost:8005/docs"
echo "   MS-Proveedor:         http://localhost:8006/docs"
echo ""
echo "🛑 Para detener todos los servicios, ejecuta: ./stop-services.sh"
echo ""

# Esperar a que el usuario presione Ctrl+C
trap 'echo ""; echo "🛑 Deteniendo servicios..."; kill $(cat *.pid) 2>/dev/null; rm -f *.pid; exit' INT

echo "⏳ Servicios ejecutándose... Presiona Ctrl+C para detener"
wait
