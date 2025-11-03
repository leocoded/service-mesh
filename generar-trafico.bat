@echo off
echo 🚀 Generando tráfico para todos los microservicios...
echo.

echo 📊 Esto ayudará a:
echo   - Activar Kiali (Service Mesh Dashboard)
echo   - Generar métricas en Prometheus/Grafana
echo   - Crear trazas en Jaeger
echo   - Probar conectividad del Gateway
echo.

echo ⏱️ Generando 30 peticiones a cada microservicio...
echo.

for /L %%i in (1,1,30) do (
    echo [%%i/30] Probando todos los microservicios...
    
    REM Productos
    curl -s http://localhost/productos > nul
    
    REM Bodegas  
    curl -s http://localhost/bodegas > nul
    
    REM Lotes
    curl -s http://localhost/lotes > nul
    
    REM Crear lotes para activar Oracle y Blockchain automáticamente
    curl -s -X POST http://localhost/lotes -H "Content-Type: application/json" -d "{\"id_producto\":\"PROD-%%i\",\"id_bodega\":\"BOD-001\",\"cantidad_inicial\":100,\"fecha_vencimiento\":\"2025-12-31\",\"tipo_almacenamiento\":\"refrigerado\",\"temperatura_optima\":5.0}" > nul
    
    REM Analytics (solo health check)
    curl -s http://localhost:8010/ > nul
    
    timeout /t 2 /nobreak > nul
)

echo.
echo ✅ Tráfico generado exitosamente!
echo.
echo 🌐 Ahora puedes verificar en:
echo   - Kiali:      http://localhost:20001 (Graph → service-mesh namespace)
echo   - Grafana:    http://localhost:3000 (Dashboards → Istio)
echo   - Prometheus: http://localhost:9090 (Status → Targets)
echo   - Jaeger:     http://localhost:16686 (Search traces)
echo   - Kafka UI:   http://localhost:8080 (Topics y Brokers)
echo.
echo 💡 Tip: En Kiali, cambia el tiempo a "Last 5m" para ver el tráfico reciente
pause