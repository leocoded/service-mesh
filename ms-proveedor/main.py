from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime, date, timedelta
import uuid
from models import (
    ProveedorCreate, ProveedorUpdate, ProveedorResponse, ProveedorFilter,
    CertificacionSanitaria, ProveedorEvaluacion, ProveedorEstadisticas,
    CondicionesEntrega, TipoCertificacion, EstadoProveedor
)

app = FastAPI(
    title="MS-Proveedor API",
    description="Microservicio para gestión de proveedores",
    version="1.0.0"
)

# Simulación de base de datos en memoria
proveedores_db = {}
certificaciones_db = {}  # {proveedor_id: [certificaciones]}
evaluaciones_db = {}  # {proveedor_id: [evaluaciones]}

def calcular_calificacion_promedio(proveedor_id: str) -> float:
    """Calcular calificación promedio de un proveedor"""
    evaluaciones = evaluaciones_db.get(proveedor_id, [])
    if not evaluaciones:
        return 0.0
    
    total_puntos = sum(
        (eval["calidad"] + eval["puntualidad"] + eval["servicio"] + eval["precio"]) / 4
        for eval in evaluaciones
    )
    return round(total_puntos / len(evaluaciones), 1)

def verificar_certificaciones_vigentes(proveedor_id: str) -> List[CertificacionSanitaria]:
    """Verificar y actualizar estado de certificaciones"""
    certificaciones = certificaciones_db.get(proveedor_id, [])
    hoy = date.today()
    
    for cert in certificaciones:
        cert["vigente"] = cert["fecha_vencimiento"] >= hoy
    
    return [CertificacionSanitaria(**cert) for cert in certificaciones]

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-Proveedor API activa", "timestamp": datetime.now()}

@app.post("/proveedores", response_model=ProveedorResponse, tags=["Proveedores"])
async def crear_proveedor(proveedor: ProveedorCreate):
    """Crear un nuevo proveedor"""
    proveedor_id = str(uuid.uuid4())
    now = datetime.now()
    
    nuevo_proveedor = {
        "id": proveedor_id,
        "nombre": proveedor.nombre,
        "email": str(proveedor.email),
        "telefono": proveedor.telefono,
        "direccion": proveedor.direccion,
        "ciudad": proveedor.ciudad,
        "pais": proveedor.pais,
        "nit_rut": proveedor.nit_rut,
        "persona_contacto": proveedor.persona_contacto,
        "especialidades": proveedor.especialidades,
        "condiciones_entrega": proveedor.condiciones_entrega.dict(),
        "estado": EstadoProveedor.PENDING,
        "calificacion": None,
        "total_ordenes": 0,
        "fecha_ultimo_pedido": None,
        "fecha_creacion": now,
        "fecha_actualizacion": now
    }
    
    # Inicializar certificaciones y evaluaciones vacías
    certificaciones_db[proveedor_id] = []
    evaluaciones_db[proveedor_id] = []
    
    proveedores_db[proveedor_id] = nuevo_proveedor
    
    return ProveedorResponse(
        **nuevo_proveedor,
        condiciones_entrega=CondicionesEntrega(**nuevo_proveedor["condiciones_entrega"]),
        certificaciones=[]
    )

