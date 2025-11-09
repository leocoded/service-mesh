@echo off
echo 🚪 Instalando Istio Gateway...
echo.

echo [1/2] Instalando Istio Gateway...
helm install istio-gateway istio/gateway -n istio-system

echo [2/2] Configurando port-forward al gateway...
kubectl port-forward -n istio-system svc/istio-gateway 80:80

echo.
echo ✅ Gateway configurado en puerto 80!
echo.
pause