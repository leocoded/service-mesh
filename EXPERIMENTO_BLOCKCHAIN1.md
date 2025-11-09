# 🔗 Experimento de Blockchain - Trazabilidad de Medicamentos

## 📋 Resumen del Experimento

Este experimento implementa un sistema de **trazabilidad completa de medicamentos** usando blockchain, combinando:
- **Service Mesh (Istio)** para comunicación entre microservicios
- **Event Mesh (Kafka)** para eventos en tiempo real
- **Blockchain (Ethereum/Ganache)** para inmutabilidad y trazabilidad
- **IPFS** para almacenamiento descentralizado de datos

## 🎯 Objetivo del Experimento

**Demostrar cómo cada operación en el sistema de inventario de medicamentos se registra de forma inmutable en blockchain, creando una cadena de trazabilidad completa desde la creación del producto hasta su venta final.**

## 🏗️ Arquitectura del Sistema

### Componentes Principales:

1. **Microservicios de Negocio**:
   - MS-Producto (Catálogo)
   - MS-Lote (Inventario)
   - MS-Bodega (Almacenamiento)

2. **Event-Driven Architecture**:
   - Kafka (Event Mesh)
   - Event Publishers/Consumers

3. **Blockchain Layer**:
   - MS-Blockchain (Trazabilidad)
   - Smart Contract (Ethereum)
   - IPFS (Almacenamiento descentralizado)
   - Ganache (Blockchain local)

4. **Service Mesh**:
   - Istio (Comunicación segura)
   - Kiali (Observabilidad)

## 🔄 Flujo del Experimento

### Caso de Uso: "Crear Lote y Almacenar en Bodega"

```
1. Usuario crea un LOTE → MS-Lote
2. MS-Lote publica evento → Kafka (Event Mesh)
3. MS-Blockchain consume evento → Procesa trazabilidad
4. Datos se almacenan en → IPFS (descentralizado)
5. Transacción se registra → Smart Contract (Ethereum)
6. Hash inmutable se genera → Blockchain
7. Usuario ingresa lote a bodega → MS-Bodega
8. Nuevo evento se publica → Kafka
9. MS-Blockchain registra movimiento → Nueva transacción
10. Trazabilidad completa disponible → Consulta blockchain
```

## 🛠️ Tecnologías Utilizadas

### 1. **Blockchain Stack**
- **Ganache**: Blockchain Ethereum local para desarrollo
- **Web3.py**: Librería para interactuar con Ethereum
- **Solidity**: Lenguaje para Smart Contracts
- **Hardhat**: Framework de desarrollo blockchain

### 2. **Event Mesh**
- **Apache Kafka**: Message broker para eventos
- **Confluent Kafka Python**: Cliente Kafka
- **Event-Driven Architecture**: Patrón de comunicación asíncrona

### 3. **Service Mesh**
- **Istio**: Service mesh para Kubernetes
- **Envoy Proxy**: Sidecar proxy para comunicación
- **Kiali**: Observabilidad del service mesh

### 4. **Storage Descentralizado**
- **IPFS**: InterPlanetary File System
- **Hash-based addressing**: Direccionamiento por contenido

### 5. **Microservicios**
- **FastAPI**: Framework web Python
- **Pydantic**: Validación de datos
- **Docker**: Containerización
- **Kubernetes**: Orquestación

## 📊 Diagramas de Componentes

### Diagrama 1: Arquitectura General
```
┌─────────────────────────────────────────────────────────────┐
│                    SERVICE MESH (ISTIO)                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ MS-Producto │  │  MS-Lote    │  │ MS-Bodega   │         │
│  │   :8003     │  │   :8002     │  │   :8001     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
├─────────────────────────────────────────────────────────────┤
│                    EVENT MESH (KAFKA)                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Topics:                                                 ││
│  │ • inventory.lote.created                               ││
│  │ • inventory.lote.updated                               ││
│  │ • warehouse.lote.ingresado                             ││
│  │ • warehouse.stock.reserved                             ││
│  │ • catalog.producto.created                             ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                  │
├─────────────────────────────────────────────────────────────┤
│                   BLOCKCHAIN LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │MS-Blockchain│  │    IPFS     │  │   Ganache   │         │
│  │   :8007     │  │ (Storage)   │  │ (Ethereum)  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Diagrama 2: Flujo de Eventos Blockchain
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Usuario   │    │  MS-Lote    │    │   Kafka     │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ POST /lotes      │                  │
       ├─────────────────►│                  │
       │                  │ publish_event    │
       │                  ├─────────────────►│
       │                  │                  │
       │                  │                  │
┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐
│ MS-Blockchain│    │    IPFS     │    │ Smart       │
│             │    │             │    │ Contract    │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ consume_event    │                  │
       │◄─────────────────┤                  │
       │                  │                  │
       │ store_data       │                  │
       ├─────────────────►│                  │
       │                  │ return hash      │
       │◄─────────────────┤                  │
       │                  │                  │
       │ record_trace     │                  │
       ├─────────────────────────────────────►│
       │                  │ return tx_hash   │
       │◄─────────────────────────────────────┤
```

