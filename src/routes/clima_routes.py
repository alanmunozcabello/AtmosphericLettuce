from fastapi import APIRouter
from services.clima_service import (
    clima_hora_service,
    clima_hoy_service,
    clima_semana_service,
)

router = APIRouter()


@router.get("/clima/hora/{lat}/{lon}")
def ruta_clima_hora(lat, lon):
    return clima_hora_service(lat, lon)


@router.get("/clima/hoy/{lat}/{lon}")
def ruta_clima_hoy(lat, lon):
    return clima_hoy_service(lat, lon)


@router.get("/clima/semana/{lat}/{lon}")
def ruta_clima_semana(lat, lon):
    return clima_semana_service(lat, lon)
