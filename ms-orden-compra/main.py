from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
import uuid
from models import (
    OrdenCompraCreate, ItemOrdenCreate, OrdenCompraUpdate,
    OrdenCompraResponse, ItemOrdenResponse, OrdenCompraFilter,
    ResumenOrdenesProveedor, AlertaOrden,
    EstadoOrden, TipoOrden
)

app = FastAPI(
    title="MS-OrdenCompra API",
    description="Microservicio para gestión de órdenes de compra",
    version="1.0.0"
)

# Simulación de base de datos en memoria
ordenes_db = {}
items_orden_db = {}  # {orden_id: [items]}
contador_orden = 1

def generar_numero_orden() -> str:
    """Generar número de orden secuencial"""
    global contador_orden
    numero = f"OC{contador_orden:06d}"
    contador_orden += 1
    return numero

def calcular_totales_orden(orden_id: str) -> dict:
    """Calcular totales de una orden"""
    items = items_orden_db.get(orden_id, [])
    
    subtotal = sum(item["total_item"] for item in items)
    descuento_total = sum(item["precio_unitario"] * item["cantidad"] * item["descuento_porcentaje"] / 100 for item in items)
    impuestos = subtotal * Decimal("0.19")  # IVA 19%
    total = subtotal + impuestos
    
    return {
        "subtotal": subtotal,
        "descuento_total": descuento_total,
        "impuestos": impuestos,
        "total": total
    }

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-OrdenCompra API activa", "timestamp": datetime.now()}

@app.post("/ordenes", response_model=OrdenCompraResponse, tags=["Órdenes"])
async def crear_orden(orden: OrdenCompraCreate):
    """Crear una nueva orden de compra"""
    orden_id = str(uuid.uuid4())
    now = datetime.now()
    
    nueva_orden = {
        "id": orden_id,
        "numero_orden": generar_numero_orden(),
        "id_proveedor": orden.id_proveedor,
        "tipo_orden": orden.tipo_orden,
        "estado": EstadoOrden.DRAFT,
        "fecha_orden": date.today(),
        "fecha_requerida": orden.fecha_requerida,
        "observaciones": orden.observaciones,
        "direccion_entrega": orden.direccion_entrega,
        "fecha_creacion": now,
        "fecha_actualizacion": now
    }
    
    # Inicializar items vacíos
    items_orden_db[orden_id] = []
    
    # Calcular totales iniciales (serán 0)
    totales = calcular_totales_orden(orden_id)
    nueva_orden.update(totales)
    
    ordenes_db[orden_id] = nueva_orden
    return OrdenCompraResponse(**nueva_orden, items=[])

@app.post("/ordenes/{orden_id}/items", response_model=ItemOrdenResponse, tags=["Items"])
async def agregar_item_orden(orden_id: str, item: ItemOrdenCreate):
    """Agregar un item a una orden de compra"""
    if orden_id not in ordenes_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden = ordenes_db[orden_id]
    if orden["estado"] not in [EstadoOrden.DRAFT, EstadoOrden.PENDING]:
        raise HTTPException(status_code=400, detail="No se pueden modificar items en una orden en este estado")
    
    item_id = str(uuid.uuid4())
    subtotal = item.precio_unitario * item.cantidad
    descuento = subtotal * (item.descuento_porcentaje / 100)
    total_item = subtotal - descuento
    
    nuevo_item = {
        "id": item_id,
        "id_producto": item.id_producto,
        "cantidad": item.cantidad,
        "precio_unitario": item.precio_unitario,
        "descuento_porcentaje": item.descuento_porcentaje,
        "subtotal": subtotal,
        "total_item": total_item
    }
    
    # Agregar item a la orden
    if orden_id not in items_orden_db:
        items_orden_db[orden_id] = []
    items_orden_db[orden_id].append(nuevo_item)
    
    # Actualizar totales de la orden
    totales = calcular_totales_orden(orden_id)
    orden.update(totales)
    orden["fecha_actualizacion"] = datetime.now()
    
    return ItemOrdenResponse(**nuevo_item)

