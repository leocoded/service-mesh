@echo off
echo 🌐 Iniciando Port-Forwards...
echo.

echo [1/5] API Gateway en puerto 80...
start "API Gateway" kubectl port-forward -n istio-system svc/istio-gateway 80:80

echo [2/5] Kiali en puerto 20001...
start "Kiali" kubectl port-forward -n istio-system svc/kiali 20001:20001

echo [3/5] Grafana en puerto 3000...
start "Grafana" kubectl port-forward -n istio-system svc/grafana 3000:3000

echo [4/5] Prometheus en puerto 9090...
start "Prometheus" kubectl port-forward -n istio-system svc/prometheus 9090:9090

echo [5/5] Jaeger en puerto 16686...
start "Jaeger" kubectl port-forward -n istio-system svc/tracing 16686:80

echo.
echo ✅ Port-forwards activos!
echo 🌐 API: http://localhost/lotes
echo 📊 Kiali: http://localhost:20001
echo 📈 Grafana: http://localhost:3000
echo 🔍 Prometheus: http://localhost:9090
echo 🔍 Jaeger: http://localhost:16686
echo.
pause