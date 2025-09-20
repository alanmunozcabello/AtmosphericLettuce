from fastapi import APIRouter
from controllers.clima_controller import clima_hora_controller, clima_hoy_controller, clima_semana_controller

router=APIRouter()

@router.get("/clima/hora/{lat}/{lon}")
def ruta_clima_hora(lat, lon):
    return clima_hora_controller(lat, lon)

@router.get("/clima/hoy/{lat}/{lon}")
def ruta_clima_hoy(lat, lon):
    return clima_hoy_controller(lat, lon)

@router.get("/clima/semana/{lat}/{lon}")
def ruta_clima_semana(lat, lon):
    return clima_semana_controller(lat, lon)