@app.get("/ordenes", response_model=List[OrdenCompraResponse], tags=["Órdenes"])
async def listar_ordenes(
    id_proveedor: Optional[str] = Query(None, description="Filtrar por ID de proveedor"),
    estado: Optional[EstadoOrden] = Query(None, description="Filtrar por estado"),
    tipo_orden: Optional[TipoOrden] = Query(None, description="Filtrar por tipo de orden"),
    fecha_desde: Optional[date] = Query(None, description="Fecha de orden desde"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha de orden hasta"),
    monto_min: Optional[Decimal] = Query(None, description="Monto mínimo"),
    monto_max: Optional[Decimal] = Query(None, description="Monto máximo")
):
    """Listar todas las órdenes con filtros opcionales"""
    ordenes = list(ordenes_db.values())
    
    # Aplicar filtros
    if id_proveedor:
        ordenes = [o for o in ordenes if o["id_proveedor"] == id_proveedor]
    if estado:
        ordenes = [o for o in ordenes if o["estado"] == estado]
    if tipo_orden:
        ordenes = [o for o in ordenes if o["tipo_orden"] == tipo_orden]
    if fecha_desde:
        ordenes = [o for o in ordenes if o["fecha_orden"] >= fecha_desde]
    if fecha_hasta:
        ordenes = [o for o in ordenes if o["fecha_orden"] <= fecha_hasta]
    if monto_min:
        ordenes = [o for o in ordenes if o["total"] >= monto_min]
    if monto_max:
        ordenes = [o for o in ordenes if o["total"] <= monto_max]
    
    # Agregar items a cada orden
    ordenes_response = []
    for orden in ordenes:
        items = items_orden_db.get(orden["id"], [])
        items_response = [ItemOrdenResponse(**item) for item in items]
        ordenes_response.append(OrdenCompraResponse(**orden, items=items_response))
    
    return ordenes_response

@app.get("/ordenes/{orden_id}", response_model=OrdenCompraResponse, tags=["Órdenes"])
async def obtener_orden(orden_id: str):
    """Obtener una orden específica por ID"""
    if orden_id not in ordenes_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden = ordenes_db[orden_id]
    items = items_orden_db.get(orden_id, [])
    items_response = [ItemOrdenResponse(**item) for item in items]
    
    return OrdenCompraResponse(**orden, items=items_response)

@app.put("/ordenes/{orden_id}", response_model=OrdenCompraResponse, tags=["Órdenes"])
async def actualizar_orden(orden_id: str, orden_update: OrdenCompraUpdate):
    """Actualizar una orden existente"""
    if orden_id not in ordenes_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden = ordenes_db[orden_id]
    update_data = orden_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        orden[field] = value
    
    orden["fecha_actualizacion"] = datetime.now()
    
    items = items_orden_db.get(orden_id, [])
    items_response = [ItemOrdenResponse(**item) for item in items]
    
    return OrdenCompraResponse(**orden, items=items_response)

@app.delete("/ordenes/{orden_id}", tags=["Órdenes"])
async def eliminar_orden(orden_id: str):
    """Eliminar una orden (solo si está en borrador)"""
    if orden_id not in ordenes_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden = ordenes_db[orden_id]
    if orden["estado"] != EstadoOrden.DRAFT:
        raise HTTPException(status_code=400, detail="Solo se pueden eliminar órdenes en borrador")
    
    del ordenes_db[orden_id]
    if orden_id in items_orden_db:
        del items_orden_db[orden_id]
    
    return {"message": f"Orden {orden_id} eliminada exitosamente"}

@app.patch("/ordenes/{orden_id}/aprobar", tags=["Estados"])
async def aprobar_orden(orden_id: str):
    """Aprobar una orden de compra"""
    if orden_id not in ordenes_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden = ordenes_db[orden_id]
    if orden["estado"] not in [EstadoOrden.DRAFT, EstadoOrden.PENDING]:
        raise HTTPException(status_code=400, detail="La orden no puede ser aprobada en su estado actual")
    
    orden["estado"] = EstadoOrden.APPROVED
    orden["fecha_aprobacion"] = datetime.now()
    orden["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Orden {orden['numero_orden']} aprobada exitosamente"}

@app.patch("/ordenes/{orden_id}/enviar", tags=["Estados"])
async def enviar_orden(orden_id: str):
    """Enviar una orden de compra al proveedor"""
    if orden_id not in ordenes_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden = ordenes_db[orden_id]
    if orden["estado"] != EstadoOrden.APPROVED:
        raise HTTPException(status_code=400, detail="La orden debe estar aprobada para ser enviada")
    
    orden["estado"] = EstadoOrden.SENT
    orden["fecha_envio"] = datetime.now()
    orden["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Orden {orden['numero_orden']} enviada exitosamente"}

@app.patch("/ordenes/{orden_id}/recibir", tags=["Estados"])
async def recibir_orden(orden_id: str):
    """Marcar una orden como recibida"""
    if orden_id not in ordenes_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden = ordenes_db[orden_id]
    if orden["estado"] != EstadoOrden.SENT:
        raise HTTPException(status_code=400, detail="La orden debe estar enviada para ser recibida")
    
    orden["estado"] = EstadoOrden.RECEIVED
    orden["fecha_recepcion"] = datetime.now()
    orden["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Orden {orden['numero_orden']} recibida exitosamente"}

@app.patch("/ordenes/{orden_id}/cancelar", tags=["Estados"])
async def cancelar_orden(orden_id: str, motivo: Optional[str] = None):
    """Cancelar una orden de compra"""
    if orden_id not in ordenes_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden = ordenes_db[orden_id]
    if orden["estado"] == EstadoOrden.RECEIVED:
        raise HTTPException(status_code=400, detail="No se puede cancelar una orden ya recibida")
    
    orden["estado"] = EstadoOrden.CANCELLED
    if motivo:
        orden["observaciones"] = f"{orden.get('observaciones', '')} - CANCELADA: {motivo}".strip(" -")
    orden["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Orden {orden['numero_orden']} cancelada exitosamente"}

@app.get("/proveedores/{id_proveedor}/ordenes/resumen", response_model=ResumenOrdenesProveedor, tags=["Reportes"])
async def obtener_resumen_proveedor(id_proveedor: str):
    """Obtener resumen de órdenes de un proveedor específico"""
    ordenes_proveedor = [o for o in ordenes_db.values() if o["id_proveedor"] == id_proveedor]
    
    if not ordenes_proveedor:
        raise HTTPException(status_code=404, detail="No se encontraron órdenes para este proveedor")
    
    total_ordenes = len(ordenes_proveedor)
    ordenes_pendientes = len([o for o in ordenes_proveedor if o["estado"] in [EstadoOrden.PENDING, EstadoOrden.APPROVED, EstadoOrden.SENT]])
    ordenes_completadas = len([o for o in ordenes_proveedor if o["estado"] == EstadoOrden.RECEIVED])
    monto_total = sum(o["total"] for o in ordenes_proveedor)
    
    return ResumenOrdenesProveedor(
        id_proveedor=id_proveedor,
        total_ordenes=total_ordenes,
        ordenes_pendientes=ordenes_pendientes,
        ordenes_completadas=ordenes_completadas,
        monto_total=monto_total
    )

@app.get("/alertas/ordenes", response_model=List[AlertaOrden], tags=["Alertas"])
async def obtener_alertas_ordenes():
    """Obtener alertas de órdenes de compra"""
    alertas = []
    hoy = date.today()
    
    for orden in ordenes_db.values():
        # Alerta por retraso en entrega
        if (orden["estado"] == EstadoOrden.SENT and 
            orden["fecha_requerida"] < hoy):
            dias_retraso = (hoy - orden["fecha_requerida"]).days
            criticidad = "ALTA" if dias_retraso > 7 else "MEDIA"
            
            alertas.append(AlertaOrden(
                id_orden=orden["id"],
                numero_orden=orden["numero_orden"],
                tipo_alerta="RETRASO_ENTREGA",
                dias_retraso=dias_retraso,
                criticidad=criticidad,
                descripcion=f"Orden vencida hace {dias_retraso} días",
                fecha_alerta=datetime.now()
            ))
        
        # Alerta por aprobación pendiente
        elif (orden["estado"] == EstadoOrden.PENDING and 
              (hoy - orden["fecha_orden"]).days > 3):
            alertas.append(AlertaOrden(
                id_orden=orden["id"],
                numero_orden=orden["numero_orden"],
                tipo_alerta="APROBACION_PENDIENTE",
                criticidad="MEDIA",
                descripcion="Orden pendiente de aprobación por más de 3 días",
                fecha_alerta=datetime.now()
            ))
    
    return alertas

@app.get("/estadisticas/ordenes", tags=["Estadísticas"])
async def obtener_estadisticas_ordenes():
    """Obtener estadísticas generales de órdenes"""
    if not ordenes_db:
        return {"message": "No hay órdenes registradas"}
    
    ordenes = list(ordenes_db.values())
    
    # Estadísticas por estado
    estados_count = {}
    for orden in ordenes:
        estado = orden["estado"]
        estados_count[estado] = estados_count.get(estado, 0) + 1
    
    # Estadísticas por tipo
    tipos_count = {}
    for orden in ordenes:
        tipo = orden["tipo_orden"]
        tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
    
    # Montos
    monto_total = sum(o["total"] for o in ordenes)
    monto_promedio = monto_total / len(ordenes)
    
    return {
        "total_ordenes": len(ordenes),
        "monto_total": monto_total,
        "monto_promedio": round(float(monto_promedio), 2),
        "ordenes_por_estado": estados_count,
        "ordenes_por_tipo": tipos_count,
        "fecha_consulta": datetime.now()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
