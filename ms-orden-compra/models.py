from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


class EstadoOrden(str, Enum):
    """Estados de la orden de compra"""
    DRAFT = "borrador"
    PENDING = "pendiente"
    APPROVED = "aprobada"
    SENT = "enviada"
    RECEIVED = "recibida"
    CANCELLED = "cancelada"


class TipoOrden(str, Enum):
    """Tipos de orden de compra"""
    REGULAR = "regular"
    URGENT = "urgente"
    RECURRING = "recurrente"


class OrdenCompraCreate(BaseModel):
    """Modelo para crear una orden de compra"""
    id_proveedor: str
    tipo_orden: TipoOrden
    fecha_requerida: date
    observaciones: Optional[str] = None
    direccion_entrega: Optional[str] = None


class ItemOrdenCreate(BaseModel):
    """Modelo para crear un item de orden"""
    id_producto: str
    cantidad: int
    precio_unitario: Decimal
    descuento_porcentaje: Optional[Decimal] = 0


class OrdenCompraUpdate(BaseModel):
    """Modelo para actualizar una orden de compra"""
    id_proveedor: Optional[str] = None
    tipo_orden: Optional[TipoOrden] = None
    fecha_requerida: Optional[date] = None
    observaciones: Optional[str] = None
    direccion_entrega: Optional[str] = None
    estado: Optional[EstadoOrden] = None


class ItemOrdenResponse(BaseModel):
    """Modelo de respuesta para item de orden"""
    id: str
    id_producto: str
    nombre_producto: Optional[str] = None
    cantidad: int
    precio_unitario: Decimal
    descuento_porcentaje: Decimal
    subtotal: Decimal
    total_item: Decimal

    class Config:
        from_attributes = True


class OrdenCompraResponse(BaseModel):
    """Modelo de respuesta para orden de compra"""
    id: str
    numero_orden: str
    id_proveedor: str
    nombre_proveedor: Optional[str] = None
    tipo_orden: TipoOrden
    estado: EstadoOrden
    fecha_orden: date
    fecha_requerida: date
    fecha_aprobacion: Optional[datetime] = None
    fecha_envio: Optional[datetime] = None
    fecha_recepcion: Optional[datetime] = None
    observaciones: Optional[str] = None
    direccion_entrega: Optional[str] = None
    items: List[ItemOrdenResponse] = []
    subtotal: Decimal
    descuento_total: Decimal
    impuestos: Decimal
    total: Decimal
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class OrdenCompraFilter(BaseModel):
    """Filtros para consulta de órdenes de compra"""
    id_proveedor: Optional[str] = None
    estado: Optional[EstadoOrden] = None
    tipo_orden: Optional[TipoOrden] = None
    fecha_desde: Optional[date] = None
    fecha_hasta: Optional[date] = None
    monto_min: Optional[Decimal] = None
    monto_max: Optional[Decimal] = None


class ResumenOrdenesProveedor(BaseModel):
    """Resumen de órdenes por proveedor"""
    id_proveedor: str
    nombre_proveedor: Optional[str] = None
    total_ordenes: int
    ordenes_pendientes: int
    ordenes_completadas: int
    monto_total: Decimal
    promedio_tiempo_entrega: Optional[int] = None  # días


class AlertaOrden(BaseModel):
    """Alerta de orden de compra"""
    id_orden: str
    numero_orden: str
    tipo_alerta: str  # "RETRASO_ENTREGA", "APROBACION_PENDIENTE", "STOCK_CRITICO"
    dias_retraso: Optional[int] = None
    criticidad: str  # "ALTA", "MEDIA", "BAJA"
    descripcion: str
    fecha_alerta: datetime
