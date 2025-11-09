# 🏗️ ARQUITECTURA SISTEMA BLOCKCHAIN - MERMAID

## 📊 Arquitectura General Completa

```mermaid
graph TB
    subgraph SM["🕸️ SERVICE MESH (ISTIO)"]
        direction TB
        MSP["📦 MS-Producto<br/>:8003"]
        MSL["📋 MS-Lote<br/>:8002"] 
        MSB["🏢 MS-Bodega<br/>:8001"]
        MSO["🛒 MS-Orden-Compra<br/>:8005"]
        MSPV["🏭 MS-Proveedor<br/>:8006"]
        MSPD["📊 MS-Proyección<br/>:8004"]
        MSA["📈 MS-Analytics<br/>:8010"]
        MSBC["⛓️ MS-Blockchain<br/>:8007"]
    end
    
    subgraph EM["📡 EVENT MESH (KAFKA)"]
        direction TB
        T1["📋 inventory.lote.created"]
        T2["📋 inventory.lote.updated"]
        T3["🏢 warehouse.lote.ingresado"]
        T4["🔒 warehouse.stock.reserved"]
        T5["💰 warehouse.stock.sold"]
        T6["📦 catalog.producto.created"]
    end
    
    subgraph BL["⛓️ BLOCKCHAIN LAYER"]
        direction LR
        IPFS["📁 IPFS/Pinata<br/>(Storage Off-Chain)"]
        GAN["🔗 Ganache<br/>(Ethereum Local)"]
        SC["📜 Smart Contract<br/>(Trazabilidad)"]
    end
    
    %% Conexiones Service Mesh -> Event Mesh
    MSP --> T6
    MSL --> T1
    MSL --> T2
    MSB --> T3
    MSB --> T4
    MSB --> T5
    
    %% Conexiones Event Mesh -> Blockchain
    T1 --> MSBC
    T2 --> MSBC
    T3 --> MSBC
    T4 --> MSBC
    T5 --> MSBC
    T6 --> MSBC
    
    %% Conexiones Blockchain Layer
    MSBC --> IPFS
    MSBC --> GAN
    GAN --> SC
    
    %% Estilos
    classDef serviceMesh fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef eventMesh fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef blockchain fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    
    class MSP,MSL,MSB,MSO,MSPV,MSPD,MSA,MSBC serviceMesh
    class T1,T2,T3,T4,T5,T6 eventMesh
    class IPFS,GAN,SC blockchain
```

## 🔄 Flujo de Datos Simplificado

```mermaid
graph LR
    U["👤 Usuario"] --> API["🌐 API Gateway"]
    API --> MS["🔧 Microservicio"]
    MS --> K["📡 Kafka Event"]
    K --> BC["⛓️ Blockchain Service"]
    BC --> IPFS["📁 IPFS Storage"]
    BC --> ETH["🔗 Ethereum/Ganache"]
    ETH --> SC["📜 Smart Contract"]
    
    classDef user fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    classDef service fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef blockchain fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    
    class U user
    class API,MS,K,BC service
    class IPFS,ETH,SC blockchain
```

## 🎯 Patrones Implementados

### 🔮 Patrón Oracle
```mermaid
graph LR
    EXT["🌍 Evento Externo<br/>(Sistema Inventario)"] --> EM["📡 Event Mesh<br/>(Kafka)"]
    EM --> OR["🔮 Oracle Service<br/>(MS-Blockchain)"]
    OR --> BC["⛓️ Blockchain<br/>(Smart Contract)"]
    BC --> IMM["🔒 Registro Inmutable"]
    
    classDef external fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef oracle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef blockchain fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    
    class EXT external
    class EM,OR oracle
    class BC,IMM blockchain
```

### 📁 Patrón Off-Chain Storage
```mermaid
graph LR
    DATA["📊 Datos Grandes<br/>(Metadata del Lote)"] --> IPFS["📁 IPFS<br/>(Almacenamiento)"]
    IPFS --> HASH["🔑 Content Hash<br/>(QmXXX...)"]
    HASH --> BC["⛓️ Blockchain<br/>(Solo Hash)"]
    BC --> VER["✅ Verificación<br/>(Integridad)"]
    
    classDef data fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px
    classDef storage fill:#fff8e1,stroke:#ff8f00,stroke-width:2px
    classDef blockchain fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    
    class DATA data
    class IPFS,HASH storage
    class BC,VER blockchain
```

## 🔄 Estados del Lote (Trazabilidad)

```mermaid
stateDiagram-v2
    [*] --> Creado: inventory.lote.created
    Creado --> Ingresado: warehouse.lote.ingresado
    Ingresado --> Reservado: warehouse.stock.reserved
    Reservado --> Despachado: warehouse.lote.despachado
    Despachado --> Vendido: warehouse.stock.sold
    Vendido --> [*]
    
    note right of Creado: 📝 Registro inicial<br/>⛓️ Primera transacción
    note right of Ingresado: 🏢 Movimiento a bodega<br/>⛓️ Nueva transacción
    note right of Reservado: 🔒 Stock reservado<br/>⛓️ Actualización estado
    note right of Despachado: 🚚 Salida de bodega<br/>⛓️ Trazabilidad movimiento
    note right of Vendido: 💰 Venta final<br/>⛓️ Registro inmutable final
```

## 📊 Distribución de Componentes

```mermaid
pie title Distribución de Responsabilidades
    "Service Mesh (Comunicación)" : 30
    "Event Mesh (Eventos)" : 25
    "Blockchain (Inmutabilidad)" : 25
    "IPFS (Almacenamiento)" : 20
```