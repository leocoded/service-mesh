# 🚀 Guía de Reinicio Completa - Service Mesh con Istio

## ⚡ Pasos en Orden Correcto (Método Helm - Funciona 100%)

### 1. Verificar que todo esté listo
```powershell
cd d:\proyectos\nuevas_generaciones\service-mesh
docker --version
kubectl cluster-info
kubectl config current-context  # Debe ser: docker-desktop
```

### 2. Instalar Helm (Solo la primera vez)
```powershell
# Si no tienes Helm instalado
curl https://get.helm.sh/helm-v3.13.0-windows-amd64.zip -o helm.zip
Expand-Archive helm.zip -DestinationPath .
move windows-amd64\helm.exe C:\Windows\System32\
```

### 3. Instalar Istio con Helm
```powershell
# Agregar repositorio de Istio
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

# Instalar Istio base
helm install istio-base istio/base -n istio-system --create-namespace

# Instalar Istio control plane
helm install istiod istio/istiod -n istio-system

# Instalar gateway
helm install istio-ingress istio/gateway -n istio-system

# Verificar instalación
kubectl get pods -n istio-system
```

### 4. Iniciar Event Mesh y Blockchain
```powershell
# Iniciar Kafka y Redis con Docker Compose
docker-compose -f docker-compose-kafka.yml up -d
docker-compose -f docker-compose-redis.yml up -d

# Iniciar Ganache para Blockchain (en nueva ventana)
cd ms-blockchain
npm run ganache
# O en ventana separada: Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run ganache"
cd ..

# Verificar que estén corriendo
docker ps
```

### 5. Instalar addons de monitoreo
```powershell
# Instalar Kiali, Prometheus, Grafana y Jaeger
kubectl apply -f https://raw.githubusercontent.com/istio/istio/1.24.0/samples/addons/kiali.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/1.24.0/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/1.24.0/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/1.24.0/samples/addons/jaeger.yaml

# Esperar a que todos estén corriendo
kubectl get pods -n istio-system
```

### 6. Construir imágenes de microservicios
```powershell
# Construir todas las imágenes Docker (necesario después de cambios en código)
docker build -t ms-bodega:latest ./ms-bodega
docker build -t ms-lote:latest ./ms-lote
docker build -t ms-producto:latest ./ms-producto
#docker build -t ms-orden-compra:latest ./ms-orden-compra
#docker build -t ms-proveedor:latest ./ms-proveedor
#docker build -t ms-proyeccion-demanda:latest ./ms-proyeccion-demanda
docker build -t ms-blockchain:latest ./ms-blockchain
docker build -t ms-analytics:latest ./ms-analytics
```

### 7. Configurar conectividad externa (Kafka/Redis)
```powershell
# Crear servicios externos para que Kubernetes acceda a Kafka y Redis
kubectl apply -f kafka-external.yaml

# Verificar servicios externos
kubectl get svc -n service-mesh
```

### 8. Desplegar microservicios
```powershell
# Aplicar configuración de microservicios
kubectl apply -f istio.yaml

# Verificar que todos estén corriendo
kubectl get pods -n service-mesh
kubectl get svc -n istio-system
```

### 9. Configurar Port Forwarding (TODO EN UNO)
```powershell
# Un solo script para todo
./swagger-forwards.bat
```

### 10. Generar tráfico para activar dashboards
```powershell
# Ejecutar script para generar tráfico y activar Kiali/Grafana/Jaeger
./generar-trafico.bat
```

### 11. Acceder a microservicios a través del Gateway
```powershell
# Ver el puerto del gateway
kubectl get svc -n istio-system istio-ingress

# Los microservicios estarán disponibles en:
# http://localhost/bodegas
# http://localhost/lotes  
# http://localhost/productos
# http://localhost/ordenes
# http://localhost/proveedores
# http://localhost/proyecciones
```

## 🌐 URLs de Acceso Final

### Dashboards de Monitoreo:
- **Kiali (Service Mesh)**: http://localhost:20001
- **Grafana (Métricas)**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Jaeger (Tracing)**: http://localhost:16686