@app.get("/proveedores", response_model=List[ProveedorResponse], tags=["Proveedores"])
async def listar_proveedores(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre (búsqueda parcial)"),
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    pais: Optional[str] = Query(None, description="Filtrar por país"),
    estado: Optional[EstadoProveedor] = Query(None, description="Filtrar por estado"),
    especialidad: Optional[str] = Query(None, description="Filtrar por especialidad"),
    certificacion: Optional[TipoCertificacion] = Query(None, description="Filtrar por tipo de certificación"),
    tiempo_entrega_max: Optional[int] = Query(None, description="Tiempo máximo de entrega en días")
):
    """Listar todos los proveedores con filtros opcionales"""
    proveedores = list(proveedores_db.values())
    
    # Aplicar filtros
    if nombre:
        proveedores = [p for p in proveedores if nombre.lower() in p["nombre"].lower()]
    if ciudad:
        proveedores = [p for p in proveedores if ciudad.lower() in p["ciudad"].lower()]
    if pais:
        proveedores = [p for p in proveedores if pais.lower() in p["pais"].lower()]
    if estado:
        proveedores = [p for p in proveedores if p["estado"] == estado]
    if especialidad:
        proveedores = [p for p in proveedores if especialidad.lower() in [e.lower() for e in p["especialidades"]]]
    if tiempo_entrega_max:
        proveedores = [p for p in proveedores if p["condiciones_entrega"]["tiempo_entrega"] <= tiempo_entrega_max]
    
    # Filtrar por certificación si se especifica
    if certificacion:
        proveedores_con_cert = []
        for proveedor in proveedores:
            certificaciones = certificaciones_db.get(proveedor["id"], [])
            tiene_certificacion = any(
                cert["tipo"] == certificacion and cert["vigente"]
                for cert in certificaciones
            )
            if tiene_certificacion:
                proveedores_con_cert.append(proveedor)
        proveedores = proveedores_con_cert
    
    # Preparar respuesta con certificaciones
    proveedores_response = []
    for proveedor in proveedores:
        # Actualizar calificación
        proveedor["calificacion"] = calcular_calificacion_promedio(proveedor["id"])
        
        # Obtener certificaciones vigentes
        certificaciones = verificar_certificaciones_vigentes(proveedor["id"])
        
        proveedores_response.append(ProveedorResponse(
            **proveedor,
            condiciones_entrega=CondicionesEntrega(**proveedor["condiciones_entrega"]),
            certificaciones=certificaciones
        ))
    
    return proveedores_response

@app.get("/proveedores/{proveedor_id}", response_model=ProveedorResponse, tags=["Proveedores"])
async def obtener_proveedor(proveedor_id: str):
    """Obtener un proveedor específico por ID"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    proveedor = proveedores_db[proveedor_id]
    proveedor["calificacion"] = calcular_calificacion_promedio(proveedor_id)
    certificaciones = verificar_certificaciones_vigentes(proveedor_id)
    
    return ProveedorResponse(
        **proveedor,
        condiciones_entrega=CondicionesEntrega(**proveedor["condiciones_entrega"]),
        certificaciones=certificaciones
    )

@app.put("/proveedores/{proveedor_id}", response_model=ProveedorResponse, tags=["Proveedores"])
async def actualizar_proveedor(proveedor_id: str, proveedor_update: ProveedorUpdate):
    """Actualizar un proveedor existente"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    proveedor = proveedores_db[proveedor_id]
    update_data = proveedor_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "condiciones_entrega" and value:
            proveedor[field] = value.dict()
        elif field == "email" and value:
            proveedor[field] = str(value)
        else:
            proveedor[field] = value
    
    proveedor["fecha_actualizacion"] = datetime.now()
    proveedor["calificacion"] = calcular_calificacion_promedio(proveedor_id)
    certificaciones = verificar_certificaciones_vigentes(proveedor_id)
    
    return ProveedorResponse(
        **proveedor,
        condiciones_entrega=CondicionesEntrega(**proveedor["condiciones_entrega"]),
        certificaciones=certificaciones
    )

@app.delete("/proveedores/{proveedor_id}", tags=["Proveedores"])
async def eliminar_proveedor(proveedor_id: str):
    """Eliminar un proveedor (marcarlo como inactivo)"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    proveedor = proveedores_db[proveedor_id]
    proveedor["estado"] = EstadoProveedor.INACTIVE
    proveedor["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Proveedor {proveedor_id} desactivado exitosamente"}

@app.post("/proveedores/{proveedor_id}/certificaciones", tags=["Certificaciones"])
async def agregar_certificacion(proveedor_id: str, certificacion: CertificacionSanitaria):
    """Agregar una certificación sanitaria a un proveedor"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    if proveedor_id not in certificaciones_db:
        certificaciones_db[proveedor_id] = []
    
    nueva_certificacion = certificacion.dict()
    nueva_certificacion["vigente"] = certificacion.fecha_vencimiento >= date.today()
    
    certificaciones_db[proveedor_id].append(nueva_certificacion)
    
    return {"message": "Certificación agregada exitosamente", "certificacion": nueva_certificacion}

