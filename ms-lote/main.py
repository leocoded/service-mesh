from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime, date, timedelta
import uuid
import os
import json
from models import (
    LoteCreate, LoteUpdate, LoteResponse, LoteFilter, 
    AlertaVencimiento, TipoAlmacenamiento
)

app = FastAPI(
    title="MS-Lote API",
    description="Microservicio para gestión de lotes y almacenamiento",
    version="1.0.0"
)

# Simulación de base de datos en memoria
lotes_db = {}

def esta_vencido(fecha_vencimiento: date) -> bool:
    """Verificar si un lote está vencido"""
    return fecha_vencimiento < date.today()

def cargar_lotes_desde_json():
    ruta = os.path.join(os.path.dirname(__file__), "test_data.json")
    if not os.path.exists(ruta):
        return {}
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    lotes = {}
    for lote in data:
        lote_id = lote.get("id") or str(uuid.uuid4())
        lotes[lote_id] = {
            "id": lote_id,
            "fecha_vencimiento": date.fromisoformat(lote["fecha_vencimiento"]) if isinstance(lote["fecha_vencimiento"], str) else lote["fecha_vencimiento"],
            "tipo_almacenamiento": lote["tipo_almacenamiento"],
            "cantidad_inicial": lote["cantidad_inicial"],
            "cantidad_disponible": lote.get("cantidad_disponible", lote["cantidad_inicial"]),
            "cantidad_reservada": lote.get("cantidad_reservada", 0),
            "cantidad_vendida": lote.get("cantidad_vendida", 0),
            "id_producto": lote["id_producto"],
            "id_bodega": lote["id_bodega"],
            "temperatura_optima": lote["temperatura_optima"],
            "humedad_optima": lote["humedad_optima"],
            "fecha_creacion": datetime.now(),
            "fecha_actualizacion": datetime.now(),
            "esta_vencido": esta_vencido(date.fromisoformat(lote["fecha_vencimiento"]) if isinstance(lote["fecha_vencimiento"], str) else lote["fecha_vencimiento"])
        }
    return lotes

lotes_db = cargar_lotes_desde_json()

def calcular_dias_vencimiento(fecha_vencimiento: date) -> int:
    """Calcular días para el vencimiento"""
    return (fecha_vencimiento - date.today()).days



@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-Lote API activa", "timestamp": datetime.now()}

@app.post("/lotes", response_model=LoteResponse, tags=["Lotes"])
async def crear_lote(lote: LoteCreate):
    """Crear un nuevo lote"""
    lote_id = str(uuid.uuid4())
    now = datetime.now()
    
    nuevo_lote = {
        "id": lote_id,
        "fecha_vencimiento": lote.fecha_vencimiento,
        "tipo_almacenamiento": lote.tipo_almacenamiento,
        "cantidad_inicial": lote.cantidad_inicial,
        "cantidad_disponible": lote.cantidad_inicial,
        "cantidad_reservada": 0,
        "cantidad_vendida": 0,
        "id_producto": lote.id_producto,
        "id_bodega": lote.id_bodega,
        "temperatura_optima": lote.temperatura_optima,
        "humedad_optima": lote.humedad_optima,
        "fecha_creacion": now,
        "fecha_actualizacion": now,
        "esta_vencido": esta_vencido(lote.fecha_vencimiento)
    }
    
    lotes_db[lote_id] = nuevo_lote
    return LoteResponse(**nuevo_lote)

@app.get("/lotes", response_model=List[LoteResponse], tags=["Lotes"])
async def listar_lotes(
    id_producto: Optional[str] = Query(None, description="Filtrar por ID de producto"),
    id_bodega: Optional[str] = Query(None, description="Filtrar por ID de bodega"),
    tipo_almacenamiento: Optional[TipoAlmacenamiento] = Query(None, description="Filtrar por tipo de almacenamiento"),
    vencimiento_desde: Optional[date] = Query(None, description="Fecha de vencimiento desde"),
    vencimiento_hasta: Optional[date] = Query(None, description="Fecha de vencimiento hasta"),
    solo_disponibles: Optional[bool] = Query(None, description="Solo lotes con cantidad disponible > 0"),
    solo_vencidos: Optional[bool] = Query(None, description="Solo lotes vencidos")
):
    """Listar todos los lotes con filtros opcionales"""
    lotes = list(lotes_db.values())
    
    # Actualizar estado de vencimiento
    for lote in lotes:
        lote["esta_vencido"] = esta_vencido(lote["fecha_vencimiento"])
    
    # Aplicar filtros
    if id_producto:
        lotes = [l for l in lotes if l["id_producto"] == id_producto]
    if id_bodega:
        lotes = [l for l in lotes if l["id_bodega"] == id_bodega]
    if tipo_almacenamiento:
        lotes = [l for l in lotes if l["tipo_almacenamiento"] == tipo_almacenamiento]
    if vencimiento_desde:
        lotes = [l for l in lotes if l["fecha_vencimiento"] >= vencimiento_desde]
    if vencimiento_hasta:
        lotes = [l for l in lotes if l["fecha_vencimiento"] <= vencimiento_hasta]
    if solo_disponibles:
        lotes = [l for l in lotes if l["cantidad_disponible"] > 0]
    if solo_vencidos:
        lotes = [l for l in lotes if l["esta_vencido"]]
    
    return [LoteResponse(**lote) for lote in lotes]

