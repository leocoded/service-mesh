@echo off
echo ========================================
echo RECONSTRUYENDO TODAS LAS IMAGENES
echo ========================================

echo.
echo 1. Reconstruyendo imagenes con fix de Kafka...

docker build -t ms-lote:latest ./ms-lote
docker build -t ms-bodega:latest ./ms-bodega
docker build -t ms-producto:latest ./ms-producto
docker build -t ms-analytics:latest ./ms-analytics
docker build -t ms-blockchain:latest ./ms-blockchain

echo.
echo 2. Cargando imagenes a Kind...

docker save ms-lote:latest | docker exec -i desktop-control-plane ctr -n k8s.io images import -
docker save ms-bodega:latest | docker exec -i desktop-control-plane ctr -n k8s.io images import -
docker save ms-producto:latest | docker exec -i desktop-control-plane ctr -n k8s.io images import -
docker save ms-analytics:latest | docker exec -i desktop-control-plane ctr -n k8s.io images import -
docker save ms-blockchain:latest | docker exec -i desktop-control-plane ctr -n k8s.io images import -

echo.
echo 3. Reiniciando deployments...
kubectl rollout restart deployment -n service-mesh

echo.
echo 4. Esperando reinicio completo...
timeout /t 25 /nobreak >nul

echo.
echo 5. Verificando logs de MS-Lote...
kubectl logs -n service-mesh deployment/ms-lote --tail=3

echo.
echo 6. Verificando logs de MS-Blockchain...
kubectl logs -n service-mesh deployment/ms-blockchain --tail=3

echo.
echo 7. PRUEBA FINAL...
curl -X POST "http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-lote:8002/proxy/lotes" ^
  -H "Content-Type: application/json" ^
  -d "{\"fecha_vencimiento\":\"2024-12-31\",\"tipo_almacenamiento\":\"refrigerado\",\"cantidad_inicial\":300,\"id_producto\":\"PROD-ULTIMATE\",\"id_bodega\":\"BODEGA-ULTIMATE\"}"

echo.
echo 8. Esperando procesamiento...
timeout /t 10 /nobreak >nul

echo.
echo 9. RESULTADO FINAL...
curl "http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-blockchain:8007/proxy/trace/all"

echo.
echo ========================================
echo SI TOTAL_RECORDS > 0: EXITO TOTAL
echo ========================================
pause