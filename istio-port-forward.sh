#!/bin/bash

NAMESPACE="istio-system"

# Función para iniciar port-forward en background
start_port_forward() {
  local svc=$1
  local local_port=$2
  local remote_port=$3

  echo "▶️ Iniciando port-forward para $svc en http://localhost:$local_port"
  nohup kubectl port-forward -n $NAMESPACE svc/$svc $local_port:$remote_port > $svc.log 2>&1 &
}

# Kiali
start_port_forward kiali 20001 20001

# Grafana
start_port_forward grafana 3000 3000

# Prometheus
start_port_forward prometheus 9090 9090

# Jaeger
start_port_forward jaeger 16686 16686

echo "✅ Todos los port-forwards están corriendo en segundo plano."
echo ""
echo "Accesos disponibles:"
echo "  - Kiali:     http://localhost:20001"
echo "  - Grafana:   http://localhost:3000"
echo "  - Prometheus:http://localhost:9090"
echo "  - Jaeger:    http://localhost:16686"
echo ""
echo "👉 Para detenerlos, ejecuta: pkill -f 'kubectl port-forward'"
