from services.notificaciones_service import enviar_archivo




def controller_enviar_pdf(correo):
    return enviar_archivo(correo,"services/Archivos_pdf/pdf_modificado.pdf") 

def controller_enviar_html(correo):
    return enviar_archivo(correo,"services/Archivos_HTML/salida.html")

def controller_enviar_codigo(correo):
    return enviar_archivo(correo,None)
           
  