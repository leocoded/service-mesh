from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class TipoAlmacenamiento(str, Enum):
    """Tipos de almacenamiento disponibles"""
    REFRIGERADO = "refrigerado"
    CONGELADO = "congelado"
    AMBIENTE = "ambiente"
    SECO = "seco"


class LoteCreate(BaseModel):
    """Modelo para crear un lote"""
    fecha_vencimiento: date
    tipo_almacenamiento: TipoAlmacenamiento
    cantidad_inicial: int
    id_producto: str
    id_bodega: str
    temperatura_optima: Optional[float] = None
    humedad_optima: Optional[float] = None


class LoteUpdate(BaseModel):
    """Modelo para actualizar un lote"""
    fecha_vencimiento: Optional[date] = None
    tipo_almacenamiento: Optional[TipoAlmacenamiento] = None
    cantidad_disponible: Optional[int] = None
    temperatura_optima: Optional[float] = None
    humedad_optima: Optional[float] = None


class LoteResponse(BaseModel):
    """Modelo de respuesta para lote"""
    id: str
    fecha_vencimiento: date
    tipo_almacenamiento: TipoAlmacenamiento
    cantidad_inicial: int
    cantidad_disponible: int
    cantidad_reservada: int
    cantidad_vendida: int
    id_producto: str
    id_bodega: str
    temperatura_optima: Optional[float] = None
    humedad_optima: Optional[float] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    esta_vencido: bool

    class Config:
        from_attributes = True


class LoteFilter(BaseModel):
    """Filtros para consulta de lotes"""
    id_producto: Optional[str] = None
    id_bodega: Optional[str] = None
    tipo_almacenamiento: Optional[TipoAlmacenamiento] = None
    vencimiento_desde: Optional[date] = None
    vencimiento_hasta: Optional[date] = None
    solo_disponibles: Optional[bool] = None
    solo_vencidos: Optional[bool] = None


class AlertaVencimiento(BaseModel):
    """Modelo para alertas de vencimiento"""
    id_lote: str
    dias_para_vencer: int
    cantidad_disponible: int
    prioridad: str  # "ALTA", "MEDIA", "BAJA"