### Swagger UIs (Port-Forward - NO se ven en Kiali):
- **MS-Producto**: http://localhost:8003/docs
- **MS-Bodega**: http://localhost:8001/docs
- **MS-Lote**: http://localhost:8002/docs
- **MS-Orden-Compra**: http://localhost:8005/docs
- **MS-Proveedor**: http://localhost:8006/docs
- **MS-Proyeccion-Demanda**: http://localhost:8004/docs
- **MS-Blockchain**: http://localhost:8007/docs
- **MS-Analytics**: http://localhost:8010/docs
- **MS-Oracle**: http://localhost:8008/docs

### Swagger UIs (Gateway - SÍ se ven en Kiali):
- **MS-Producto**: http://localhost/productos/docs
- **MS-Bodega**: http://localhost/bodegas/docs
- **MS-Lote**: http://localhost/lotes/docs
- **MS-Orden-Compra**: http://localhost/ordenes/docs
- **MS-Proveedor**: http://localhost/proveedores/docs
- **MS-Proyeccion-Demanda**: http://localhost/proyecciones/docs

### APIs REST (datos):
- **Productos**: http://localhost/productos
- **Bodegas**: http://localhost/bodegas
- **Lotes**: http://localhost/lotes
- **Órdenes**: http://localhost/ordenes
- **Proveedores**: http://localhost/proveedores
- **Proyecciones**: http://localhost/proyecciones

### Event Mesh:
- **Kafka UI**: http://localhost:8080 (si usas docker-compose-complete.yml)
- **Redis**: localhost:6379

### Blockchain:
- **Ganache**: http://localhost:8545 (RPC)
- **Ganache UI**: Consola en terminal
- **MS-Blockchain**: http://localhost:8007/docs
- **Blockchain UI**: http://localhost:8007/ui (si está configurado)

## 📊 Generar Tráfico para Pruebas

```powershell
# Script automático para activar todos los dashboards
./generar-trafico.bat

# O manualmente para pruebas específicas:
for ($i=1; $i -le 20; $i++) {
    curl http://localhost/productos
    curl http://localhost/bodegas
    curl http://localhost/lotes
    curl http://localhost/ordenes
    curl http://localhost/proveedores
    curl http://localhost/proyecciones
    Start-Sleep 2
}

# Verificar Kafka topics
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list

# Crear un topic de prueba
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic test-topic --partitions 1 --replication-factor 1

# Probar Blockchain y IPFS
curl -X POST http://localhost:8007/blockchain/deploy
curl http://localhost:8007/blockchain/accounts
curl http://localhost:8007/ipfs/status

# Ver transacciones en Ganache
curl -X POST http://localhost:8545 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

## 🔄 Reconstruir Imágenes (Cuando modifiques código)

```powershell
# Si modificas models.py o cualquier archivo de un microservicio:

# 1. Reconstruir imagen específica
docker build -t ms-producto:latest ./ms-producto

# 2. Reiniciar deployment para usar nueva imagen
kubectl rollout restart deployment/ms-producto -n service-mesh

# 3. Verificar que se reinició
kubectl get pods -n service-mesh

# Para todos los microservicios a la vez:
docker build -t ms-bodega:latest ./ms-bodega
docker build -t ms-lote:latest ./ms-lote
docker build -t ms-producto:latest ./ms-producto
docker build -t ms-orden-compra:latest ./ms-orden-compra
docker build -t ms-proveedor:latest ./ms-proveedor
docker build -t ms-proyeccion-demanda:latest ./ms-proyeccion-demanda
docker build -t ms-blockchain:latest ./ms-blockchain
docker build -t ms-analytics:latest ./ms-analytics

# Reiniciar todos los deployments
kubectl rollout restart deployment -n service-mesh
```

## 🔧 Comandos de Verificación

```powershell
# Verificar que todo esté corriendo
kubectl get pods -n istio-system
kubectl get pods -n service-mesh

# Ver servicios y puertos
kubectl get svc -n istio-system
kubectl get svc -n service-mesh