@app.get("/lotes/{lote_id}", response_model=LoteResponse, tags=["Lotes"])
async def obtener_lote(lote_id: str):
    """Obtener un lote específico por ID"""
    if lote_id not in lotes_db:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    lote = lotes_db[lote_id]
    lote["esta_vencido"] = esta_vencido(lote["fecha_vencimiento"])
    return LoteResponse(**lote)

@app.put("/lotes/{lote_id}", response_model=LoteResponse, tags=["Lotes"])
async def actualizar_lote(lote_id: str, lote_update: LoteUpdate):
    """Actualizar un lote existente"""
    if lote_id not in lotes_db:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    lote = lotes_db[lote_id]
    update_data = lote_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        lote[field] = value
    
    lote["fecha_actualizacion"] = datetime.now()
    lote["esta_vencido"] = esta_vencido(lote["fecha_vencimiento"])
    lotes_db[lote_id] = lote
    
    return LoteResponse(**lote)

@app.delete("/lotes/{lote_id}", tags=["Lotes"])
async def eliminar_lote(lote_id: str):
    """Eliminar un lote"""
    if lote_id not in lotes_db:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    del lotes_db[lote_id]
    return {"message": f"Lote {lote_id} eliminado exitosamente"}

@app.get("/lotes/{lote_id}/disponibilidad", tags=["Disponibilidad"])
async def consultar_disponibilidad_lote(lote_id: str):
    """Consultar disponibilidad de un lote específico"""
    if lote_id not in lotes_db:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    lote = lotes_db[lote_id]
    dias_vencimiento = calcular_dias_vencimiento(lote["fecha_vencimiento"])
    
    return {
        "lote_id": lote_id,
        "cantidad_inicial": lote["cantidad_inicial"],
        "cantidad_disponible": lote["cantidad_disponible"],
        "cantidad_reservada": lote["cantidad_reservada"],
        "cantidad_vendida": lote["cantidad_vendida"],
        "porcentaje_disponible": round((lote["cantidad_disponible"] / lote["cantidad_inicial"]) * 100, 2),
        "dias_para_vencer": dias_vencimiento,
        "esta_vencido": esta_vencido(lote["fecha_vencimiento"])
    }

@app.patch("/lotes/{lote_id}/reservar/{cantidad}", tags=["Operaciones"])
async def reservar_cantidad_lote(lote_id: str, cantidad: int):
    """Reservar una cantidad específica del lote"""
    if lote_id not in lotes_db:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    
    lote = lotes_db[lote_id]
    
    if esta_vencido(lote["fecha_vencimiento"]):
        raise HTTPException(status_code=400, detail="No se puede reservar de un lote vencido")
    
    if lote["cantidad_disponible"] < cantidad:
        raise HTTPException(
            status_code=400, 
            detail=f"Cantidad no disponible. Disponible: {lote['cantidad_disponible']}"
        )
    
    lote["cantidad_disponible"] -= cantidad
    lote["cantidad_reservada"] += cantidad
    lote["fecha_actualizacion"] = datetime.now()
    
    return {
        "message": f"Se reservaron {cantidad} unidades del lote",
        "cantidad_disponible": lote["cantidad_disponible"],
        "cantidad_reservada": lote["cantidad_reservada"]
    }

@app.get("/alertas/vencimiento", response_model=List[AlertaVencimiento], tags=["Alertas"])
async def obtener_alertas_vencimiento(
    dias_anticipacion: int = Query(30, description="Días de anticipación para alerta")
):
    """Obtener alertas de lotes próximos a vencer"""
    alertas = []
    fecha_limite = date.today() + timedelta(days=dias_anticipacion)
    
    for lote_id, lote in lotes_db.items():
        if (lote["fecha_vencimiento"] <= fecha_limite and 
            lote["cantidad_disponible"] > 0 and 
            not esta_vencido(lote["fecha_vencimiento"])):
            
            dias_vencimiento = calcular_dias_vencimiento(lote["fecha_vencimiento"])
            
            # Determinar prioridad
            if dias_vencimiento <= 7:
                prioridad = "ALTA"
            elif dias_vencimiento <= 15:
                prioridad = "MEDIA"
            else:
                prioridad = "BAJA"
            
            alertas.append(AlertaVencimiento(
                id_lote=lote_id,
                dias_para_vencer=dias_vencimiento,
                cantidad_disponible=lote["cantidad_disponible"],
                prioridad=prioridad
            ))
    
    # Ordenar por prioridad y días de vencimiento
    prioridad_orden = {"ALTA": 1, "MEDIA": 2, "BAJA": 3}
    alertas.sort(key=lambda x: (prioridad_orden[x.prioridad], x.dias_para_vencer))
    
    return alertas

@app.get("/lotes/vencidos", response_model=List[LoteResponse], tags=["Consultas"])
async def obtener_lotes_vencidos():
    """Obtener todos los lotes vencidos"""
    lotes_vencidos = []
    
    for lote_id, lote in lotes_db.items():
        if esta_vencido(lote["fecha_vencimiento"]):
            lote["esta_vencido"] = True
            lotes_vencidos.append(LoteResponse(**lote))
    
    return lotes_vencidos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
