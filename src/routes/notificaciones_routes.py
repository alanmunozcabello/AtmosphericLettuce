from fastapi import APIRouter
from services.notificaciones_service import (
    enviar_archivo,
    verificar_conexion_gmail,
)
from services.modificadora_service import services_modificar_html

router = APIRouter()


@router.get("/notificaciones/verificar_gmail")
def ruta_verificar_gmail():
    """Endpoint para verificar que la conexión con Gmail API funciona"""
    return verificar_conexion_gmail()


@router.post("/notificaciones/enviar_html")
def ruta_enviar_html(correo):
    services_modificar_html(correo)
    return enviar_archivo(correo, "services/Archivos_HTML/salida.html")


@router.post("/notificaciones/enviar_codigo")
def ruta_enviar_codigo(correo):
    return enviar_archivo(correo, None)
