"""
Modelos Pydantic para Clima
"""

from pydantic import BaseModel, Field, ConfigDict


class ClimaRequest(BaseModel):
    """
    Modelo para solicitudes de clima con coordenadas validadas
    """
    lat: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitud (entre -90 y 90)"
    )
    lon: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitud (entre -180 y 180)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lat": -33.4489,
                "lon": -70.6693
            }
        }
    )
