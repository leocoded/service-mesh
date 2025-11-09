#!/usr/bin/env python3
import requests
import json

def mostrar_trazabilidad():
    print("🔍 MOSTRANDO TRAZABILIDAD DEL SISTEMA")
    
    # 1. Crear lote
    print("\n1. 📦 Creando lote...")
    lote_data = {
        "numero_lote": "TRACE001",
        "id_producto": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "cantidad_inicial": 100,
        "fecha_vencimiento": "2024-12-31",
        "tipo_almacenamiento": "ambiente",
        "id_bodega": "2d3e9401-a9be-44e9-9bb3-42701891a06e"
    }
    
    response = requests.post("http://localhost:8090/lotes", json=lote_data)
    lote = response.json()
    lote_id = lote['id']
    print(f"✅ Lote creado: {lote_id}")
    
    # 2. Consultar el lote
    print(f"\n2. 🔍 Consultando lote {lote_id[:8]}...")
    response = requests.get(f"http://localhost:8090/lotes")
    lotes = response.json()
    mi_lote = next((l for l in lotes if l['id'] == lote_id), None)
    if mi_lote:
        print(f"✅ Lote encontrado: {mi_lote.get('numero_lote', 'N/A')}")
        print(f"   📊 Cantidad: {mi_lote['cantidad_disponible']}")
        print(f"   📅 Vencimiento: {mi_lote['fecha_vencimiento']}")
        print(f"   🆔 ID: {mi_lote['id'][:8]}...")
        print(f"   🏢 Bodega: {mi_lote['id_bodega'][:8]}...")
        print(f"   📦 Producto: {mi_lote['id_producto'][:8]}...")
    
    # 3. Reservar stock
    print(f"\n3. 🔒 Reservando stock...")
    response = requests.patch(f"http://localhost:8090/bodegas/{lote['id_bodega']}/reservar/30")
    reserva = response.json()
    print(f"✅ {reserva['message']}")
    
    # 4. Subir evidencia a IPFS
    print(f"\n4. 📁 Creando evidencia en IPFS...")
    evidencia = {
        "operacion": "RESERVA_STOCK",
        "lote_id": lote_id,
        "cantidad_reservada": 30,
        "operador": "Sistema Demo",
        "timestamp": "2024-11-08T11:45:00Z"
    }
    
    response = requests.post("http://localhost:8098/ipfs/upload", json=evidencia)
    ipfs_result = response.json()
    print(f"✅ Evidencia en IPFS: {ipfs_result['ipfs_hash']}")
    
    # 5. Mostrar trazabilidad completa
    print(f"\n🔗 TRAZABILIDAD COMPLETA:")
    print(f"   📦 Lote: {lote_id}")
    print(f"   🏢 Bodega: {lote['id_bodega']}")
    print(f"   📊 Producto: {lote['id_producto']}")
    print(f"   📁 Evidencia IPFS: {ipfs_result['ipfs_hash']}")
    print(f"   📡 Evento Kafka: inventory.lote.created")
    
    print(f"\n📋 PARA MOSTRAR EN VIDEO:")
    print(f"   1. Ve a Kafka UI y muestra el evento")
    print(f"   2. Ve a Pinata y busca: {ipfs_result['ipfs_hash']}")
    print(f"   3. Explica que cada operación deja rastro")
    print(f"   4. Muestra que el lote se puede rastrear por ID")

if __name__ == "__main__":
    mostrar_trazabilidad()