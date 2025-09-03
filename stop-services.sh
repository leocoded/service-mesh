#!/bin/bash

# Script para detener todos los microservicios

echo "🛑 Deteniendo todos los microservicios..."

# Leer PIDs y detener procesos
if [ -f "services.pid" ]; then
    while read -r line; do
        if [[ $line =~ ^[0-9]+$ ]]; then
            kill "$line" 2>/dev/null
            echo "   ✓ Proceso $line detenido"
        fi
    done < services.pid
    rm -f services.pid
fi

# Limpiar archivos PID individuales
rm -f *.pid

# Matar cualquier proceso Python que esté usando los puertos del sistema
echo "🧹 Limpiando puertos..."
for port in 8001 8002 8003 8004 8005 8006; do
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
done

echo "✅ Todos los microservicios han sido detenidos"
