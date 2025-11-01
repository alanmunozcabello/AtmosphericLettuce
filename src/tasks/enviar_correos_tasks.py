from services.usuarios_service import service_leer_usuarios
from services.notificaciones_service import enviar_archivo
from services.modificadora_service import modificar_html
from services.clima_service import clima_semana_service



def enviar_correos_a_todos():
  usuarios_data = service_leer_usuarios()
  for correo in usuarios_data.keys():
    try: 
        usuario=usuarios_data[correo]
        clima=clima_semana_service(usuario["ubicacion"]["latitud"],usuario["ubicacion"]["longitud"])
        modificar_html(correo,usuario,clima,"")
        enviar_archivo(correo,"services/Archivos_HTML/salida.html")
    except Exception as e:
        print(f"Error al procesar el correo {correo}: {e}")
        continue    
    