@app.get("/proveedores/{proveedor_id}/certificaciones", response_model=List[CertificacionSanitaria], tags=["Certificaciones"])
async def listar_certificaciones_proveedor(proveedor_id: str, solo_vigentes: bool = Query(True, description="Solo certificaciones vigentes")):
    """Listar certificaciones de un proveedor"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    certificaciones = verificar_certificaciones_vigentes(proveedor_id)
    
    if solo_vigentes:
        certificaciones = [cert for cert in certificaciones if cert.vigente]
    
    return certificaciones

@app.post("/proveedores/{proveedor_id}/evaluaciones", tags=["Evaluaciones"])
async def agregar_evaluacion(proveedor_id: str, evaluacion: ProveedorEvaluacion):
    """Agregar una evaluación a un proveedor"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    if proveedor_id not in evaluaciones_db:
        evaluaciones_db[proveedor_id] = []
    
    nueva_evaluacion = evaluacion.dict()
    nueva_evaluacion["id_proveedor"] = proveedor_id
    
    evaluaciones_db[proveedor_id].append(nueva_evaluacion)
    
    # Actualizar calificación del proveedor
    proveedor = proveedores_db[proveedor_id]
    proveedor["calificacion"] = calcular_calificacion_promedio(proveedor_id)
    proveedor["fecha_actualizacion"] = datetime.now()
    
    return {"message": "Evaluación agregada exitosamente", "nueva_calificacion": proveedor["calificacion"]}

@app.get("/proveedores/{proveedor_id}/estadisticas", response_model=ProveedorEstadisticas, tags=["Estadísticas"])
async def obtener_estadisticas_proveedor(proveedor_id: str):
    """Obtener estadísticas detalladas de un proveedor"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    proveedor = proveedores_db[proveedor_id]
    certificaciones_vigentes = len([
        cert for cert in certificaciones_db.get(proveedor_id, [])
        if cert["vigente"]
    ])
    
    # En un escenario real, estos datos vendrían de MS-OrdenCompra
    estadisticas = ProveedorEstadisticas(
        id_proveedor=proveedor_id,
        nombre_proveedor=proveedor["nombre"],
        total_ordenes=proveedor["total_ordenes"],
        ordenes_completadas=proveedor["total_ordenes"] - 2,  # Simulado
        ordenes_pendientes=2,  # Simulado
        monto_total_compras=50000.0,  # Simulado
        calificacion_promedio=proveedor.get("calificacion", 0.0),
        tiempo_entrega_promedio=proveedor["condiciones_entrega"]["tiempo_entrega"],
        certificaciones_vigentes=certificaciones_vigentes,
        ultima_actividad=proveedor.get("fecha_ultimo_pedido", proveedor["fecha_actualizacion"])
    )
    
    return estadisticas

@app.patch("/proveedores/{proveedor_id}/activar", tags=["Estados"])
async def activar_proveedor(proveedor_id: str):
    """Activar un proveedor"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    proveedor = proveedores_db[proveedor_id]
    proveedor["estado"] = EstadoProveedor.ACTIVE
    proveedor["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Proveedor {proveedor['nombre']} activado exitosamente"}

@app.patch("/proveedores/{proveedor_id}/suspender", tags=["Estados"])
async def suspender_proveedor(proveedor_id: str, motivo: Optional[str] = None):
    """Suspender un proveedor"""
    if proveedor_id not in proveedores_db:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    proveedor = proveedores_db[proveedor_id]
    proveedor["estado"] = EstadoProveedor.SUSPENDED
    proveedor["fecha_actualizacion"] = datetime.now()
    
    # En un caso real, se podría guardar el motivo en un campo específico
    return {"message": f"Proveedor {proveedor['nombre']} suspendido", "motivo": motivo}

