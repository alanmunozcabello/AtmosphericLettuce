"""
Modelos Pydantic para Usuario
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class UsuarioRegistro(BaseModel):
    """
    Modelo para registro de nuevo usuario
    """
    correo: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario",
        example="usuario@example.com"
    )
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario",
        example="Juan Pérez"
    )
    contrasena: str = Field(
        ...,
        min_length=8,
        description="Contraseña del usuario (mínimo 8 caracteres)",
        example="MiContraseña123"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "correo": "usuario@example.com",
                "nombre": "Juan Pérez",
                "contrasena": "MiContraseña123"
            }
        }


class UsuarioModificado(BaseModel):
    """
    Modelo para modificar datos del usuario
    Todos los campos son opcionales
    """
    nombre: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario"
    )
    ciudad: Optional[str] = Field(
        None,
        max_length=100,
        description="Ciudad del usuario"
    )
    region: Optional[str] = Field(
        None,
        max_length=100,
        description="Región/Estado del usuario"
    )
    foto_perfil: Optional[str] = Field(
        None,
        description="Foto de perfil en formato Base64"
    )

    @validator('foto_perfil')
    def validar_foto_base64(cls, v):
        """Validar que la foto sea Base64 válida"""
        if v and not v.startswith('data:image/'):
            raise ValueError('La foto debe estar en formato Base64 (data:image/...)')
        if v and len(v) > 500000:  # ~375KB en Base64
            raise ValueError('La imagen es muy grande (máximo ~375KB)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan Pérez Actualizado",
                "ciudad": "Santiago",
                "region": "Región Metropolitana",
                "foto_perfil": "data:image/jpeg;base64,/9j/4AAQ..."
            }
        }


class UbicacionUsuario(BaseModel):
    """
    Modelo para ubicación del usuario
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
    ciudad: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=100)


class UsuarioResponse(BaseModel):
    """
    Modelo de respuesta con datos del usuario
    """
    id: str
    nombre: str
    ubicacion: dict
    cultivos: list
    foto_perfil: Optional[str] = None
    notificaciones: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": "usuario@example.com",
                "nombre": "Juan Pérez",
                "ubicacion": {
                    "latitud": -33.4489,
                    "longitud": -70.6693,
                    "ciudad": "Santiago",
                    "region": "Región Metropolitana"
                },
                "cultivos": [
                    {
                        "nombre": "Tomate",
                        "hectareas": 5.5,
                        "area": 5.5,
                        "puntos": [
                            {"latitud": -33.4489, "longitud": -70.6693}
                        ]
                    }
                ],
                "foto_perfil": "data:image/jpeg;base64,/9j/4AAQ...",
                "notificaciones": True
            }
        }
