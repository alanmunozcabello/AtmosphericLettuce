"""
Modelos Pydantic para Chat
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List


class ChatConsulta(BaseModel):
    """
    Modelo para consulta al chatbot
    """
    texto: Optional[str] = Field(
        None,
        max_length=5000,
        description="Texto de la consulta del usuario"
    )
    correo: Optional[EmailStr] = Field(
        None,
        description="Correo del usuario (para contexto de cultivos)"
    )
    cultivo: Optional[str] = Field(
        None,
        max_length=100,
        description="Nombre del cultivo sobre el que se consulta"
    )
    imagen: Optional[List[str]] = Field(
        None,
        description="Lista de imágenes en Base64 para análisis"
    )
    pdf: Optional[List[str]] = Field(
        None,
        description="Lista de PDFs en Base64 para análisis"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "texto": "¿Cómo puedo mejorar el riego de mis tomates?",
                "correo": "usuario@example.com",
                "cultivo": "Tomate",
                "imagen": ["data:image/jpeg;base64,..."],
                "pdf": []
            }
        }
    )
