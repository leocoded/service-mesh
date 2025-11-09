@echo off
echo 🔧 Instalando Istio...
echo.

echo [1/4] Agregando repositorio Helm...
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

echo [2/4] Instalando Istio base...
helm install istio-base istio/base -n istio-system --create-namespace

echo [3/4] Instalando Istio control plane...
helm install istiod istio/istiod -n istio-system

echo [4/4] Instalando gateway...
helm install istio-ingress istio/gateway -n istio-system

echo [4/4] Verificando instalación...
kubectl get pods -n istio-system

echo.
echo ✅ Istio instalado!
echo.
pause