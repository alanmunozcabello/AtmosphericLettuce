from services.usuarios_service import (
    service_leer_usuarios,
    service_obtener_info_cultivo
)
from services.notificaciones_service import enviar_archivo
from services.modificadora_service import modificar_html
from services.clima_service import clima_semana_service
from services.ai_services import deepseek_para_correos
import json


def enviar_correos_a_todos():
    usuarios_data = service_leer_usuarios()
    for correo in usuarios_data.keys():
        usuario = usuarios_data[correo]
        if usuarios_data[correo]["notificaciones"]:
            if not len(usuarios_data[correo]["cultivos"]) == 0:
                try:
                    # Generar consejos para todos los cultivos
                    consejos = []
                    clima = None
                    
                    for cultivo_nombre in usuario["cultivos"].keys():
                        info_cultivo = service_obtener_info_cultivo(
                            correo, cultivo_nombre
                        )
                        
                        # Obtener clima usando el primer punto del cultivo
                        if info_cultivo.get("puntos"):
                            puntos = json.loads(info_cultivo["puntos"])
                            # Buscar el primer punto válido (no None)
                            primer_punto = next((p for p in puntos if p is not None), None)
                            
                            if primer_punto and not clima:
                                # Obtener clima solo una vez con el primer cultivo
                                clima_response = clima_semana_service(
                                    primer_punto["latitud"],
                                    primer_punto["longitud"]
                                )
                                clima = (clima_response.get("data", {})
                                        if clima_response.get("success") else {})
                        
                        # Generar consejo para este cultivo
                        consejo = deepseek_para_correos(info_cultivo)
                        consejos.append({
                            "cultivo": cultivo_nombre,
                            "consejo": consejo
                        })
                    
                    # Si no se pudo obtener clima de cultivos, usar ubicación del usuario
                    if not clima:
                        clima_response = clima_semana_service(
                            usuario["ubicacion"]["latitud"],
                            usuario["ubicacion"]["longitud"]
                        )
                        clima = (clima_response.get("data", {})
                                if clima_response.get("success") else {})
                    
                    modificar_html(correo, usuario, clima, consejos)
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


def enviar_correos_warning():
    
    
    
    