### Diagrama 3: Smart Contract Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                 SMART CONTRACT                              │
│                MedicineTraceability.sol                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  struct TraceRecord {                                       │
│    string loteId;                                          │
│    string productoId;                                      │
│    string ipfsHash;                                        │
│    EventType eventType;                                    │
│    uint256 timestamp;                                      │
│    address recorder;                                       │
│  }                                                         │
│                                                             │
│  enum EventType {                                          │
│    CREATED,     // 0 - Lote creado                        │
│    UPDATED,     // 1 - Lote actualizado                   │
│    RESERVED,    // 2 - Lote reservado                     │
│    INGRESADO,   // 3 - Lote ingresado a bodega           │
│    DESPACHADO,  // 4 - Lote despachado                    │
│    SOLD         // 5 - Stock vendido                      │
│  }                                                         │
│                                                             │
│  mapping(string => TraceRecord[]) public traces;           │
│                                                             │
│  function recordTrace(...) public returns (uint256)       │
│  function getTraceHistory(...) public view returns (...)  │
│  function verifyTrace(...) public view returns (bool)     │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Casos de Uso del Experimento

### 1. **Creación de Producto**
```json
POST /productos
{
  "nombre": "Paracetamol 500mg",
  "codigo_barras": "7891234567890",
  "laboratorio": "FarmaLab",
  "principio_activo": "Paracetamol"
}
```
**Resultado**: Evento `catalog.producto.created` → Registro en blockchain

### 2. **Creación de Lote**
```json
POST /lotes
{
  "id_producto": "PROD-001",
  "id_bodega": "BOD-001",
  "cantidad_inicial": 1000,
  "fecha_vencimiento": "2025-12-31"
}
```
**Resultado**: Evento `inventory.lote.created` → IPFS + Blockchain

### 3. **Ingreso a Bodega**
```json
POST /bodegas/BOD-001/lotes/LOTE-001/ingresar
{
  "cantidad": 1000
}
```
**Resultado**: Evento `warehouse.lote.ingresado` → Nueva transacción blockchain

### 4. **Consulta de Trazabilidad**
```json
GET /blockchain/trace/lote/LOTE-001
```
**Resultado**: Historial completo desde IPFS + verificación blockchain

## 📈 Métricas y Observabilidad

### Service Mesh (Kiali)
- Visualización de comunicación entre microservicios
- Latencia y throughput de requests
- Errores y reintentos

### Event Mesh (Kafka)
- Volumen de eventos por topic
- Lag de consumers
- Particiones y replicación

### Blockchain
- Número de transacciones
- Gas utilizado
- Tiempo de confirmación
- Integridad de datos IPFS

## 🎯 Beneficios del Experimento

### 1. **Inmutabilidad**
- Los registros no pueden ser alterados
- Cada cambio genera nueva transacción
- Hash criptográfico garantiza integridad

### 2. **Trazabilidad Completa**
- Desde creación hasta venta final
- Cada movimiento registrado
- Auditoría transparente

### 3. **Descentralización**
- Datos distribuidos en IPFS
- No hay punto único de falla
- Resistente a censura

### 4. **Interoperabilidad**
- Event-driven architecture
- APIs REST estándar
- Service mesh para comunicación

## 🔬 Validación del Experimento

### Pruebas de Integridad
```bash
# 1. Crear lote
curl -X POST http://localhost/lotes -d '{...}'

# 2. Verificar evento en Kafka
docker exec kafka kafka-console-consumer --topic inventory.lote.created

# 3. Verificar registro en blockchain
curl http://localhost:8007/trace/lote/LOTE-001

# 4. Verificar datos en IPFS
curl http://localhost:8007/ipfs/QmHash...

# 5. Verificar en smart contract
curl http://localhost:8007/blockchain/verify/tx_hash
```

### Pruebas de Inmutabilidad
```bash
# Intentar modificar datos en IPFS (debe fallar)
curl -X PUT http://localhost:8007/ipfs/QmHash.../modify

# Verificar que el hash cambió si los datos cambian
curl -X POST http://localhost:8007/ipfs/test-integrity
```

## 🚀 Ejecución del Experimento

1. **Iniciar infraestructura**:
   ```bash
   .\reiniciar-sistema-completo.bat
   ```

2. **Generar tráfico de prueba**:
   ```bash
   .\generar-trafico.bat
   ```

3. **Verificar integración**:
   ```bash
   .\diagnostico-integracion.bat
   ```

4. **Monitorear en dashboards**:
   - Kiali: http://localhost:20001
   - Blockchain: http://localhost:8007/trace/all

Este experimento demuestra cómo las tecnologías modernas (microservicios, event-driven architecture, blockchain, service mesh) pueden combinarse para crear sistemas de trazabilidad robustos y confiables para industrias críticas como la farmacéutica.