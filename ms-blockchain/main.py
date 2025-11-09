from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from datetime import datetime
import uuid
import threading
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.kafka_client import KafkaEventClient
from models import TraceRecord, TraceResponse
from blockchain_service import BlockchainService
from ipfs_pinata_service import IPFSPinataService
from smart_contract_service import SmartContractService
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="MS-Blockchain API",
    description="Microservicio para trazabilidad blockchain",
    version="1.0.0"
)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulación de registros blockchain
blockchain_records = {}

# Servicios
blockchain_service = BlockchainService()
ipfs_service = IPFSPinataService()
smart_contract_service = SmartContractService(blockchain_service.w3)

def handle_lote_created(data: Dict[Any, Any], key: str):
    """Handler para eventos de creación de lote"""
    print(f"📦 Procesando creación de lote: {key}")
    
    # 1. Almacenar datos detallados en IPFS
    ipfs_hash = ipfs_service.store_data(data["data"])
    
    # 2. Crear registro en smart contract en Polygon Amoy
    private_key = os.getenv('PRIVATE_KEY')
    blockchain_result = smart_contract_service.record_trace(
        lote_id=key,
        producto_id=data["data"].get("producto_id", "UNKNOWN"),
        ipfs_hash=ipfs_hash,
        event_type=0,  # CREATED = 0
        private_key=private_key
    )
    
    # 3. Crear registro de trazabilidad
    trace_id = str(uuid.uuid4())
    record = {
        "trace_id": trace_id,
        "lote_id": key,
        "event_type": "LOTE_CREATED",
        "data": data["data"],
        "timestamp": datetime.now(),
        "blockchain_tx": blockchain_result["tx_hash"],
        "ipfs_hash": ipfs_hash,
        "status": blockchain_result["status"],
        "block_number": blockchain_result.get("block_number", 0)
    }
    
    blockchain_records[trace_id] = record
    print(f"✅ Registro blockchain creado: {trace_id}")
    print(f"🔗 TX: {blockchain_result['tx_hash']}")
    print(f"📁 IPFS: {ipfs_hash}")

def handle_lote_updated(data: Dict[Any, Any], key: str):
    """Handler para eventos de actualización de lote"""
    print(f"🔄 Procesando actualización de lote: {key}")
    
    # 1. Almacenar datos en IPFS
    ipfs_hash = ipfs_service.store_data(data["data"])
    
    # 2. Crear registro en smart contract
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    blockchain_result = smart_contract_service.record_trace(
        lote_id=key,
        producto_id=data["data"].get("producto_id", "UNKNOWN"),
        ipfs_hash=ipfs_hash,
        event_type=1,  # UPDATED = 1
        private_key=private_key
    )
    
    # 3. Crear registro de trazabilidad
    trace_id = str(uuid.uuid4())
    record = {
        "trace_id": trace_id,
        "lote_id": key,
        "event_type": "LOTE_UPDATED",
        "data": data["data"],
        "timestamp": datetime.now(),
        "blockchain_tx": blockchain_result["tx_hash"],
        "ipfs_hash": ipfs_hash,
        "status": blockchain_result["status"],
        "block_number": blockchain_result.get("block_number", 0)
    }
    
    blockchain_records[trace_id] = record
    print(f"✅ Actualización registrada: {trace_id}")
    print(f"🔗 TX: {blockchain_result['tx_hash']}")
    print(f"📁 IPFS: {ipfs_hash}")

def handle_lote_reserved(data: Dict[Any, Any], key: str):
    """Handler para eventos de reserva de lote"""
    print(f"🔒 Procesando reserva de lote: {key}")
    
    # 1. Almacenar datos en IPFS
    ipfs_hash = ipfs_service.store_data(data["data"])
    
    # 2. Crear registro en smart contract
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    blockchain_result = smart_contract_service.record_trace(
        lote_id=key,
        producto_id=data["data"].get("producto_id", "UNKNOWN"),
        ipfs_hash=ipfs_hash,
        event_type=2,  # RESERVED = 2
        private_key=private_key
    )
    
    # 3. Crear registro de trazabilidad
    trace_id = str(uuid.uuid4())
    record = {
        "trace_id": trace_id,
        "lote_id": key,
        "event_type": "LOTE_RESERVED",
        "data": data["data"],
        "timestamp": datetime.now(),
        "blockchain_tx": blockchain_result["tx_hash"],
        "ipfs_hash": ipfs_hash,
        "status": blockchain_result["status"],
        "block_number": blockchain_result.get("block_number", 0)
    }
    
    blockchain_records[trace_id] = record
    print(f"✅ Reserva registrada: {trace_id}")
    print(f"🔗 TX: {blockchain_result['tx_hash']}")
    print(f"📁 IPFS: {ipfs_hash}")

