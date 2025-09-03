from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import uuid
from models import (
    ProductoCreate, ProductoUpdate, ProductoResponse, ProductoFilter,
    ProductoStock, CategoriaProducto, UnidadMedida
)

app = FastAPI(
    title="MS-Producto API",
    description="Microservicio para gestión de productos",
    version="1.0.0"
)

# Simulación de base de datos en memoria
productos_db = {}

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-Producto API activa", "timestamp": datetime.now()}

@app.post("/productos", response_model=ProductoResponse, tags=["Productos"])
async def crear_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    producto_id = str(uuid.uuid4())
    now = datetime.now()
    
    nuevo_producto = {
        "id": producto_id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "categoria": producto.categoria,
        "unidad_medida": producto.unidad_medida,
        "precio_unitario": producto.precio_unitario,
        "codigo_barras": producto.codigo_barras,
        "peso_unitario": producto.peso_unitario,
        "requiere_refrigeracion": producto.requiere_refrigeracion,
        "vida_util_dias": producto.vida_util_dias,
        "activo": True,
        "fecha_creacion": now,
        "fecha_actualizacion": now,
        "stock_total": 0,
        "bodegas_disponibles": 0
    }
    
    productos_db[producto_id] = nuevo_producto
    return ProductoResponse(**nuevo_producto)

@app.get("/productos", response_model=List[ProductoResponse], tags=["Productos"])
async def listar_productos(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre (búsqueda parcial)"),
    categoria: Optional[CategoriaProducto] = Query(None, description="Filtrar por categoría"),
    unidad_medida: Optional[UnidadMedida] = Query(None, description="Filtrar por unidad de medida"),
    requiere_refrigeracion: Optional[bool] = Query(None, description="Filtrar productos que requieren refrigeración"),
    precio_min: Optional[float] = Query(None, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, description="Precio máximo"),
    activo: Optional[bool] = Query(True, description="Filtrar por estado activo")
):
    """Listar todos los productos con filtros opcionales"""
    productos = list(productos_db.values())
    
    # Aplicar filtros
    if nombre:
        productos = [p for p in productos if nombre.lower() in p["nombre"].lower()]
    if categoria:
        productos = [p for p in productos if p["categoria"] == categoria]
    if unidad_medida:
        productos = [p for p in productos if p["unidad_medida"] == unidad_medida]
    if requiere_refrigeracion is not None:
        productos = [p for p in productos if p["requiere_refrigeracion"] == requiere_refrigeracion]
    if precio_min:
        productos = [p for p in productos if p["precio_unitario"] >= precio_min]
    if precio_max:
        productos = [p for p in productos if p["precio_unitario"] <= precio_max]
    if activo is not None:
        productos = [p for p in productos if p["activo"] == activo]
    
    return [ProductoResponse(**producto) for producto in productos]

@app.get("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
async def obtener_producto(producto_id: str):
    """Obtener un producto específico por ID"""
    if producto_id not in productos_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return ProductoResponse(**productos_db[producto_id])

@app.put("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
async def actualizar_producto(producto_id: str, producto_update: ProductoUpdate):
    """Actualizar un producto existente"""
    if producto_id not in productos_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto = productos_db[producto_id]
    update_data = producto_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        producto[field] = value
    
    producto["fecha_actualizacion"] = datetime.now()
    productos_db[producto_id] = producto
    
    return ProductoResponse(**producto)

@app.delete("/productos/{producto_id}", tags=["Productos"])
async def eliminar_producto(producto_id: str):
    """Eliminar un producto (marcarlo como inactivo)"""
    if producto_id not in productos_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto = productos_db[producto_id]
    producto["activo"] = False
    producto["fecha_actualizacion"] = datetime.now()
    
    return {"message": f"Producto {producto_id} desactivado exitosamente"}

@app.get("/productos/buscar/codigo-barras/{codigo_barras}", response_model=ProductoResponse, tags=["Búsqueda"])
async def buscar_por_codigo_barras(codigo_barras: str):
    """Buscar producto por código de barras"""
    for producto in productos_db.values():
        if producto.get("codigo_barras") == codigo_barras:
            return ProductoResponse(**producto)
    
    raise HTTPException(status_code=404, detail="Producto no encontrado con el código de barras especificado")

@app.get("/productos/categoria/{categoria}", response_model=List[ProductoResponse], tags=["Búsqueda"])
async def obtener_productos_por_categoria(categoria: CategoriaProducto):
    """Obtener todos los productos de una categoría específica"""
    productos = [
        ProductoResponse(**producto) 
        for producto in productos_db.values() 
        if producto["categoria"] == categoria and producto["activo"]
    ]
    
    return productos

@app.get("/productos/{producto_id}/stock", response_model=ProductoStock, tags=["Stock"])
async def obtener_stock_producto(producto_id: str):
    """Obtener información de stock de un producto específico"""
    if producto_id not in productos_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto = productos_db[producto_id]
    
    # Aquí se integraría con MS-Bodega y MS-Lote para obtener stock real
    # Por ahora simulamos la respuesta
    stock_info = ProductoStock(
        id_producto=producto_id,
        nombre_producto=producto["nombre"],
        stock_total=producto.get("stock_total", 0),
        stock_disponible=producto.get("stock_total", 0),
        stock_reservado=0,
        valor_inventario=producto.get("stock_total", 0) * producto["precio_unitario"],
        bodegas_con_stock=[]  # Se obtendría de MS-Bodega
    )
    
    return stock_info

@app.get("/productos/refrigeracion/requeridos", response_model=List[ProductoResponse], tags=["Consultas"])
async def obtener_productos_refrigeracion():
    """Obtener todos los productos que requieren refrigeración"""
    productos = [
        ProductoResponse(**producto) 
        for producto in productos_db.values() 
        if producto["requiere_refrigeracion"] and producto["activo"]
    ]
    
    return productos

@app.get("/categorias", tags=["Categorías"])
async def listar_categorias():
    """Listar todas las categorías disponibles"""
    return {
        "categorias": [categoria.value for categoria in CategoriaProducto],
        "total": len(CategoriaProducto)
    }

@app.get("/unidades-medida", tags=["Unidades"])
async def listar_unidades_medida():
    """Listar todas las unidades de medida disponibles"""
    return {
        "unidades_medida": [unidad.value for unidad in UnidadMedida],
        "total": len(UnidadMedida)
    }

@app.get("/estadisticas/productos", tags=["Estadísticas"])
async def obtener_estadisticas():
    """Obtener estadísticas generales de productos"""
    productos_activos = [p for p in productos_db.values() if p["activo"]]
    
    # Estadísticas por categoría
    categoria_count = {}
    for producto in productos_activos:
        categoria = producto["categoria"]
        categoria_count[categoria] = categoria_count.get(categoria, 0) + 1
    
    # Productos que requieren refrigeración
    productos_refrigerados = len([p for p in productos_activos if p["requiere_refrigeracion"]])
    
    # Precio promedio
    precios = [p["precio_unitario"] for p in productos_activos]
    precio_promedio = sum(precios) / len(precios) if precios else 0
    
    return {
        "total_productos": len(productos_activos),
        "productos_refrigerados": productos_refrigerados,
        "precio_promedio": round(precio_promedio, 2),
        "productos_por_categoria": categoria_count,
        "fecha_consulta": datetime.now()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
