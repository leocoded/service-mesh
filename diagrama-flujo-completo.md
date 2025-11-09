# 🔄 DIAGRAMA DE SECUENCIA - FLUJO COMPLETO BLOCKCHAIN

## Flujo Principal: Creación de Lote con Trazabilidad Blockchain

```mermaid
sequenceDiagram
    participant U as Usuario
    participant API as API Gateway (Istio)
    participant MS as MS-Lote
    participant K as Kafka Event Mesh
    participant BC as MS-Blockchain
    participant IPFS as IPFS/Pinata
    participant ETH as Ganache (Ethereum)
    participant SC as Smart Contract

    Note over U,SC: 🎯 FLUJO COMPLETO DE TRAZABILIDAD BLOCKCHAIN

    %% 1. Creación de Lote
    U->>+API: POST /lotes (crear lote)
    API->>+MS: Crear lote medicamento
    MS->>MS: Validar datos
    MS->>MS: Generar ID único
    MS-->>-API: Lote creado exitosamente
    API-->>-U: Response: Lote ID + detalles

    %% 2. Publicación de Evento
    Note over MS,K: 📡 EVENT-DRIVEN ARCHITECTURE
    MS->>+K: Publish event "inventory.lote.created"
    Note right of K: Topic: inventory.lote.created<br/>Payload: lote_data + metadata
    K-->>-MS: Event published ✅

    %% 3. Consumo por Blockchain Service
    Note over K,BC: 🔮 ORACLE PATTERN
    K->>+BC: Event consumed by blockchain service
    BC->>BC: Process lote creation event
    BC->>BC: Prepare blockchain transaction

    %% 4. Almacenamiento Off-Chain (IPFS)
    Note over BC,IPFS: 📁 OFF-CHAIN STORAGE PATTERN
    BC->>+IPFS: Store lote data + metadata
    Note right of IPFS: Datos grandes almacenados<br/>descentralizadamente
    IPFS->>IPFS: Generate content hash
    IPFS-->>-BC: Return IPFS hash

    %% 5. Registro en Blockchain
    Note over BC,ETH: ⛓️ BLOCKCHAIN IMMUTABLE RECORD
    BC->>+ETH: Create transaction
    ETH->>+SC: Call recordTrace()
    Note right of SC: Smart Contract<br/>MedicineTraceability.sol
    SC->>SC: Store: loteId + IPFS hash + timestamp
    SC->>SC: Emit TraceRecorded event
    SC-->>-ETH: Transaction successful
    ETH->>ETH: Mine block
    ETH-->>-BC: Return tx_hash + block_number

    %% 6. Confirmación Final
    BC->>BC: Store trace record locally
    BC-->>K: Processing complete ✅

    %% 7. Consulta de Trazabilidad
    Note over U,SC: 🔍 CONSULTA DE TRAZABILIDAD
    U->>+API: GET /blockchain/trace/lote/{id}
    API->>+BC: Get trace history
    BC->>+ETH: Query blockchain
    ETH->>+SC: getTraceHistory(loteId)
    SC-->>-ETH: Return trace records
    ETH-->>-BC: Blockchain data
    BC->>+IPFS: Retrieve detailed data
    IPFS-->>-BC: Return stored data
    BC-->>-API: Complete trace history
    API-->>-U: Trazabilidad completa

    Note over U,SC: ✅ TRAZABILIDAD INMUTABLE COMPLETADA
```

## 🏗️ PATRONES IMPLEMENTADOS

### 1. 🔮 **Oracle Pattern**
```mermaid
graph LR
    A[Evento Externo] --> B[Kafka Event Mesh]
    B --> C[MS-Blockchain Oracle]
    C --> D[Smart Contract]
    D --> E[Blockchain Inmutable]
```

### 2. 📁 **Off-Chain Storage Pattern**
```mermaid
graph LR
    A[Datos Grandes] --> B[IPFS Storage]
    B --> C[Content Hash]
    C --> D[Blockchain Reference]
    D --> E[Verificación Integridad]
```

### 3. 📡 **Event-Driven Architecture**
```mermaid
graph TD
    A[MS-Lote] --> B[Kafka Topic]
    C[MS-Bodega] --> B
    D[MS-Producto] --> B
    B --> E[MS-Blockchain]
    B --> F[MS-Analytics]
    B --> G[Other Consumers]
```

## 🎯 BENEFICIOS DEL SISTEMA

| Componente | Beneficio | Implementación |
|------------|-----------|----------------|
| **Service Mesh** | Comunicación segura | Istio + Envoy |
| **Event Mesh** | Desacoplamiento | Kafka Topics |
| **Blockchain** | Inmutabilidad | Smart Contracts |
| **IPFS** | Descentralización | Content Addressing |
| **Oracle** | Datos externos | Event Consumers |

## 📊 MÉTRICAS DE TRAZABILIDAD

```mermaid
pie title Distribución de Datos
    "Blockchain (Hashes)" : 15
    "IPFS (Datos Detallados)" : 70
    "Cache Local" : 10
    "Event Stream" : 5
```

## 🔄 ESTADOS DEL LOTE

```mermaid
stateDiagram-v2
    [*] --> Creado: inventory.lote.created
    Creado --> Ingresado: warehouse.lote.ingresado
    Ingresado --> Reservado: warehouse.stock.reserved
    Reservado --> Despachado: warehouse.lote.despachado
    Despachado --> Vendido: warehouse.stock.sold
    Vendido --> [*]
    
    note right of Creado: Registro inicial en blockchain
    note right of Ingresado: Nueva transacción
    note right of Reservado: Actualización de estado
    note right of Despachado: Trazabilidad de movimiento
    note right of Vendido: Registro final inmutable
```