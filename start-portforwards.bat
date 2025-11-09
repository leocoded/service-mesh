@echo off
echo 🌐 Iniciando Port Forwards para Service Mesh
echo.

echo Iniciando port forwards en segundo plano...
start /B kubectl port-forward -n istio-system svc/kiali 20001:20001
start /B kubectl port-forward -n istio-system svc/grafana 3000:3000
start /B kubectl port-forward -n istio-system svc/tracing 16686:80
start /B kubectl port-forward -n event-mesh svc/kafka-ui 30080:8080

echo.
echo ✅ Port forwards iniciados!
echo.
echo 🌐 URLs disponibles:
echo   - API Gateway:    http://localhost:32680
echo   - Kiali:          http://localhost:20001
echo   - Kafka UI:       http://localhost:30080
echo   - Grafana:        http://localhost:3000
echo   - Jaeger:         http://localhost:16686
echo.
echo 📊 Endpoints API:
echo   - Lotes:          http://localhost:32680/lotes
echo   - Productos:      http://localhost:32680/productos
echo   - Blockchain:     http://localhost:32680/blockchain
echo.
pause