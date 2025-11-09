from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CategoriaProducto(str, Enum):
    """Categorías de medicamentos"""
    ANALGESICOS = "analgesicos"
    ANTIBIOTICOS = "antibioticos"
    ANTIINFLAMATORIOS = "antiinflamatorios"
    CARDIOVASCULARES = "cardiovasculares"
    RESPIRATORIOS = "respiratorios"
    DIGESTIVOS = "digestivos"
    NEUROLOGICOS = "neurologicos"
    VITAMINAS = "vitaminas"
    VACUNAS = "vacunas"
    OTROS = "otros"


class UnidadMedida(str, Enum):
    """Unidades de medida para medicamentos"""
    MILIGRAMOS = "mg"
    GRAMOS = "g"
    MILILITROS = "ml"
    LITROS = "l"
    TABLETAS = "tabletas"
    CAPSULAS = "capsulas"
    AMPOLLAS = "ampollas"
    VIALES = "viales"
    FRASCOS = "frascos"
    CAJAS = "cajas"
    UNIDADES = "unidades"


class ProductoCreate(BaseModel):
    """Modelo para crear un medicamento"""
    nombre: str
    descripcion: Optional[str] = None
    categoria: CategoriaProducto
    unidad_medida: UnidadMedida
    precio_unitario: float
    codigo_barras: Optional[str] = None
    concentracion: Optional[str] = None  # ej: "500mg", "10mg/ml"
    principio_activo: Optional[str] = None
    laboratorio: Optional[str] = None
    requiere_refrigeracion: bool = False
    requiere_receta: bool = False
    vida_util_dias: Optional[int] = None


class ProductoUpdate(BaseModel):
    """Modelo para actualizar un medicamento"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[CategoriaProducto] = None
    unidad_medida: Optional[UnidadMedida] = None
    precio_unitario: Optional[float] = None
    codigo_barras: Optional[str] = None
    concentracion: Optional[str] = None
    principio_activo: Optional[str] = None
    laboratorio: Optional[str] = None
    requiere_refrigeracion: Optional[bool] = None
    requiere_receta: Optional[bool] = None
    vida_util_dias: Optional[int] = None
    activo: Optional[bool] = None


class ProductoResponse(BaseModel):
    """Modelo de respuesta para medicamento"""
    id: str
    nombre: str
    descripcion: Optional[str] = None
    categoria: CategoriaProducto
    unidad_medida: UnidadMedida
    precio_unitario: float
    codigo_barras: Optional[str] = None
    concentracion: Optional[str] = None
    principio_activo: Optional[str] = None
    laboratorio: Optional[str] = None
    requiere_refrigeracion: bool
    requiere_receta: bool
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
