@echo off
echo 🚀 Despliegue Completo Service Mesh
echo.

echo [1/8] Iniciando Kafka...
docker-compose -f docker-compose-kafka.yml up -d

echo [2/8] Instalando Istio...
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
helm install istio-base istio/base -n istio-system --create-namespace
helm install istiod istio/istiod -n istio-system --wait

echo [3/8] Instalando Istio Gateway...
helm install istio-gateway istio/gateway -n istio-system

echo [4/8] Instalando addons de observabilidad...
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml

echo [5/8] Creando namespace service-mesh...
kubectl create namespace service-mesh
kubectl label namespace service-mesh istio-injection=enabled

echo [6/8] Aplicando configuración blockchain...
kubectl apply -f blockchain-config.yaml

echo [7/8] Aplicando configuración kafka-mesh...
kubectl apply -f kafka-mesh-enterprise.yaml

echo [8/8] Aplicando microservicios...
kubectl apply -f istio-kafka-bypass.yaml

echo [9/9] Corrigiendo selector del Gateway...
kubectl patch gateway api-gateway -n service-mesh --type=merge -p="{\"spec\":{\"selector\":{\"app\":\"istio-gateway\"}}}"

echo [10/10] Esperando que los pods estén listos...
kubectl wait --for=condition=ready pod -l app=istio-gateway -n istio-system --timeout=300s
kubectl wait --for=condition=ready pod -l app=ms-lote -n service-mesh --timeout=300s

echo.
echo ✅ Despliegue completo!
echo 📝 Para iniciar port-forward ejecuta: start-forward.bat
echo 📝 Prueba: http://localhost/lotes
echo.
pause