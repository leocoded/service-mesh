@echo off
echo 🚀 Iniciando Port Forwards Completos...

echo.
echo 📋 DASHBOARDS DE MONITOREO:
echo ▶️ Kiali en http://localhost:20001
start "Kiali" cmd /k "kubectl port-forward -n istio-system svc/kiali 20001:20001"

echo ▶️ Grafana en http://localhost:3000
start "Grafana" cmd /k "kubectl port-forward -n istio-system svc/grafana 3000:3000"

echo ▶️ Prometheus en http://localhost:9090
start "Prometheus" cmd /k "kubectl port-forward -n istio-system svc/prometheus 9090:9090"

echo ▶️ Jaeger en http://localhost:16686
start "Jaeger" cmd /k "kubectl port-forward -n istio-system svc/tracing 16686:80"

echo.
echo 📋 SWAGGER UIs DE MICROSERVICIOS:
echo ▶️ MS-Producto en http://localhost:8003/docs
start "MS-Producto" cmd /k "kubectl port-forward -n service-mesh svc/ms-producto 8003:8003"

echo ▶️ MS-Bodega en http://localhost:8001/docs  
start "MS-Bodega" cmd /k "kubectl port-forward -n service-mesh svc/ms-bodega 8001:8001"

echo ▶️ MS-Lote en http://localhost:8002/docs
start "MS-Lote" cmd /k "kubectl port-forward -n service-mesh svc/ms-lote 8002:8002"

echo ▶️ MS-Orden-Compra en http://localhost:8005/docs
start "MS-Orden-Compra" cmd /k "kubectl port-forward -n service-mesh svc/ms-orden-compra 8005:8005"

echo ▶️ MS-Proveedor en http://localhost:8006/docs
start "MS-Proveedor" cmd /k "kubectl port-forward -n service-mesh svc/ms-proveedor 8006:8006"

echo ▶️ MS-Proyeccion-Demanda en http://localhost:8004/docs
start "MS-Proyeccion-Demanda" cmd /k "kubectl port-forward -n service-mesh svc/ms-proyeccion-demanda 8004:8004"

echo ▶️ MS-Blockchain en http://localhost:8007/docs
start "MS-Blockchain" cmd /k "kubectl port-forward -n service-mesh svc/ms-blockchain 8007:8007"

echo ▶️ MS-Analytics en http://localhost:8010/docs
start "MS-Analytics" cmd /k "kubectl port-forward -n service-mesh svc/ms-analytics 8010:8010"
start "MS-Oracle" cmd /k "kubectl port-forward -n service-mesh svc/ms-oracle 8008:8008"

echo.
echo ✅ Todos los port-forwards iniciados en 12 ventanas separadas
echo.
echo 📋 DASHBOARDS DE MONITOREO:
echo   - Kiali:      http://localhost:20001
echo   - Grafana:    http://localhost:3000
echo   - Prometheus: http://localhost:9090
echo   - Jaeger:     http://localhost:16686
echo.
echo 📋 SWAGGER UIs (Port-Forward):
echo   - MS-Producto:     http://localhost:8003/docs
echo   - MS-Bodega:       http://localhost:8001/docs
echo   - MS-Lote:         http://localhost:8002/docs
echo   - MS-Orden-Compra: http://localhost:8005/docs
echo   - MS-Proveedor:    http://localhost:8006/docs
echo   - MS-Proyeccion:   http://localhost:8004/docs
echo   - MS-Blockchain:   http://localhost:8007/docs
echo   - MS-Analytics:    http://localhost:8010/docs
echo.
echo 🌐 APIs REST (Gateway):
echo   - http://localhost/productos
echo   - http://localhost/bodegas
echo   - http://localhost/lotes
echo   - http://localhost/ordenes
echo   - http://localhost/proveedores
echo   - http://localhost/proyecciones
echo.
echo 💡 Para detener: Cierra las 12 ventanas de cmd
pause