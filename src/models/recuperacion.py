from pydantic import BaseModel, EmailStr, Field, field_validator

class SolicitudRecuperacion(BaseModel):
    correo: EmailStr

class VerificacionCodigo(BaseModel):
    correo: EmailStr
    codigo: str

class CambioContrasena(BaseModel):
    correo: EmailStr
    codigo: str
    nueva_contrasena: str = Field(
        ...,
        min_length=6,
        max_length=25,
        description="Contraseña del usuario (6-25 caracteres)",
        example="MiContraseña123!"
    )

    @field_validator('nueva_contrasena')
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
