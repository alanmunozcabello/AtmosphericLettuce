from services.notificaciones_service import enviar_archivo, verificar_conexion_gmail

def controller_enviar_html(correo):
    return enviar_archivo(correo,"services/Archivos_HTML/salida.html")

def controller_enviar_codigo(correo):
    return enviar_archivo(correo,None)

def controller_verificar_gmail():
    return verificar_conexion_gmail()
           
  