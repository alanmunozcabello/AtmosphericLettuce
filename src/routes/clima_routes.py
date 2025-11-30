from fastapi import APIRouter, Path
from services.clima_service import (
    clima_hora_service,
    clima_hoy_service,
    clima_semana_service,
)

router = APIRouter()


@router.get("/clima/hora/{lat}/{lon}")
def ruta_clima_hora(
    lat: float = Path(..., ge=-90, le=90, description="Latitud"),
    lon: float = Path(..., ge=-180, le=180, description="Longitud")
):
    return clima_hora_service(lat, lon)


@router.get("/clima/hoy/{lat}/{lon}")
def ruta_clima_hoy(
    lat: float = Path(..., ge=-90, le=90, description="Latitud"),
    lon: float = Path(..., ge=-180, le=180, description="Longitud")
):
    return clima_hoy_service(lat, lon)


@router.get("/clima/semana/{lat}/{lon}")
def ruta_clima_semana(
    lat: float = Path(..., ge=-90, le=90, description="Latitud"),
    lon: float = Path(..., ge=-180, le=180, description="Longitud")
):
    return clima_semana_service(lat, lon)
