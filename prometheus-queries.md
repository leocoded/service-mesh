# 📊 Queries Útiles para Prometheus - Service Mesh

## 🚀 Métricas de Tráfico HTTP

### Request Rate (RPS)
```
sum(rate(istio_requests_total[5m])) by (destination_service_name)
```

### Success Rate por Servicio
```
sum(rate(istio_requests_total{response_code!~"5.*"}[5m])) by (destination_service_name) / sum(rate(istio_requests_total[5m])) by (destination_service_name) * 100
```

### Response Time P95
```
histogram_quantile(0.95, sum(rate(istio_request_duration_milliseconds_bucket[5m])) by (destination_service_name, le))
```

### Error Rate (4xx + 5xx)
```
sum(rate(istio_requests_total{response_code=~"4.*|5.*"}[5m])) by (destination_service_name)
```

## 🔗 Métricas de Conectividad

### TCP Connections (Kafka)
```
sum(istio_tcp_connections_opened_total) by (destination_service_name)
```

### Bytes Sent/Received
```
sum(rate(istio_tcp_sent_bytes_total[5m])) by (destination_service_name)
sum(rate(istio_tcp_received_bytes_total[5m])) by (destination_service_name)
```

## 📈 Métricas de Pods

### CPU Usage
```
sum(rate(container_cpu_usage_seconds_total{namespace="service-mesh"}[5m])) by (pod)
```

### Memory Usage
```
sum(container_memory_working_set_bytes{namespace="service-mesh"}) by (pod)
```

### Pod Restarts
```
sum(increase(kube_pod_container_status_restarts_total{namespace="service-mesh"}[1h])) by (pod)
```

## 🎯 Queries por Microservicio

### MS-Lote específico
```
sum(rate(istio_requests_total{destination_service_name="ms-lote"}[5m]))
```

### MS-Blockchain específico
```
sum(rate(istio_requests_total{destination_service_name="ms-blockchain"}[5m]))
```

## 🔍 Debugging

### Ver todos los targets
```
up
```

### Ver métricas disponibles
```
{__name__=~"istio.*"}
```

### Servicios activos
```
sum by (destination_service_name) (istio_requests_total)
```