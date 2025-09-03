from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class TipoCertificacion(str, Enum):
    """Tipos de certificación sanitaria"""
    ISO_22000 = "iso_22000"
    HACCP = "haccp"
    BRC = "brc"
    SQF = "sqf"
    ORGANICA = "organica"
    KOSHER = "kosher"
    HALAL = "halal"
    OTRA = "otra"


class EstadoProveedor(str, Enum):
    """Estados del proveedor"""
    ACTIVE = "activo"
    INACTIVE = "inactivo"
    SUSPENDED = "suspendido"
    PENDING = "pendiente"


class CondicionesEntrega(BaseModel):
    """Condiciones de entrega del proveedor"""
    tiempo_entrega: int  # días
    cantidad_minima: Optional[int] = None
    costo_envio: Optional[float] = None
    area_cobertura: Optional[str] = None
    restricciones: Optional[List[str]] = []


class CertificacionSanitaria(BaseModel):
    """Certificación sanitaria del proveedor"""
    tipo: TipoCertificacion
    entidad: str
    numero_certificado: str
    fecha_emision: date
    fecha_vencimiento: date
    vigente: bool = True


class ProveedorCreate(BaseModel):
    """Modelo para crear un proveedor"""
    nombre: str
    email: EmailStr
    telefono: str
    direccion: str
    ciudad: str
    pais: str
    nit_rut: str
    persona_contacto: str
    especialidades: List[str] = []
    condiciones_entrega: CondicionesEntrega


class ProveedorUpdate(BaseModel):
    """Model para actualizar un proveedor"""
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    persona_contacto: Optional[str] = None
    especialidades: Optional[List[str]] = None
    condiciones_entrega: Optional[CondicionesEntrega] = None
    estado: Optional[EstadoProveedor] = None


class ProveedorResponse(BaseModel):
    """Modelo de respuesta para proveedor"""
    id: str
    nombre: str
    email: str
    telefono: str
    direccion: str
    ciudad: str
    pais: str
    nit_rut: str
    persona_contacto: str
    especialidades: List[str]
    condiciones_entrega: CondicionesEntrega
    certificaciones: List[CertificacionSanitaria] = []
    estado: EstadoProveedor
    calificacion: Optional[float] = None
    total_ordenes: int = 0
    fecha_ultimo_pedido: Optional[datetime] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class ProveedorFilter(BaseModel):
    """Filtros para consulta de proveedores"""
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    estado: Optional[EstadoProveedor] = None
    especialidad: Optional[str] = None
    certificacion: Optional[TipoCertificacion] = None
    tiempo_entrega_max: Optional[int] = None


class ProveedorEvaluacion(BaseModel):
    """Evaluación de proveedor"""
    id_proveedor: str
    calidad: int  # 1-5
    puntualidad: int  # 1-5
    servicio: int  # 1-5
    precio: int  # 1-5
    comentarios: Optional[str] = None
    fecha_evaluacion: datetime = datetime.now()


class ProveedorEstadisticas(BaseModel):
    """Estadísticas de un proveedor"""
    id_proveedor: str
    nombre_proveedor: str
    total_ordenes: int
    ordenes_completadas: int
    ordenes_pendientes: int
    monto_total_compras: float
    calificacion_promedio: float
    tiempo_entrega_promedio: int
    certificaciones_vigentes: int
    ultima_actividad: datetime
