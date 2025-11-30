"""
Modelos Pydantic para Cultivo
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EtapaPlanta(str, Enum):
    """Etapas del ciclo de vida de la planta"""
    SIEMBRA_GERMINACION = "siembra-germinacion"
    CRECIMIENTO_VEGETATIVO = "crecimiento-vegetativo"
    FLORACION = "floracion"
    FRUCTIFICACION = "fructificacion"
    MADURACION = "maduracion"
    COSECHA_DORMANCIA = "cosecha-dormancia"


class TipoRiego(str, Enum):
    """Tipos de sistemas de riego"""
    GOTEO = "goteo"
    ASPERSION = "aspersion"
    INUNDACION = "inundacion"
    PIVOTE_CENTRAL = "pivote-central"
    MICROASPERSION = "microaspersion"


class TexturaSuelo(str, Enum):
    """Texturas del suelo"""
    ARENOSO = "arenoso"
    FRANCO = "franco"
    ARCILLOSO = "arcilloso"
    FRANCO_ARENOSO = "franco-arenoso"
    FRANCO_ARCILLOSO = "franco-arcilloso"
    ARCILLO_ARENOSO = "arcillo-arenoso"


class TipoSensor(str, Enum):
    """Tipos de sensores de humedad"""
    CAPACITANCIA = "capacitancia"
    TENSIOMETRO = "tensiometro"
    RESISTENCIA = "resistencia"
    NEUTRONES = "neutrones"
    TDR = "tdr"
    GRAVIMETRICO = "gravimetrico"
    NO_TIENE = "no-tiene"


class PuntoCoordenada(BaseModel):
    """
    Modelo para un punto de coordenadas GPS
    """
    latitud: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitud (entre -90 y 90)"
    )
    longitud: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitud (entre -180 y 180)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "latitud": -33.4489,
                "longitud": -70.6693
            }
        }


class CultivoCreate(BaseModel):
    """
    Modelo para crear un nuevo cultivo
    """
    nombre_cultivo: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del cultivo",
        example="Tomate"
    )
    hectareas: int = Field(
        ...,
        gt=0,
        description="Hectáreas del cultivo",
        example=5
    )

    class Config:
        json_schema_extra = {
            "example": {
                "nombre_cultivo": "Tomate",
                "hectareas": 5
            }
        }


class CultivoDatos(BaseModel):
    """
    Modelo completo para datos del cultivo (formulario técnico)
    """
    nombre_cultivo: str = Field(..., min_length=1, max_length=100)
    hectareas: Optional[float] = Field(None, description="Hectáreas (opcional para modificar formulario)")
    fecha_siembra: Optional[str] = Field(None, description="Fecha en formato ISO")
    notas: Optional[str] = Field(None, max_length=1000)
    
    # Etapa y riego
    etapa_planta: Optional[EtapaPlanta] = Field(
        None,
        description="Etapa de la planta"
    )
    tipo_riego: Optional[TipoRiego] = Field(
        None,
        description="Tipo de riego"
    )
    ultimo_riego: Optional[str] = Field(None, description="Última vez que se regó (datetime)")
    frecuencia_riego: Optional[str] = Field(None, description="Frecuencia de riego en días")
    
    # Suelo
    humedad_suelo: Optional[str] = Field(None, description="Porcentaje de humedad del suelo")
    textura_suelo: Optional[TexturaSuelo] = Field(
        None,
        description="Textura del suelo"
    )
    
    # Planta
    variedad_planta: Optional[str] = Field(None, max_length=100)
    estado_planta: Optional[str] = Field(None, max_length=200, description="Observación visual")
    estres_hidrico: Optional[int] = Field(None, ge=0, le=1, description="0=No, 1=Sí")
    profundidad_radical: Optional[int] = Field(None, gt=0, description="Profundidad en cm")
    densidad_plantacion: Optional[int] = Field(None, gt=0, description="Plantas por hectárea")
    
    # Sistema de riego
    tipo_sensor: Optional[TipoSensor] = Field(
        None,
        description="Tipo de sensor"
    )
    eficiencia_riego: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de eficiencia")
    caudal: Optional[float] = Field(None, gt=0, description="Litros por hora")
    ph_agua: Optional[float] = Field(None, ge=0, le=14, description="pH del agua")
    acolchado: Optional[int] = Field(None, ge=0, le=1, description="0=No, 1=Sí")

    @validator('fecha_siembra')
    def validar_fecha_siembra(cls, v):
        """Validar que la fecha no sea futura"""
        if v:
            try:
                fecha = datetime.fromisoformat(v.replace('Z', '+00:00'))
                if fecha > datetime.now():
                    raise ValueError('La fecha de siembra no puede ser futura')
            except ValueError as e:
                raise ValueError(f'Formato de fecha inválido: {e}')
        return v

    @validator('ph_agua')
    def validar_ph(cls, v):
        """Validar rango de pH"""
        if v is not None and (v < 0 or v > 14):
            raise ValueError('El pH debe estar entre 0 y 14')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "nombre_cultivo": "Tomate",
                "hectareas": 5.5,
                "fecha_siembra": "2024-03-15T00:00:00",
                "notas": "Variedad híbrida resistente",
                "etapa_planta": "crecimiento-vegetativo",
                "tipo_riego": "goteo",
                "ultimo_riego": "2024-11-28T08:00:00",
                "frecuencia_riego": "2",
                "humedad_suelo": "25",
                "textura_suelo": "franco",
                "variedad_planta": "Roma VF",
                "estado_planta": "Saludable, hojas verdes",
                "estres_hidrico": 0,
                "profundidad_radical": 30,
                "densidad_plantacion": 10000,
                "tipo_sensor": "capacitancia",
                "eficiencia_riego": 85.5,
                "caudal": 2.5,
                "ph_agua": 6.8,
                "acolchado": 1
            }
        }


class AreaCultivoDatos(BaseModel):
    """
    Modelo para área del cultivo con coordenadas GPS
    """
    cultivo: str = Field(..., min_length=1, max_length=100, description="Nombre del cultivo")
    area: float = Field(..., gt=0, description="Área en hectáreas")
    puntos: List[PuntoCoordenada] = Field(
        ...,
        min_length=3,
        description="Lista de puntos GPS que forman el polígono (mínimo 3)"
    )

    @validator('puntos')
    def validar_puntos(cls, v):
        """Validar que haya al menos 3 puntos para formar un polígono"""
        if len(v) < 3:
            raise ValueError('Se necesitan al menos 3 puntos para formar un área')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "cultivo": "Tomate",
                "area": 5.5,
                "puntos": [
                    {"latitud": -33.4489, "longitud": -70.6693},
                    {"latitud": -33.4490, "longitud": -70.6694},
                    {"latitud": -33.4491, "longitud": -70.6692},
                    {"latitud": -33.4489, "longitud": -70.6693}
                ]
            }
        }


class CultivoResponse(BaseModel):
    """
    Modelo de respuesta con datos completos del cultivo
    """
    id: int
    nombre: str
    hectareas: float
    formulario: dict
    puntos: List[PuntoCoordenada]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Tomate",
                "hectareas": 5.5,
                "formulario": {
                    "fecha_siembra": "2024-03-15",
                    "etapa_planta": "crecimiento-vegetativo",
                    "tipo_riego": "goteo"
                },
                "puntos": [
                    {"latitud": -33.4489, "longitud": -70.6693}
                ]
            }
        }
