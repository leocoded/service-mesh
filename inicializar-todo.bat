@echo off
echo 🚀 Inicializando Service Mesh Completo
echo.

echo [1/7] Instalando Istio...
helm repo add istio https://istio-release.storage.googleapis.com/charts > nul 2>&1
helm repo update > nul 2>&1
helm install istio-base istio/base -n istio-system --create-namespace > nul 2>&1
helm install istiod istio/istiod -n istio-system > nul 2>&1
helm install istio-ingress istio/gateway -n istio-system > nul 2>&1
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml > nul 2>&1
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml > nul 2>&1

echo [2/7] Desplegando Kafka (fuera del mesh)...
kubectl apply -f kafka-outside-mesh.yaml

echo [3/7] Desplegando microservicios (dentro del mesh)...
kubectl apply -f istio.yaml

echo [4/7] Esperando que Kafka esté listo...
kubectl wait --for=condition=ready pod -l app=kafka -n event-mesh --timeout=120s

echo [5/7] Esperando que microservicios estén listos...
kubectl wait --for=condition=ready pod -l app=ms-lote -n service-mesh --timeout=120s

echo [6/7] Iniciando port-forwards...
start /B kubectl port-forward -n istio-system svc/kiali 20001:20001
start /B kubectl port-forward -n istio-system svc/grafana 3000:3000
timeout /t 5 /nobreak > nul

echo [7/7] Verificando despliegue...
kubectl get pods -n event-mesh
kubectl get pods -n service-mesh
kubectl get svc -n istio-system | findstr istio-ingress

echo.
echo ✅ Sistema desplegado!
echo.
echo 🌐 URLs disponibles:
echo   - API Gateway:    http://localhost:32680 o http://172.24.0.3
echo   - Kiali:          http://localhost:20001
echo   - Grafana:        http://localhost:3000
echo   - Kafka UI:       http://localhost:30080
echo.
echo 📊 Endpoints API:
echo   - Lotes:          http://localhost:32680/lotes
echo   - Productos:      http://localhost:32680/productos
echo   - Blockchain:     http://localhost:32680/blockchain
echo.
echo 🧪 Ejecuta: test-sistema.bat para probar
echo.
pause