# Ver gateway y virtual services
kubectl get gateway -n service-mesh
kubectl get virtualservice -n service-mesh
```

## 🔍 Diferencia entre Port-Forward y Gateway

**¿Por qué Kiali no muestra tráfico del Swagger pero sí del script?**

```powershell
# ✅ ESTO SE VE EN KIALI (pasa por Istio Gateway)
curl http://localhost/productos
curl http://localhost/lotes/docs

# ❌ ESTO NO SE VE EN KIALI (port-forward directo, bypasea Istio)
curl http://localhost:8003/productos  
curl http://localhost:8002/docs
```

**Solución**: Para que el tráfico se vea en Kiali, usa las URLs del Gateway:
- **Port-Forward**: `http://localhost:8002/docs` → NO se ve en Kiali
- **Gateway**: `http://localhost/lotes/docs` → SÍ se ve en Kiali

## 📋 Scripts de Logs para Debugging

```powershell
# Ver logs de un microservicio específico
kubectl logs -n service-mesh deployment/ms-lote --tail=50
kubectl logs -n service-mesh deployment/ms-blockchain --tail=50
kubectl logs -n service-mesh deployment/ms-oracle --tail=50

# Seguir logs en tiempo real
kubectl logs -n service-mesh deployment/ms-lote -f
kubectl logs -n service-mesh deployment/ms-blockchain -f

# Ver logs de todos los pods de un deployment
kubectl logs -n service-mesh -l app=ms-lote --tail=20

# Ver eventos del namespace
kubectl get events -n service-mesh --sort-by='.lastTimestamp'

# Ver descripción de un pod con problemas
kubectl describe pod -n service-mesh <pod-name>

# Ver logs del istio-proxy (sidecar)
kubectl logs -n service-mesh <pod-name> -c istio-proxy --tail=20

# Verificar conectividad Kafka desde un pod
kubectl exec -n service-mesh deployment/ms-lote -- nslookup kafka-external

# Ver todos los pods con su estado
kubectl get pods -n service-mesh -o wide
```

## 🧹 Limpiar Servicios Innecesarios

```powershell
# Eliminar servicios de ejemplo de Istio (si existen)
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/bookinfo/platform/kube/bookinfo.yaml

# Si necesitas reconfigurar conectividad externa
kubectl apply -f kafka-external.yaml

# Reconstruir microservicios para usar nueva configuración
kubectl rollout restart deployment -n service-mesh
```

## 🚨 Solución de Problemas

### Si los pods no inician:
```powershell
# Ver logs de un pod específico
kubectl logs -n istio-system <pod-name>
kubectl logs -n service-mesh <pod-name>

# Reiniciar un deployment
kubectl rollout restart deployment/<deployment-name> -n service-mesh
```

### Si el gateway no funciona:
```powershell
# Verificar que el gateway esté corriendo
kubectl get svc -n istio-system istio-ingress

# Debe mostrar EXTERNAL-IP como localhost
```

### Reinicio completo:
```powershell
# Limpiar todo
kubectl delete namespace service-mesh
helm uninstall istio-ingress -n istio-system
helm uninstall istiod -n istio-system  
helm uninstall istio-base -n istio-system
kubectl delete namespace istio-system

# Reiniciar desde el paso 3
```

## ✅ Checklist Final

- [ ] Docker Desktop corriendo
- [ ] Kubernetes activo (`kubectl cluster-info`)
- [ ] Helm instalado
- [ ] **Kafka y Redis corriendo** (`docker ps`)
- [ ] **Ganache corriendo** (`npm run ganache`)
- [ ] **Imágenes Docker construidas** (paso 6)
- [ ] **Conectividad externa configurada** (`kubectl apply -f kafka-external.yaml`)
- [ ] Istio pods corriendo (`kubectl get pods -n istio-system`)
- [ ] Microservicios corriendo (`kubectl get pods -n service-mesh`)
- [ ] Gateway activo (`kubectl get svc -n istio-system istio-ingress`)
- [ ] Port forwarding configurado
- [ ] **Tráfico generado** (`./generar-trafico.bat`)
- [ ] Kiali accesible en http://localhost:20001
- [ ] APIs accesibles a través del gateway

---
**💡 Con este método usando Helm, el reinicio debería tomar solo 5-10 minutos**