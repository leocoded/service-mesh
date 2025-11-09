@echo off
echo 🧹 Limpiando ambiente completo...
echo.

echo [1/5] Deteniendo port-forwards...
taskkill /f /im kubectl.exe > nul 2>&1

echo [2/5] Eliminando namespaces de Kubernetes...
kubectl delete namespace service-mesh --ignore-not-found=true
kubectl delete namespace event-mesh --ignore-not-found=true
kubectl delete namespace istio-system --ignore-not-found=true

echo [3/5] Deteniendo contenedores Docker...
docker-compose -f docker-compose-kafka.yml down > nul 2>&1
docker stop $(docker ps -q) > nul 2>&1

echo [4/5] Limpiando imágenes Docker...
docker system prune -f > nul 2>&1

echo [5/5] Verificando limpieza...
kubectl get namespaces
docker ps

echo.
echo ✅ Ambiente limpio!
echo.
pause