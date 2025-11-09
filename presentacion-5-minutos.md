# 🎯 PRESENTACIÓN 5 MINUTOS - SISTEMA BLOCKCHAIN TRAZABILIDAD

## 📊 DIAGRAMA PRINCIPAL (2 minutos)

```mermaid
sequenceDiagram
    participant U as Usuario
    participant API as Gateway Istio
    participant MS as MS-Lote
    participant K as Kafka
    participant BC as MS-Blockchain
    participant IPFS as IPFS/Pinata
    participant ETH as Ganache

    Note over U,ETH: 🎯 TRAZABILIDAD BLOCKCHAIN MEDICAMENTOS

    %% 1. Crear Lote
    U->>+API: POST /lotes (crear lote)
    API->>+MS: Crear lote medicamento
    MS->>MS: Validar y generar ID
    MS-->>-API: Lote creado ✅
    API-->>-U: Respuesta: ID del lote

    %% 2. Evento Kafka
    Note over MS,K: 📡 ARQUITECTURA DIRIGIDA POR EVENTOS
    MS->>+K: Publicar evento "lote.creado"
    Note right of K: Topic: inventory.lote.created
    K-->>-MS: Evento publicado ✅

    %% 3. Blockchain Oracle
    Note over K,BC: 🔮 PATRÓN ORACLE
    K->>+BC: Consumir evento blockchain
    BC->>BC: Procesar creación de lote

    %% 4. Almacenamiento IPFS
    Note over BC,IPFS: 📁 ALMACENAMIENTO OFF-CHAIN
    BC->>+IPFS: Guardar datos del lote
    Note right of IPFS: Datos grandes<br/>descentralizados
    IPFS-->>-BC: Hash IPFS generado

    %% 5. Transacción Blockchain
    Note over BC,ETH: ⛓️ REGISTRO INMUTABLE
    BC->>+ETH: Crear transacción
    ETH->>ETH: Minar bloque
    ETH-->>-BC: Hash transacción + bloque

    %% 6. Consulta Trazabilidad
    Note over U,ETH: 🔍 CONSULTA TRAZABILIDAD
    U->>+API: GET /trazabilidad/{lote_id}
    API->>+BC: Obtener historial
    BC->>ETH: Consultar blockchain
    BC->>IPFS: Recuperar datos
    BC-->>-API: Trazabilidad completa
    API-->>-U: Historial inmutable ✅

    Note over U,ETH: ✅ TRAZABILIDAD COMPLETA GARANTIZADA
```

## 🏗️ ARQUITECTURA IMPLEMENTADA (1 minuto)

```mermaid
graph TB
    subgraph "SERVICE MESH (ISTIO)"
        A[MS-Lote :8002]
        B[MS-Bodega :8001] 
        C[MS-Producto :8003]
        D[MS-Blockchain :8007]
    end
    
    subgraph "EVENT MESH (KAFKA)"
        E[inventory.lote.created]
        F[warehouse.stock.reserved]
        G[warehouse.stock.sold]
    end
    
    subgraph "BLOCKCHAIN LAYER"
        H[IPFS/Pinata<br/>Almacenamiento]
        I[Ganache<br/>Ethereum Local]
        J[Smart Contract<br/>Trazabilidad]
    end
    
    A --> E
    B --> F
    C --> E
    E --> D
    F --> D
    G --> D
    D --> H
    D --> I
    I --> J
```

## 🎯 PATRONES BLOCKCHAIN (1 minuto)

### 🔮 Patrón Oracle
```mermaid
graph LR
    A[Evento Externo<br/>Sistema Inventario] --> B[Kafka<br/>Event Mesh]
    B --> C[MS-Blockchain<br/>Oracle Service]
    C --> D[Smart Contract<br/>Ethereum]
    D --> E[Blockchain<br/>Inmutable]
```

### 📁 Patrón Off-Chain Storage
```mermaid
graph LR
    A[Datos Grandes<br/>Lote + Metadata] --> B[IPFS<br/>Almacenamiento]
    B --> C[Hash Contenido<br/>QmXXX...]
    C --> D[Blockchain<br/>Solo Hash]
    D --> E[Verificación<br/>Integridad]
```

## 📋 GUIÓN PRESENTACIÓN (5 minutos)

### Minuto 1: **Introducción**
> "Implementé un sistema de trazabilidad blockchain para medicamentos usando service mesh con Istio, event-driven architecture con Kafka, y patrones blockchain avanzados."

### Minuto 2: **Demostración Arquitectura**
> "Tengo 8 microservicios corriendo en Kubernetes con Istio. Cuando creo un lote, automáticamente se genera un evento en Kafka que dispara la trazabilidad blockchain."

### Minuto 3: **Mostrar Componentes**
- **Kiali**: "Service mesh visualiza la comunicación"
- **Kafka UI**: "Eventos se generan automáticamente"
- **Swagger**: "APIs funcionan independientemente"

### Minuto 4: **Patrones Blockchain**
> "Implementé el patrón Oracle donde blockchain actúa como fuente de verdad externa, y off-chain storage donde IPFS almacena datos grandes mientras blockchain solo guarda hashes."

### Minuto 5: **Beneficios y Conclusión**
> "El sistema garantiza inmutabilidad, trazabilidad completa, y escalabilidad. Cada operación deja rastro verificable desde creación hasta venta final."

## 🎬 QUÉ MOSTRAR EN PANTALLA

1. **Diagrama de secuencia** (30 seg)
2. **Kiali - Service mesh** (30 seg)
3. **Kafka UI - Eventos** (30 seg)
4. **Swagger APIs** (30 seg)
5. **Arquitectura general** (30 seg)
6. **Patrones implementados** (resto)

## ✅ PUNTOS CLAVE A DESTACAR

- ✅ **Arquitectura completa implementada**
- ✅ **Patrones blockchain correctos**
- ✅ **Event-driven architecture funcionando**
- ✅ **Service mesh operativo**
- ✅ **Almacenamiento distribuido**
- ✅ **Trazabilidad inmutable diseñada**