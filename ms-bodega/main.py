from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import uuid
import os
import json
from models import BodegaCreate, BodegaUpdate, BodegaResponse, BodegaFilter

app = FastAPI(
    title="MS-Bodega API",
    description="Microservicio para gestión de bodegas y ubicaciones geográficas",
    version="1.0.0"
)

# Simulación de base de datos en memoria
bodegas_db = {}

def cargar_bodegas_desde_json():
    ruta = os.path.join(os.path.dirname(__file__), "test_data.json")
    if not os.path.exists(ruta):
        return {}
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    bodegas = {}
    for bodega in data:
        # Ajustar a lo definido en models.py (BodegaResponse)
        bodega_id = bodega.get("id") or str(uuid.uuid4())
        bodegas[bodega_id] = {
            "id": bodega_id,
            "nombre": bodega["nombre"],
            "capacidad": bodega["capacidad"],
            "ubicacion_geografica": bodega["ubicacion_geografica"],
            "cantidad_disponible": bodega.get("cantidad_disponible", bodega["capacidad"]),
            "cantidad_reservada": bodega.get("cantidad_reservada", 0),
            "cantidad_vendida": bodega.get("cantidad_vendida", 0),
            "id_producto": bodega["id_producto"],
            "fecha_creacion": datetime.now(),
            "fecha_actualizacion": datetime.now()
        }
    return bodegas

bodegas_db = cargar_bodegas_desde_json()

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-Bodega API activa", "timestamp": datetime.now()}

@app.post("/bodegas", response_model=BodegaResponse, tags=["Bodegas"])
async def crear_bodega(bodega: BodegaCreate):
    """Crear una nueva bodega"""
    bodega_id = str(uuid.uuid4())
    now = datetime.now()
    
    nueva_bodega = {
        "id": bodega_id,
        "nombre": bodega.nombre,
        "capacidad": bodega.capacidad,
        "ubicacion_geografica": bodega.ubicacion_geografica.dict(),
        "cantidad_disponible": bodega.capacidad,  # Inicialmente toda la capacidad está disponible
        "cantidad_reservada": 0,
        "cantidad_vendida": 0,
        "id_producto": bodega.id_producto,
        "fecha_creacion": now,
        "fecha_actualizacion": now
    }
    
    bodegas_db[bodega_id] = nueva_bodega
    return BodegaResponse(**nueva_bodega)

@app.get("/bodegas", response_model=List[BodegaResponse], tags=["Bodegas"])
async def listar_bodegas(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    id_producto: Optional[str] = Query(None, description="Filtrar por ID de producto"),
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    capacidad_min: Optional[int] = Query(None, description="Capacidad mínima"),
    capacidad_max: Optional[int] = Query(None, description="Capacidad máxima")
):
    """Listar todas las bodegas con filtros opcionales"""
    bodegas = list(bodegas_db.values())
    
    # Aplicar filtros
    if nombre:
        bodegas = [b for b in bodegas if nombre.lower() in b["nombre"].lower()]
    if id_producto:
        bodegas = [b for b in bodegas if b["id_producto"] == id_producto]
    if ciudad:
        bodegas = [b for b in bodegas if ciudad.lower() in b["ubicacion_geografica"]["ciudad"].lower()]
    if capacidad_min:
        bodegas = [b for b in bodegas if b["capacidad"] >= capacidad_min]
    if capacidad_max:
        bodegas = [b for b in bodegas if b["capacidad"] <= capacidad_max]
    
    return [BodegaResponse(**bodega) for bodega in bodegas]

@app.get("/bodegas/{bodega_id}", response_model=BodegaResponse, tags=["Bodegas"])
async def obtener_bodega(bodega_id: str):
    """Obtener una bodega específica por ID"""
    if bodega_id not in bodegas_db:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    
    return BodegaResponse(**bodegas_db[bodega_id])

@app.put("/bodegas/{bodega_id}", response_model=BodegaResponse, tags=["Bodegas"])
async def actualizar_bodega(bodega_id: str, bodega_update: BodegaUpdate):
    """Actualizar una bodega existente"""
    if bodega_id not in bodegas_db:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    
    bodega = bodegas_db[bodega_id]
    update_data = bodega_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "ubicacion_geografica" and value:
            bodega[field] = value.dict()
        else:
            bodega[field] = value
    
    bodega["fecha_actualizacion"] = datetime.now()
    bodegas_db[bodega_id] = bodega
    
    return BodegaResponse(**bodega)

@app.delete("/bodegas/{bodega_id}", tags=["Bodegas"])
async def eliminar_bodega(bodega_id: str):
    """Eliminar una bodega"""
    if bodega_id not in bodegas_db:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    
    del bodegas_db[bodega_id]
    return {"message": f"Bodega {bodega_id} eliminada exitosamente"}

@app.get("/bodegas/{bodega_id}/disponibilidad", tags=["Disponibilidad"])
async def consultar_disponibilidad(bodega_id: str):
    """Consultar disponibilidad de una bodega específica"""
    if bodega_id not in bodegas_db:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    
    bodega = bodegas_db[bodega_id]
    return {
        "bodega_id": bodega_id,
        "nombre": bodega["nombre"],
        "capacidad_total": bodega["capacidad"],
        "cantidad_disponible": bodega["cantidad_disponible"],
        "cantidad_reservada": bodega["cantidad_reservada"],
        "cantidad_vendida": bodega["cantidad_vendida"],
        "porcentaje_ocupacion": round((bodega["capacidad"] - bodega["cantidad_disponible"]) / bodega["capacidad"] * 100, 2)
    }

@app.patch("/bodegas/{bodega_id}/reservar/{cantidad}", tags=["Operaciones"])
async def reservar_cantidad(bodega_id: str, cantidad: int):
    """Reservar una cantidad específica en la bodega"""
    if bodega_id not in bodegas_db:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    
    bodega = bodegas_db[bodega_id]
    
    if bodega["cantidad_disponible"] < cantidad:
        raise HTTPException(
            status_code=400, 
            detail=f"Cantidad no disponible. Disponible: {bodega['cantidad_disponible']}"
        )
    
    bodega["cantidad_disponible"] -= cantidad
    bodega["cantidad_reservada"] += cantidad
    bodega["fecha_actualizacion"] = datetime.now()
    
    return {
        "message": f"Se reservaron {cantidad} unidades",
        "cantidad_disponible": bodega["cantidad_disponible"],
        "cantidad_reservada": bodega["cantidad_reservada"]
    }

@app.patch("/bodegas/{bodega_id}/vender/{cantidad}", tags=["Operaciones"])
async def vender_cantidad(bodega_id: str, cantidad: int):
    """Vender una cantidad específica (debe estar previamente reservada)"""
    if bodega_id not in bodegas_db:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    
    bodega = bodegas_db[bodega_id]
    
    if bodega["cantidad_reservada"] < cantidad:
        raise HTTPException(
            status_code=400, 
            detail=f"Cantidad no reservada suficiente. Reservada: {bodega['cantidad_reservada']}"
        )
    
    bodega["cantidad_reservada"] -= cantidad
    bodega["cantidad_vendida"] += cantidad
    bodega["fecha_actualizacion"] = datetime.now()
    
    return {
        "message": f"Se vendieron {cantidad} unidades",
        "cantidad_reservada": bodega["cantidad_reservada"],
        "cantidad_vendida": bodega["cantidad_vendida"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
