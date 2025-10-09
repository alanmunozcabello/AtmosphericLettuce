from fastapi import APIRouter
from controllers.notificaciones_controller import controller_enviar_codigo, controller_enviar_html, controller_enviar_pdf
from controllers.modificadora_notificaciones import controller_modificar_html, controller_modificar_pdf

router=APIRouter()

@router.post("/notificaciones/enviar_pdf")
def ruta_enviar_pdf(correo):
  controller_modificar_pdf(correo)
  return controller_enviar_pdf(correo)

@router.post("/notificaciones/enviar_html")
def ruta_enviar_html(correo):
  controller_modificar_html(correo)
  return controller_enviar_html(correo)

@router.post("/notificaciones/enviar_codigo")
def ruta_enviar_codigo(correo):
  return controller_enviar_codigo(correo)