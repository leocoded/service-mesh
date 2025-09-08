from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime, date, timedelta
import uuid
import os
import json
from models import (
    ProyeccionDemandaCreate, ProyeccionDemandaUpdate, ProyeccionDemandaResponse,
    DetalleProyeccion, ProyeccionAgregada, AlertaDemanda,
    TipoProyeccion, EstadoProyeccion
)

app = FastAPI(
    title="MS-ProyeccionDemanda API",
    description="Microservicio para proyección de demanda de productos",
    version="1.0.0"
)

# Simulación de base de datos en memoria
proyecciones_db = {}

def cargar_proyecciones_desde_json():
    ruta = os.path.join(os.path.dirname(__file__), "test_data.json")
    if not os.path.exists(ruta):
        return {}
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    proyecciones = {}
    for proy in data:
        proy_id = proy.get("id") or str(uuid.uuid4())
        proyecciones[proy_id] = {
            "id": proy_id,
            "id_producto": proy["id_producto"],
            "fecha_inicio": date.fromisoformat(proy["fecha_inicio"]) if isinstance(proy["fecha_inicio"], str) else proy["fecha_inicio"],
            "fecha_fin": date.fromisoformat(proy["fecha_fin"]) if isinstance(proy["fecha_fin"], str) else proy["fecha_fin"],
            "tipo_proyeccion": proy["tipo_proyeccion"],
            "demanda_estimada": proy["demanda_estimada"],
            "unidades": proy["unidades"],
            "metodologia": proy["metodologia"],
            "factores_considerados": proy.get("factores_considerados", []),
            "confianza_porcentaje": proy["confianza_porcentaje"],
            "estado": proy.get("estado", EstadoProyeccion.DRAFT),
            "fecha_creacion": datetime.now(),
            "fecha_actualizacion": datetime.now()
        }
    return proyecciones

proyecciones_db = cargar_proyecciones_desde_json()

def calcular_metricas_proyeccion(proyeccion: dict) -> dict:
    """Calcular métricas derivadas de la proyección"""
    fecha_inicio = proyeccion["fecha_inicio"]
    fecha_fin = proyeccion["fecha_fin"]
    demanda_estimada = proyeccion["demanda_estimada"]
    
    dias_vigencia = (fecha_fin - fecha_inicio).days + 1
    demanda_diaria = demanda_estimada / dias_vigencia if dias_vigencia > 0 else 0
    demanda_semanal = demanda_diaria * 7
    demanda_mensual = demanda_diaria * 30
    
    proyeccion.update({
        "dias_vigencia": dias_vigencia,
        "demanda_diaria": round(demanda_diaria, 2),
        "demanda_semanal": round(demanda_semanal, 2),
        "demanda_mensual": round(demanda_mensual, 2)
    })
    
    return proyeccion

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-ProyeccionDemanda API activa", "timestamp": datetime.now()}

@app.post("/proyecciones", response_model=ProyeccionDemandaResponse, tags=["Proyecciones"])
async def crear_proyeccion(proyeccion: ProyeccionDemandaCreate):
    """Crear una nueva proyección de demanda"""
    proyeccion_id = str(uuid.uuid4())
    now = datetime.now()
    
    nueva_proyeccion = {
        "id": proyeccion_id,
        "id_producto": proyeccion.id_producto,
        "fecha_inicio": proyeccion.fecha_inicio,
        "fecha_fin": proyeccion.fecha_fin,
        "tipo_proyeccion": proyeccion.tipo_proyeccion,
        "demanda_estimada": proyeccion.demanda_estimada,
        "unidades": proyeccion.unidades,
        "metodologia": proyeccion.metodologia,
        "factores_considerados": proyeccion.factores_considerados or [],
        "confianza_porcentaje": proyeccion.confianza_porcentaje,
        "estado": EstadoProyeccion.DRAFT,
        "fecha_creacion": now,
        "fecha_actualizacion": now
    }
    
    nueva_proyeccion = calcular_metricas_proyeccion(nueva_proyeccion)
    proyecciones_db[proyeccion_id] = nueva_proyeccion
    
    return ProyeccionDemandaResponse(**nueva_proyeccion)

