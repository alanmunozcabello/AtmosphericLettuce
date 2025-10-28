from fastapi import APIRouter
from controllers.notificaciones_controller import controller_enviar_codigo, controller_enviar_html, controller_verificar_gmail
from controllers.modificadora_notificaciones import controller_modificar_html

router=APIRouter()

@router.get("/notificaciones/verificar_gmail")
def ruta_verificar_gmail():
  """Endpoint para verificar que la conexión con Gmail API funciona"""
  return controller_verificar_gmail()


@router.post("/notificaciones/enviar_html")
def ruta_enviar_html(correo):
  controller_modificar_html(correo)
  return controller_enviar_html(correo)

@router.post("/notificaciones/enviar_codigo")
def ruta_enviar_codigo(correo):
  return controller_enviar_codigo(correo)