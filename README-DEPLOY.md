# 🚀 Guía de Despliegue - Service Mesh

## Prerrequisitos
- Docker Desktop con Kubernetes habilitado
- Istio instalado
- kubectl configurado

## Despliegue Completo

### Opción 1: Script Automático
```bash
deploy.bat
```

### Opción 2: Manual
```bash
# 1. Event Mesh (Kafka)
kubectl apply -f kafka-k8s.yaml

# 2. Microservicios
kubectl apply -f istio.yaml

# 3. Verificar
kubectl get pods -n event-mesh
kubectl get pods -n service-mesh
```

## URLs del Sistema

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **API Gateway** | http://localhost | Punto de entrada principal |
| **Kiali** | http://localhost:20001 | Service Mesh Dashboard |
| **Kafka UI** | http://localhost:30080 | Event Mesh Dashboard |
| **Grafana** | http://localhost:3000 | Métricas y monitoreo |
| **Jaeger** | http://localhost:16686 | Trazabilidad distribuida |

## Endpoints API

| Microservicio | Endpoint | Ejemplo |
|---------------|----------|---------|
| **Lotes** | `/lotes` | `POST http://localhost/lotes` |
| **Productos** | `/productos` | `GET http://localhost/productos` |
| **Blockchain** | `/blockchain` | `GET http://localhost/blockchain/trace/all` |
| **Bodegas** | `/bodegas` | `GET http://localhost/bodegas` |

## Verificación Rápida

```bash
# Crear lote de prueba
curl -X POST "http://localhost/lotes" \
  -H "Content-Type: application/json" \
  -d '{"fecha_vencimiento":"2025-12-31","tipo_almacenamiento":"refrigerado","cantidad_inicial":100,"id_producto":"TEST","id_bodega":"CENTRAL","temperatura_optima":4.0,"humedad_optima":60.0}'

# Ver en Kiali: namespace service-mesh
# Ver en Kafka UI: topic inventory.lote.created
```

## Arquitectura Desplegada

```
┌─────────────────┐    ┌─────────────────┐
│   Service Mesh  │    │   Event Mesh    │
│   (Istio)       │    │   (Kafka)       │
├─────────────────┤    ├─────────────────┤
│ • ms-lote       │◄──►│ • Kafka         │
│ • ms-producto   │    │ • Zookeeper     │
│ • ms-blockchain │    │ • Kafka UI      │
│ • ms-bodega     │    │                 │
│ • API Gateway   │    │                 │
└─────────────────┘    └─────────────────┘
```

## Troubleshooting

```bash
# Ver logs
kubectl logs -n service-mesh deployment/ms-lote
kubectl logs -n event-mesh deployment/kafka

# Reiniciar servicios
kubectl rollout restart deployment -n service-mesh
kubectl rollout restart deployment -n event-mesh

# Limpiar y redesplegar
kubectl delete -f istio.yaml
kubectl delete -f kafka-k8s.yaml
./deploy.bat
```