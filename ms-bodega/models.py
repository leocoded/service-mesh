from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UbicacionGeografica(BaseModel):
    """Modelo para ubicación geográfica"""
    latitud: float
    longitud: float
    direccion: str
    ciudad: str
    pais: str


class BodegaCreate(BaseModel):
    """Modelo para crear una bodega"""
    nombre: str
    capacidad: int
    ubicacion_geografica: UbicacionGeografica
    id_producto: str


class BodegaUpdate(BaseModel):
    """Modelo para actualizar una bodega"""
    nombre: Optional[str] = None
    capacidad: Optional[int] = None
    ubicacion_geografica: Optional[UbicacionGeografica] = None
    cantidad_disponible: Optional[int] = None
    cantidad_reservada: Optional[int] = None
    cantidad_vendida: Optional[int] = None


class BodegaResponse(BaseModel):
    """Modelo de respuesta para bodega"""
    id: str
    nombre: str
    capacidad: int
    ubicacion_geografica: UbicacionGeografica
    cantidad_disponible: int
    cantidad_reservada: int
    cantidad_vendida: int
    id_producto: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class BodegaFilter(BaseModel):
    """Filtros para consulta de bodegas"""
    nombre: Optional[str] = None
    id_producto: Optional[str] = None
    ciudad: Optional[str] = None
    capacidad_min: Optional[int] = None
    capacidad_max: Optional[int] = None
