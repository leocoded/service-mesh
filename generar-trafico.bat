@echo off
echo 🚀 Generando tráfico para todos los microservicios...
echo.

echo 📊 Esto ayudará a:
echo   - Activar Kiali (Service Mesh Dashboard)
echo   - Generar métricas en Prometheus/Grafana
echo   - Crear trazas en Jaeger
echo   - Probar conectividad del Gateway
echo   - Activar Event-Mesh (Kafka)
echo   - Registrar transacciones en Blockchain
echo   - Generar trazabilidad completa
echo.

echo ⏱️ Generando 30 peticiones a cada microservicio...
echo.

for /L %%i in (1,1,30) do (
    echo [%%i/30] Probando todos los microservicios...
    
    REM Health checks para generar tráfico básico
    curl -s http://localhost:32680/productos > nul
    curl -s http://localhost:32680/bodegas > nul
    curl -s http://localhost:32680/lotes > nul
    curl -s http://localhost:32680/blockchain > nul
    
    REM Crear producto (activa blockchain automáticamente)
    curl -s -X POST http://localhost:32680/productos -H "Content-Type: application/json" -d "{\"nombre\":\"Medicamento-%%i\",\"descripcion\":\"Producto de prueba %%i\",\"categoria\":\"medicamento\",\"unidad_medida\":\"unidad\",\"precio_unitario\":50.0,\"codigo_barras\":\"BAR%%i\",\"concentracion\":\"500mg\",\"principio_activo\":\"Paracetamol\",\"laboratorio\":\"Lab%%i\",\"requiere_refrigeracion\":true,\"vida_util_dias\":365}" > nul
    
    REM Crear lote (activa blockchain automáticamente)
    curl -s -X POST http://localhost:32680/lotes -H "Content-Type: application/json" -d "{\"id_producto\":\"PROD-%%i\",\"id_bodega\":\"BOD-001\",\"cantidad_inicial\":100,\"fecha_vencimiento\":\"2025-12-31\",\"tipo_almacenamiento\":\"refrigerado\",\"temperatura_optima\":5.0}" > nul
    
    REM Reservar stock en bodega (activa blockchain)
    curl -s -X PATCH http://localhost:32680/bodegas/BOD-001/reservar/10 > nul
    
    REM Ingresar lote a bodega (caso de negocio - activa blockchain)
    curl -s -X POST http://localhost:32680/bodegas/BOD-001/lotes/LOTE-%%i/ingresar -H "Content-Type: application/json" -d "{\"cantidad\":50}" > nul
    
    REM Verificar trazabilidad en blockchain
    curl -s http://localhost:32680/blockchain/trace/all > nul
    
    REM Analytics y otros servicios
    curl -s http://localhost:8010/ > nul
    
    timeout /t 1 /nobreak > nul
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
echo   - Blockchain: http://localhost:32680/blockchain/trace/all
echo.
echo 💡 Tips:
echo   - En Kiali, cambia el tiempo a "Last 5m" para ver el tráfico reciente
echo   - Verifica que el namespace sea "service-mesh"
echo   - Los eventos Kafka deberían aparecer en los topics:
echo     * inventory.lote.created
echo     * warehouse.stock.reserved
echo     * warehouse.lote.ingresado
echo     * catalog.producto.created
pause