def handle_lote_ingresado(data: Dict[Any, Any], key: str):
    """Handler para ingreso de lote a bodega (Caso de negocio)"""
    print(f"🏢 Procesando ingreso de lote: {key}")
    
    # Almacenar en IPFS
    ipfs_hash = ipfs_service.store_data(data["data"])
    
    # Registrar en blockchain
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    blockchain_result = smart_contract_service.record_trace(
        lote_id=key,
        producto_id=data["data"].get("lote_id", "UNKNOWN"),
        ipfs_hash=ipfs_hash,
        event_type=3,  # INGRESADO = 3
        private_key=private_key
    )
    
    # Crear registro
    trace_id = str(uuid.uuid4())
    record = {
        "trace_id": trace_id,
        "lote_id": key,
        "event_type": "LOTE_INGRESADO",
        "data": data["data"],
        "timestamp": datetime.now(),
        "blockchain_tx": blockchain_result["tx_hash"],
        "ipfs_hash": ipfs_hash,
        "status": blockchain_result["status"],
        "block_number": blockchain_result.get("block_number", 0)
    }
    
    blockchain_records[trace_id] = record
    print(f"✅ Ingreso registrado: {trace_id}")

def handle_lote_despachado(data: Dict[Any, Any], key: str):
    """Handler para despacho de lote desde bodega (Caso de negocio)"""
    print(f"🚚 Procesando despacho de lote: {key}")
    
    # Almacenar en IPFS
    ipfs_hash = ipfs_service.store_data(data["data"])
    
    # Registrar en blockchain
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    blockchain_result = smart_contract_service.record_trace(
        lote_id=key,
        producto_id=data["data"].get("lote_id", "UNKNOWN"),
        ipfs_hash=ipfs_hash,
        event_type=4,  # DESPACHADO = 4
        private_key=private_key
    )
    
    # Crear registro
    trace_id = str(uuid.uuid4())
    record = {
        "trace_id": trace_id,
        "lote_id": key,
        "event_type": "LOTE_DESPACHADO",
        "data": data["data"],
        "timestamp": datetime.now(),
        "blockchain_tx": blockchain_result["tx_hash"],
        "ipfs_hash": ipfs_hash,
        "status": blockchain_result["status"],
        "block_number": blockchain_result.get("block_number", 0)
    }
    
    blockchain_records[trace_id] = record
    print(f"✅ Despacho registrado: {trace_id}")

def handle_stock_reserved(data: Dict[Any, Any], key: str):
    """Handler para eventos de reserva de stock en bodega"""
    print(f"🔒 Procesando reserva de stock: {key}")
    
    # Almacenar en IPFS
    ipfs_hash = ipfs_service.store_data(data["data"])
    
    # Registrar en blockchain
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    blockchain_result = smart_contract_service.record_trace(
        lote_id=f"STOCK-{key}",
        producto_id=data["data"].get("producto_id", "UNKNOWN"),
        ipfs_hash=ipfs_hash,
        event_type=2,  # RESERVED = 2
        private_key=private_key
    )
    
    # Crear registro
    trace_id = str(uuid.uuid4())
    record = {
        "trace_id": trace_id,
        "lote_id": f"STOCK-{key}",
        "event_type": "STOCK_RESERVED",
        "data": data["data"],
        "timestamp": datetime.now(),
        "blockchain_tx": blockchain_result["tx_hash"],
        "ipfs_hash": ipfs_hash,
        "status": blockchain_result["status"],
        "block_number": blockchain_result.get("block_number", 0)
    }
    
    blockchain_records[trace_id] = record
    print(f"✅ Reserva de stock registrada: {trace_id}")