@app.get("/proyecciones", response_model=List[ProyeccionDemandaResponse], tags=["Proyecciones"])
async def listar_proyecciones(
    id_producto: Optional[str] = Query(None, description="Filtrar por ID de producto"),
    tipo_proyeccion: Optional[TipoProyeccion] = Query(None, description="Filtrar por tipo de proyección"),
    estado: Optional[EstadoProyeccion] = Query(None, description="Filtrar por estado"),
    fecha_desde: Optional[date] = Query(None, description="Fecha de inicio desde"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha de inicio hasta"),
    activas_solamente: Optional[bool] = Query(None, description="Solo proyecciones activas")
):
    """Listar todas las proyecciones con filtros opcionales"""
    proyecciones = list(proyecciones_db.values())
    
    # Aplicar filtros
    if id_producto:
        proyecciones = [p for p in proyecciones if p["id_producto"] == id_producto]
    if tipo_proyeccion:
        proyecciones = [p for p in proyecciones if p["tipo_proyeccion"] == tipo_proyeccion]
    if estado:
        proyecciones = [p for p in proyecciones if p["estado"] == estado]
    if fecha_desde:
        proyecciones = [p for p in proyecciones if p["fecha_inicio"] >= fecha_desde]
    if fecha_hasta:
        proyecciones = [p for p in proyecciones if p["fecha_inicio"] <= fecha_hasta]
    if activas_solamente:
        proyecciones = [p for p in proyecciones if p["estado"] == EstadoProyeccion.ACTIVE]
    
    # Recalcular métricas
    for proyeccion in proyecciones:
        calcular_metricas_proyeccion(proyeccion)
    
    return [ProyeccionDemandaResponse(**proyeccion) for proyeccion in proyecciones]

@app.get("/proyecciones/{proyeccion_id}", response_model=ProyeccionDemandaResponse, tags=["Proyecciones"])
async def obtener_proyeccion(proyeccion_id: str):
    """Obtener una proyección específica por ID"""
    if proyeccion_id not in proyecciones_db:
        raise HTTPException(status_code=404, detail="Proyección no encontrada")
    
    proyeccion = proyecciones_db[proyeccion_id]
    proyeccion = calcular_metricas_proyeccion(proyeccion)
    
    return ProyeccionDemandaResponse(**proyeccion)

@app.put("/proyecciones/{proyeccion_id}", response_model=ProyeccionDemandaResponse, tags=["Proyecciones"])
async def actualizar_proyeccion(proyeccion_id: str, proyeccion_update: ProyeccionDemandaUpdate):
    """Actualizar una proyección existente"""
    if proyeccion_id not in proyecciones_db:
        raise HTTPException(status_code=404, detail="Proyección no encontrada")
    
    proyeccion = proyecciones_db[proyeccion_id]
    update_data = proyeccion_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        proyeccion[field] = value
    
    proyeccion["fecha_actualizacion"] = datetime.now()
    proyeccion = calcular_metricas_proyeccion(proyeccion)
    proyecciones_db[proyeccion_id] = proyeccion
    
    return ProyeccionDemandaResponse(**proyeccion)

@app.delete("/proyecciones/{proyeccion_id}", tags=["Proyecciones"])
async def eliminar_proyeccion(proyeccion_id: str):
    """Eliminar una proyección"""
    if proyeccion_id not in proyecciones_db:
        raise HTTPException(status_code=404, detail="Proyección no encontrada")
    
    del proyecciones_db[proyeccion_id]
    return {"message": f"Proyección {proyeccion_id} eliminada exitosamente"}

@app.patch("/proyecciones/{proyeccion_id}/activar", tags=["Estados"])
async def activar_proyeccion(proyeccion_id: str):
    """Activar una proyección"""
    if proyeccion_id not in proyecciones_db:
        raise HTTPException(status_code=404, detail="Proyección no encontrada")
    
    proyeccion = proyecciones_db[proyeccion_id]
    proyeccion["estado"] = EstadoProyeccion.ACTIVE
    proyeccion["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Proyección {proyeccion_id} activada exitosamente"}

@app.patch("/proyecciones/{proyeccion_id}/archivar", tags=["Estados"])
async def archivar_proyeccion(proyeccion_id: str):
    """Archivar una proyección"""
    if proyeccion_id not in proyecciones_db:
        raise HTTPException(status_code=404, detail="Proyección no encontrada")
    
    proyeccion = proyecciones_db[proyeccion_id]
    proyeccion["estado"] = EstadoProyeccion.ARCHIVED
    proyeccion["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Proyección {proyeccion_id} archivada exitosamente"}

@app.get("/productos/{id_producto}/proyecciones", response_model=ProyeccionAgregada, tags=["Consultas"])
async def obtener_proyecciones_producto(id_producto: str):
    """Obtener todas las proyecciones de un producto específico"""
    proyecciones_producto = [
        ProyeccionDemandaResponse(**calcular_metricas_proyeccion(p.copy()))
        for p in proyecciones_db.values() 
        if p["id_producto"] == id_producto
    ]
    
    if not proyecciones_producto:
        raise HTTPException(status_code=404, detail="No se encontraron proyecciones para este producto")
    
    # Calcular métricas agregadas
    demanda_total = sum(p.demanda_estimada for p in proyecciones_producto)
    dias_total = sum(p.dias_vigencia for p in proyecciones_producto)
    confianzas = [p.confianza_porcentaje for p in proyecciones_producto if p.confianza_porcentaje]
    promedio_confianza = sum(confianzas) / len(confianzas) if confianzas else 0
    
    return ProyeccionAgregada(
        id_producto=id_producto,
        proyecciones=proyecciones_producto,
        demanda_total_estimada=demanda_total,
        periodo_total_dias=dias_total,
        promedio_confianza=round(promedio_confianza, 2)
    )

@app.get("/proyecciones/vigentes", response_model=List[ProyeccionDemandaResponse], tags=["Consultas"])
async def obtener_proyecciones_vigentes():
    """Obtener proyecciones vigentes (activas y dentro del rango de fechas)"""
    hoy = date.today()
    proyecciones_vigentes = []
    
    for proyeccion in proyecciones_db.values():
        if (proyeccion["estado"] == EstadoProyeccion.ACTIVE and
            proyeccion["fecha_inicio"] <= hoy <= proyeccion["fecha_fin"]):
            proyeccion_calculada = calcular_metricas_proyeccion(proyeccion.copy())
            proyecciones_vigentes.append(ProyeccionDemandaResponse(**proyeccion_calculada))
    
    return proyecciones_vigentes

@app.get("/alertas/demanda", response_model=List[AlertaDemanda], tags=["Alertas"])
async def obtener_alertas_demanda():
    """Obtener alertas de demanda basadas en proyecciones vigentes"""
    alertas = []
    hoy = date.today()
    
    for proyeccion in proyecciones_db.values():
        if (proyeccion["estado"] == EstadoProyeccion.ACTIVE and
            proyeccion["fecha_inicio"] <= hoy <= proyeccion["fecha_fin"]):
            
            # Simular stock actual (en integración real vendría de MS-Bodega)
            stock_simulado = 1000
            demanda_proyectada = proyeccion["demanda_estimada"]
            diferencia = stock_simulado - demanda_proyectada
            
            # Determinar tipo de alerta y criticidad
            if diferencia < 0:
                tipo_alerta = "STOCK_INSUFICIENTE"
                criticidad = "ALTA" if abs(diferencia) > demanda_proyectada * 0.5 else "MEDIA"
            elif demanda_proyectada > stock_simulado * 1.5:
                tipo_alerta = "DEMANDA_ALTA"
                criticidad = "MEDIA"
            elif demanda_proyectada < stock_simulado * 0.2:
                tipo_alerta = "DEMANDA_BAJA"
                criticidad = "BAJA"
            else:
                continue  # No genera alerta
            
            alertas.append(AlertaDemanda(
                id_producto=proyeccion["id_producto"],
                tipo_alerta=tipo_alerta,
                demanda_proyectada=demanda_proyectada,
                stock_actual=stock_simulado,
                diferencia=diferencia,
                criticidad=criticidad,
                fecha_alerta=datetime.now()
            ))
    
    # Ordenar por criticidad
    criticidad_orden = {"ALTA": 1, "MEDIA": 2, "BAJA": 3}
    alertas.sort(key=lambda x: criticidad_orden[x.criticidad])
    
    return alertas

@app.get("/estadisticas/demanda", tags=["Estadísticas"])
async def obtener_estadisticas_demanda():
    """Obtener estadísticas generales de demanda"""
    proyecciones_activas = [
        p for p in proyecciones_db.values() 
        if p["estado"] == EstadoProyeccion.ACTIVE
    ]
    
    if not proyecciones_activas:
        return {"message": "No hay proyecciones activas"}
    
    # Estadísticas por tipo de proyección
    tipos_count = {}
    demanda_por_tipo = {}
    
    for proyeccion in proyecciones_activas:
        tipo = proyeccion["tipo_proyeccion"]
        tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
        demanda_por_tipo[tipo] = demanda_por_tipo.get(tipo, 0) + proyeccion["demanda_estimada"]
    
    # Demanda total y promedio
    demanda_total = sum(p["demanda_estimada"] for p in proyecciones_activas)
    demanda_promedio = demanda_total / len(proyecciones_activas)
    
    # Confianza promedio
    confianzas = [p["confianza_porcentaje"] for p in proyecciones_activas if p["confianza_porcentaje"]]
    confianza_promedio = sum(confianzas) / len(confianzas) if confianzas else 0
    
    return {
        "total_proyecciones_activas": len(proyecciones_activas),
        "demanda_total_estimada": demanda_total,
        "demanda_promedio": round(demanda_promedio, 2),
        "confianza_promedio": round(confianza_promedio, 2),
        "proyecciones_por_tipo": tipos_count,
        "demanda_por_tipo": demanda_por_tipo,
        "fecha_consulta": datetime.now()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
