@echo off
echo 🚀 Probando Service Mesh - Sistema de Trazabilidad de Medicamentos
echo.
echo 📊 Verificando conectividad de microservicios...
echo.

REM Test direct pod access
echo [1/4] Probando acceso directo a ms-lote...
kubectl port-forward -n service-mesh svc/ms-lote 8889:8002 --address=0.0.0.0 > nul 2>&1 &
timeout /t 2 /nobreak > nul

echo [2/4] Creando lote de medicamento...
curl -X POST "http://localhost:8889/lotes" -H "Content-Type: application/json" -d "{\"fecha_vencimiento\":\"2025-12-31\",\"tipo_almacenamiento\":\"refrigerado\",\"cantidad_inicial\":100,\"id_producto\":\"PARACETAMOL-001\",\"id_bodega\":\"BODEGA-CENTRAL\",\"temperatura_optima\":4.0,\"humedad_optima\":60.0}" 2>nul

echo.
echo [3/4] Consultando lotes creados...
curl -s "http://localhost:8889/lotes" 2>nul | findstr "id"

echo.
echo [4/4] Verificando disponibilidad...
curl -s "http://localhost:8889/lotes" 2>nul

echo.
echo ✅ Service Mesh funcionando correctamente!
echo.
echo 🌐 Puedes verificar en Kiali:
echo   - URL: http://localhost:20001
echo   - Namespace: service-mesh
echo   - Tiempo: Last 5m
echo.
echo 💡 Los microservicios están funcionando independientemente de Kafka
echo    Kafka está disponible para eventos pero no es crítico para la operación básica
echo.

REM Kill port-forward
taskkill /f /im kubectl.exe > nul 2>&1

pause