def handle_stock_sold(data: Dict[Any, Any], key: str):
    """Handler para eventos de venta de stock en bodega"""
    print(f"💰 Procesando venta de stock: {key}")
    
    # Almacenar en IPFS
    ipfs_hash = ipfs_service.store_data(data["data"])
    
    # Registrar en blockchain
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    blockchain_result = smart_contract_service.record_trace(
        lote_id=f"STOCK-{key}",
        producto_id=data["data"].get("producto_id", "UNKNOWN"),
        ipfs_hash=ipfs_hash,
        event_type=5,  # SOLD = 5
        private_key=private_key
    )
    
    # Crear registro
    trace_id = str(uuid.uuid4())
    record = {
        "trace_id": trace_id,
        "lote_id": f"STOCK-{key}",
        "event_type": "STOCK_SOLD",
        "data": data["data"],
        "timestamp": datetime.now(),
        "blockchain_tx": blockchain_result["tx_hash"],
        "ipfs_hash": ipfs_hash,
        "status": blockchain_result["status"],
        "block_number": blockchain_result.get("block_number", 0)
    }
    
    blockchain_records[trace_id] = record
    print(f"✅ Venta de stock registrada: {trace_id}")

def handle_producto_created(data: Dict[Any, Any], key: str):
    """Handler para eventos de creación de producto"""
    print(f"📊 Procesando creación de producto: {key}")
    
    # 1. Almacenar datos en IPFS
    ipfs_hash = ipfs_service.store_data(data["data"])
    
    # 2. Crear registro en smart contract
    private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    blockchain_result = smart_contract_service.record_trace(
        lote_id=f"PRODUCTO-{key}",  # Usar prefijo para productos
        producto_id=key,
        ipfs_hash=ipfs_hash,
        event_type=0,  # CREATED = 0
        private_key=private_key
    )
    
    # 3. Crear registro de trazabilidad
    trace_id = str(uuid.uuid4())
    record = {
        "trace_id": trace_id,
        "lote_id": f"PRODUCTO-{key}",
        "event_type": "PRODUCTO_CREATED",
        "data": data["data"],
        "timestamp": datetime.now(),
        "blockchain_tx": blockchain_result["tx_hash"],
        "ipfs_hash": ipfs_hash,
        "status": blockchain_result["status"],
        "block_number": blockchain_result.get("block_number", 0)
    }
    
    blockchain_records[trace_id] = record
    print(f"✅ Producto registrado en blockchain: {trace_id}")
    print(f"🔗 TX: {blockchain_result['tx_hash']}")
    print(f"📁 IPFS: {ipfs_hash}")

def start_event_consumer():
    """Iniciar consumer de eventos en hilo separado"""
    print("🔍 DEBUG: start_event_consumer called")
    import os
    kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'host.docker.internal:9092')
    print(f"🔍 DEBUG: KAFKA_BOOTSTRAP_SERVERS env var = {os.getenv('KAFKA_BOOTSTRAP_SERVERS')}")
    print(f"🔍 DEBUG: Using kafka_servers = {kafka_servers}")
    kafka_client = KafkaEventClient(bootstrap_servers=kafka_servers)
    print(f"🔍 DEBUG: KafkaEventClient bootstrap_servers = {kafka_client.bootstrap_servers}")
    
    handlers = {
        "inventory.lote.created": handle_lote_created,
        "inventory.lote.updated": handle_lote_updated,
        "inventory.lote.reserved": handle_lote_reserved,
        "warehouse.lote.ingresado": handle_lote_ingresado,
        "warehouse.lote.despachado": handle_lote_despachado,
        "warehouse.stock.reserved": handle_stock_reserved,
        "warehouse.stock.sold": handle_stock_sold,
        "catalog.producto.created": handle_producto_created
    }
    
    # Iniciar consumo
    print(f"🔍 DEBUG: About to consume from {kafka_client.bootstrap_servers}")
    print(f"🔍 DEBUG: Topics to subscribe: {list(handlers.keys())}")
    kafka_client.consume_events(
        topics=list(handlers.keys()),
        group_id="traceability.blockchain-service",
        handlers=handlers
    )

# Inicializar consumer directamente
print("🔍 DEBUG: Iniciando consumer directamente...")
import os
kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'host.docker.internal:9092')
print(f"🔍 DEBUG: kafka_servers = {kafka_servers}")
consumer_thread = threading.Thread(target=start_event_consumer, daemon=True)
consumer_thread.start()
print(f"🚀 MS-Blockchain iniciado - Escuchando eventos en {kafka_servers}...")
print("📡 Topics suscritos:")
print("   - inventory.lote.created")
print("   - inventory.lote.updated")
print("   - inventory.lote.reserved")
print("   - warehouse.lote.ingresado")
print("   - warehouse.lote.despachado")
print("   - warehouse.stock.reserved")
print("   - warehouse.stock.sold")
print("   - catalog.producto.created")

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-Blockchain API activa", "timestamp": datetime.now()}

