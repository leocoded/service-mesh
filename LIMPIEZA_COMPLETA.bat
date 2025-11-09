@echo off
echo 🧹 LIMPIEZA COMPLETA DEL SISTEMA
echo ================================

echo 1. Deteniendo todos los contenedores...
docker stop $(docker ps -aq) 2>nul
docker rm $(docker ps -aq) 2>nul

echo 2. Eliminando imágenes del proyecto...
docker rmi ms-bodega:latest 2>nul
docker rmi ms-lote:latest 2>nul
docker rmi ms-producto:latest 2>nul
docker rmi ms-blockchain:latest 2>nul
docker rmi ms-analytics:latest 2>nul
docker rmi ms-orden-compra:latest 2>nul
docker rmi ms-proveedor:latest 2>nul
docker rmi ms-proyeccion-demanda:latest 2>nul

echo 3. Eliminando namespace de Kubernetes...
kubectl delete namespace service-mesh --ignore-not-found=true

echo 4. Limpiando volúmenes Docker...
docker volume prune -f

echo 5. Limpiando redes Docker...
docker network prune -f

echo 6. Estado final:
docker ps
docker images | findstr ms-

echo ✅ Sistema completamente limpio!
pause