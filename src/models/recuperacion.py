from pydantic import BaseModel, EmailStr, Field

class SolicitudRecuperacion(BaseModel):
    correo: EmailStr

class VerificacionCodigo(BaseModel):
    correo: EmailStr
    codigo: str

class CambioContrasena(BaseModel):
    correo: EmailStr
    codigo: str
    nueva_contrasena: str = Field(..., min_length=8)
