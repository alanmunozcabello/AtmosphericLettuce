"""
Modelos Pydantic para Usuario
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional


class LoginRequest(BaseModel):
    """
    Modelo para inicio de sesión
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "correo": "usuario@example.com",
                "contrasena": "MiContraseña123"
            }
        }
    )
    
    correo: EmailStr = Field(
        ...,
        description="Correo electrónico",
        example="usuario@example.com"
    )
    contrasena: str = Field(
        ...,
        min_length=1,
        description="Contraseña del usuario",
        example="MiContraseña123"
    )


class UsuarioRegistro(BaseModel):
    """
    Modelo para registro de nuevo usuario
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "correo": "usuario@example.com",
                "nombre": "Juan Pérez",
                "contrasena": "MiContraseña123"
            }
        }
    )
    
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

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v):
        import re
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ'\s]+$", v):
            raise ValueError('El nombre contiene caracteres inválidos (permitidos: letras, tildes, espacios, \')')
        return v
    contrasena: str = Field(
        ...,
        min_length=8,
        max_length=25,
        description="Contraseña del usuario (6-25 caracteres)",
        example="MiContraseña123!"
    )

    @field_validator('contrasena')
    @classmethod
    def validar_complejidad_contrasena(cls, v):
        import re
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError('La contraseña debe contener al menos un carácter especial (@$!%*?&)')
        if re.search(r"['\";]", v):
            raise ValueError('La contraseña no puede contener caracteres como comillas o punto y coma')
        return v


class UsuarioModificado(BaseModel):
    """
    Modelo para modificar datos del usuario
    Todos los campos son opcionales
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Pérez Actualizado",
                "ciudad": "Santiago",
                "region": "Región Metropolitana",
                "foto_perfil": "data:image/jpeg;base64,/9j/4AAQ..."
            }
        }
    )
    
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

    @field_validator('nombre', 'ciudad', 'region')
    @classmethod
    def validar_texto_generico(cls, v):
        if v is None:
            return v
        import re
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ'\s]*$", v):
            raise ValueError('El campo contiene caracteres inválidos (permitidos: letras, tildes, espacios, \')')
        return v
    foto_perfil: Optional[str] = Field(
        None,
        description="Foto de perfil en formato Base64"
    )

    @field_validator('foto_perfil')
    @classmethod
    def validar_foto_base64(cls, v):
        """Validar que la foto sea Base64 válida"""
        if not v:
            return v
            
        import base64
        import re
        
        # Validar formato data:image/...
        if not v.startswith('data:image/'):
            raise ValueError('La foto debe estar en formato Base64 (data:image/...)')
        
        # Validar tamaño
        if len(v) > 10000000:  # ~7.5MB en Base64
            raise ValueError('La imagen es muy grande (máximo ~7.5MB)')
        
        # Validar tipos MIME permitidos
        mime_pattern = r'^data:image/(jpeg|jpg|png|gif|webp);base64,'
        if not re.match(mime_pattern, v):
            raise ValueError('Tipo de imagen no soportado. Usa: jpeg, jpg, png, gif o webp')
        
        # Validar que el Base64 sea decodificable
        try:
            header, data = v.split(',', 1)
            base64.b64decode(data, validate=True)
        except Exception:
            raise ValueError('Datos Base64 inválidos o corruptos')
        
        return v


class Coordenadas(BaseModel):
    """
    Modelo simple para validar coordenadas GPS
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lat": -33.4489,
                "lon": -70.6693
            }
        }
    )
    
    lat: float = Field(..., ge=-90, le=90, description="Latitud")
    lon: float = Field(..., ge=-180, le=180, description="Longitud")


class UbicacionUsuario(BaseModel):
    """
    Modelo para ubicación del usuario
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "latitud": -33.4489,
                "longitud": -70.6693,
                "ciudad": "Santiago",
                "region": "Región Metropolitana"
            }
        }
    )
    
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
    model_config = ConfigDict(
        json_schema_extra={
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
    )
    
    id: str
    nombre: str
    ubicacion: dict
    cultivos: list
    foto_perfil: Optional[str] = None
    notificaciones: bool = True


class NotificacionesConfig(BaseModel):
    """
    Modelo para configurar notificaciones del usuario
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notificaciones": True
            }
        }
    )
    
    notificaciones: bool = Field(
        ...,
        description="Activar/desactivar notificaciones por correo"
    )
