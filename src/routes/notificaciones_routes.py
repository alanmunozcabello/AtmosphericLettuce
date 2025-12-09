from fastapi import APIRouter, Depends
from middleware.autenticacion_mw import verificar_autenticacion
from services.notification_service import (
    enviar_archivo,
    verificar_conexion_gmail,
    generar_dashboard_completo  
)

router = APIRouter()


@router.get("/notificaciones/verificar_gmail")
def ruta_verificar_gmail(
    correo_token: str = Depends(verificar_autenticacion)
):
    """Endpoint para verificar que la conexión con Gmail API funciona"""
    return verificar_conexion_gmail()


@router.post("/notificaciones/enviar_html")
def ruta_enviar_html(
    correo,
    correo_token: str = Depends(verificar_autenticacion)
):
    generar_dashboard_completo(correo)
    return enviar_archivo(correo, "services/Archivos_HTML/salida.html")


@router.post("/notificaciones/enviar_codigo")
def ruta_enviar_codigo(
    correo,
    correo_token: str = Depends(verificar_autenticacion)
):
    return enviar_archivo(correo, None)