@app.get("/trace/lote/{lote_id}", tags=["Trazabilidad"])
async def get_lote_trace(lote_id: str):
    """Obtener historial de trazabilidad de un lote"""
    records = [r for r in blockchain_records.values() if r["lote_id"] == lote_id]
    
    if not records:
        raise HTTPException(status_code=404, detail="No se encontró trazabilidad para este lote")
    
    # Ordenar por timestamp
    records.sort(key=lambda x: x["timestamp"])
    
    return {
        "lote_id": lote_id,
        "total_records": len(records),
        "records": records
    }

@app.get("/trace/codigo-barras/{codigo_barras}", tags=["Trazabilidad"])
async def get_trace_by_barcode(codigo_barras: str):
    """Obtener trazabilidad por código de barras"""
    # Buscar todos los registros que contengan este producto
    records = []
    for record in blockchain_records.values():
        if record["data"].get("codigo_barras") == codigo_barras:
            records.append(record)
    
    if not records:
        raise HTTPException(status_code=404, detail="No se encontró trazabilidad para este código de barras")
    
    # Agrupar por lote
    lotes = {}
    for record in records:
        lote_id = record["lote_id"]
        if lote_id not in lotes:
            lotes[lote_id] = []
        lotes[lote_id].append(record)
    
    return {
        "codigo_barras": codigo_barras,
        "total_lotes": len(lotes),
        "lotes": lotes
    }

@app.get("/trace/tx/{tx_hash}", tags=["Trazabilidad"])
async def get_trace_by_tx(tx_hash: str):
    """Obtener registro por hash de transacción"""
    for record in blockchain_records.values():
        if record["blockchain_tx"] == tx_hash:
            return record
    
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@app.get("/trace/all", tags=["Trazabilidad"])
async def get_all_traces():
    """Obtener todos los registros de trazabilidad"""
    return {
        "total_records": len(blockchain_records),
        "records": list(blockchain_records.values())
    }

@app.get("/trace/verify/{trace_id}", tags=["Verificación"])
async def verify_trace(trace_id: str):
    """Verificar integridad de un registro específico"""
    if trace_id not in blockchain_records:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    record = blockchain_records[trace_id]
    
    # Verificar en blockchain
    blockchain_verification = blockchain_service.verify_transaction(record["blockchain_tx"])
    
    # Verificar datos en IPFS
    ipfs_data = ipfs_service.retrieve_data(record["ipfs_hash"])
    
    return {
        "trace_id": trace_id,
        "blockchain_verified": blockchain_verification["verified"],
        "ipfs_data_available": "error" not in ipfs_data,
        "blockchain_tx": record["blockchain_tx"],
        "ipfs_hash": record["ipfs_hash"],
        "timestamp": record["timestamp"],
        "status": record["status"],
        "block_number": record.get("block_number", 0)
    }

@app.get("/ipfs/info", tags=["IPFS"])
async def get_ipfs_info():
    """Obtener información del almacenamiento IPFS"""
    return ipfs_service.get_storage_info()

@app.get("/ipfs/{ipfs_hash}", tags=["IPFS"])
async def get_ipfs_data(ipfs_hash: str):
    """Recuperar datos desde IPFS"""
    data = ipfs_service.retrieve_data(ipfs_hash)
    if "error" in data:
        raise HTTPException(status_code=404, detail="Datos no encontrados en IPFS")
    return data

@app.post("/ipfs/upload", tags=["IPFS"])
async def upload_to_ipfs(data: dict):
    """Subir datos a IPFS y obtener hash"""
    ipfs_hash = ipfs_service.store_data(data)
    return {
        "ipfs_hash": ipfs_hash,
        "message": "Datos almacenados en IPFS",
        "timestamp": datetime.now()
    }

@app.post("/ipfs/test-integrity", tags=["IPFS"])
async def test_ipfs_integrity():
    """Probar integridad de IPFS - cambio de hash"""
    # Datos originales
    original_data = {
        "medicamento": "Paracetamol",
        "dosis": "500mg",
        "lote": "L001",
        "temperatura": "20°C"
    }
    
    # Datos modificados
    modified_data = {
        "medicamento": "Paracetamol",
        "dosis": "500mg",
        "lote": "L001",
        "temperatura": "25°C"  # Cambio aquí
    }
    
    hash1 = ipfs_service.store_data(original_data)
    hash2 = ipfs_service.store_data(modified_data)
    
    return {
        "original_hash": hash1,
        "modified_hash": hash2,
        "hashes_different": hash1 != hash2,
        "message": "Si los datos cambian, el hash cambia (integridad garantizada)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)