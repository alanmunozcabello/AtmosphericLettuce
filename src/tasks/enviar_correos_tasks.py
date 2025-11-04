from services.usuarios_service import (
    service_leer_usuarios,
    service_obtener_info_cultivo
)
from services.notificaciones_service import enviar_archivo
from services.modificadora_service import modificar_html
from services.clima_service import clima_semana_service
from services.ai_services import deepseek_para_correos


def enviar_correos_a_todos():
    usuarios_data = service_leer_usuarios()
    for correo in usuarios_data.keys():
        usuario = usuarios_data[correo]
        if usuarios_data[correo]["notificaciones"]:
            if not len(usuarios_data[correo]["cultivos"]) == 0:
                try:
                    clima_response = clima_semana_service(
                        usuario["ubicacion"]["latitud"],
                        usuario["ubicacion"]["longitud"]
                    )
                    # Extraer solo los datos del clima
                    clima = (clima_response.get("data", {})
                             if clima_response.get("success") else {})
                    # Obtener el nombre del primer cultivo
                    primer_cultivo_nombre = list(
                        usuario["cultivos"].keys())[0]
                    # Obtener info del primer cultivo
                    info_primer_cultivo = service_obtener_info_cultivo(
                        correo, primer_cultivo_nombre
                    )
                    consejo = deepseek_para_correos(info_primer_cultivo)
                    modificar_html(correo, usuario, clima, consejo)
                    enviar_archivo(
                        correo, "services/Archivos_HTML/salida.html"
                    )
                except Exception as e:
                    print(f"Error al procesar el correo {correo}: {e}")
                    continue
            else:
                print(f"{correo} sin cultivos")
        else:
            print(f"{correo} notificaciones desactivadas")
