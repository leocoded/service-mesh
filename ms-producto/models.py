from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CategoriaProducto(str, Enum):
    """Categorías de productos"""
    ALIMENTOS = "alimentos"
    BEBIDAS = "bebidas"
    LACTEOS = "lacteos"
    CARNES = "carnes"
    VEGETALES = "vegetales"
    FRUTAS = "frutas"
    CONGELADOS = "congelados"
    SECOS = "secos"
    OTROS = "otros"


class UnidadMedida(str, Enum):
    """Unidades de medida"""
    KILOGRAMOS = "kg"
    GRAMOS = "g"
    LITROS = "l"
    MILILITROS = "ml"
    UNIDADES = "unidades"
    CAJAS = "cajas"
    PAQUETES = "paquetes"


class ProductoCreate(BaseModel):
    """Modelo para crear un producto"""
    nombre: str
    descripcion: Optional[str] = None
    categoria: CategoriaProducto
    unidad_medida: UnidadMedida
    precio_unitario: float
    codigo_barras: Optional[str] = None
    peso_unitario: Optional[float] = None
    requiere_refrigeracion: bool = False
    vida_util_dias: Optional[int] = None


class ProductoUpdate(BaseModel):
    """Modelo para actualizar un producto"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[CategoriaProducto] = None
    unidad_medida: Optional[UnidadMedida] = None
    precio_unitario: Optional[float] = None
    codigo_barras: Optional[str] = None
    peso_unitario: Optional[float] = None
    requiere_refrigeracion: Optional[bool] = None
    vida_util_dias: Optional[int] = None
    activo: Optional[bool] = None


class ProductoResponse(BaseModel):
    """Modelo de respuesta para producto"""
    id: str
    nombre: str
    descripcion: Optional[str] = None
    categoria: CategoriaProducto
    unidad_medida: UnidadMedida
    precio_unitario: float
    codigo_barras: Optional[str] = None
    peso_unitario: Optional[float] = None
    requiere_refrigeracion: bool
    vida_util_dias: Optional[int] = None
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    # Información agregada desde otros microservicios
    stock_total: int = 0
    bodegas_disponibles: int = 0

    class Config:
        from_attributes = True


class ProductoFilter(BaseModel):
    """Filtros para consulta de productos"""
    nombre: Optional[str] = None
    categoria: Optional[CategoriaProducto] = None
    unidad_medida: Optional[UnidadMedida] = None
    requiere_refrigeracion: Optional[bool] = None
    precio_min: Optional[float] = None
    precio_max: Optional[float] = None
    activo: Optional[bool] = None


class ProductoStock(BaseModel):
    """Información de stock de un producto"""
    id_producto: str
    nombre_producto: str
    stock_total: int
    stock_disponible: int
    stock_reservado: int
    valor_inventario: float
    bodegas_con_stock: List[dict]
