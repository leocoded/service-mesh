from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, date
from enum import Enum


class TipoProyeccion(str, Enum):
    """Tipos de proyección de demanda"""
    SEMANAL = "semanal"
    MENSUAL = "mensual"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"


class EstadoProyeccion(str, Enum):
    """Estados de la proyección"""
    DRAFT = "borrador"
    ACTIVE = "activa"
    ARCHIVED = "archivada"


class ProyeccionDemandaCreate(BaseModel):
    """Modelo para crear una proyección de demanda"""
    id_producto: str
    fecha_inicio: date
    fecha_fin: date
    tipo_proyeccion: TipoProyeccion
    demanda_estimada: int
    unidades: str
    metodologia: Optional[str] = "historico"
    factores_considerados: Optional[List[str]] = []
    confianza_porcentaje: Optional[float] = None


class ProyeccionDemandaUpdate(BaseModel):
    """Modelo para actualizar una proyección de demanda"""
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    tipo_proyeccion: Optional[TipoProyeccion] = None
    demanda_estimada: Optional[int] = None
    metodologia: Optional[str] = None
    factores_considerados: Optional[List[str]] = None
    confianza_porcentaje: Optional[float] = None
    estado: Optional[EstadoProyeccion] = None


class ProyeccionDemandaResponse(BaseModel):
    """Modelo de respuesta para proyección de demanda"""
    id: str
    id_producto: str
    fecha_inicio: date
    fecha_fin: date
    tipo_proyeccion: TipoProyeccion
    demanda_estimada: int
    unidades: str
    metodologia: str
    factores_considerados: List[str]
    confianza_porcentaje: Optional[float] = None
    estado: EstadoProyeccion
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    # Campos calculados
    dias_vigencia: int
    demanda_diaria: float
    demanda_semanal: float
    demanda_mensual: float

    class Config:
        from_attributes = True


class DetalleProyeccion(BaseModel):
    """Detalle granular de proyección por periodo"""
    periodo: str  # "2024-01", "2024-W1", etc.
    demanda_estimada: int
    demanda_real: Optional[int] = None
    diferencia: Optional[int] = None
    precision_porcentaje: Optional[float] = None


class ProyeccionAgregada(BaseModel):
    """Proyección agregada por producto"""
    id_producto: str
    nombre_producto: Optional[str] = None
    proyecciones: List[ProyeccionDemandaResponse]
    demanda_total_estimada: int
    periodo_total_dias: int
    promedio_confianza: float


class AlertaDemanda(BaseModel):
    """Alerta de demanda"""
    id_producto: str
    tipo_alerta: str  # "DEMANDA_ALTA", "DEMANDA_BAJA", "STOCK_INSUFICIENTE"
    demanda_proyectada: int
    stock_actual: int
    diferencia: int
    criticidad: str  # "ALTA", "MEDIA", "BAJA"
    fecha_alerta: datetime