@app.get("/proveedores/buscar/especialidad/{especialidad}", response_model=List[ProveedorResponse], tags=["Búsqueda"])
async def buscar_por_especialidad(especialidad: str):
    """Buscar proveedores por especialidad"""
    proveedores_especialidad = []
    
    for proveedor in proveedores_db.values():
        if proveedor["estado"] == EstadoProveedor.ACTIVE:
            if any(especialidad.lower() in esp.lower() for esp in proveedor["especialidades"]):
                proveedor["calificacion"] = calcular_calificacion_promedio(proveedor["id"])
                certificaciones = verificar_certificaciones_vigentes(proveedor["id"])
                
                proveedores_especialidad.append(ProveedorResponse(
                    **proveedor,
                    condiciones_entrega=CondicionesEntrega(**proveedor["condiciones_entrega"]),
                    certificaciones=certificaciones
                ))
    
    return proveedores_especialidad

@app.get("/alertas/certificaciones", tags=["Alertas"])
async def obtener_alertas_certificaciones(dias_anticipacion: int = Query(30, description="Días de anticipación para alerta")):
    """Obtener alertas de certificaciones próximas a vencer"""
    alertas = []
    fecha_limite = date.today() + timedelta(days=dias_anticipacion)
    
    for proveedor_id, certificaciones in certificaciones_db.items():
        proveedor = proveedores_db.get(proveedor_id)
        if not proveedor or proveedor["estado"] != EstadoProveedor.ACTIVE:
            continue
        
        for cert in certificaciones:
            if cert["fecha_vencimiento"] <= fecha_limite and cert["vigente"]:
                dias_vencimiento = (cert["fecha_vencimiento"] - date.today()).days
                
                alertas.append({
                    "proveedor_id": proveedor_id,
                    "nombre_proveedor": proveedor["nombre"],
                    "tipo_certificacion": cert["tipo"],
                    "numero_certificado": cert["numero_certificado"],
                    "fecha_vencimiento": cert["fecha_vencimiento"],
                    "dias_para_vencer": dias_vencimiento,
                    "criticidad": "ALTA" if dias_vencimiento <= 7 else "MEDIA"
                })
    
    # Ordenar por días de vencimiento
    alertas.sort(key=lambda x: x["dias_para_vencer"])
    
    return alertas

@app.get("/estadisticas/proveedores", tags=["Estadísticas"])
async def obtener_estadisticas_generales():
    """Obtener estadísticas generales de proveedores"""
    if not proveedores_db:
        return {"message": "No hay proveedores registrados"}
    
    proveedores = list(proveedores_db.values())
    
    # Estadísticas por estado
    estados_count = {}
    for proveedor in proveedores:
        estado = proveedor["estado"]
        estados_count[estado] = estados_count.get(estado, 0) + 1
    
    # Estadísticas por país
    paises_count = {}
    for proveedor in proveedores:
        pais = proveedor["pais"]
        paises_count[pais] = paises_count.get(pais, 0) + 1
    
    # Calificación promedio general
    calificaciones = [p.get("calificacion", 0) for p in proveedores if p.get("calificacion")]
    calificacion_promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
    
    # Certificaciones totales vigentes
    total_certificaciones = sum(
        len([cert for cert in certificaciones_db.get(p["id"], []) if cert["vigente"]])
        for p in proveedores
    )
    
    return {
        "total_proveedores": len(proveedores),
        "proveedores_activos": estados_count.get(EstadoProveedor.ACTIVE, 0),
        "calificacion_promedio_general": round(calificacion_promedio, 1),
        "total_certificaciones_vigentes": total_certificaciones,
        "proveedores_por_estado": estados_count,
        "proveedores_por_pais": paises_count,
        "fecha_consulta": datetime.now()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
