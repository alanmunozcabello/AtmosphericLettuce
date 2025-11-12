from services.usuarios_service import (
    service_leer_usuarios,
    service_obtener_info_cultivo,
    guardar_clima_semanal
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
                    # 1️⃣ RECOPILAR DATOS DE TODOS LOS CULTIVOS
                    cultivos_info = []  # Info completa de cada cultivo
                    clima = None  # Para el correo HTML (primer clima obtenido)
                    
                    for cultivo_nombre in usuario["cultivos"].keys():
                        info_cultivo = service_obtener_info_cultivo(
                            correo, cultivo_nombre
                        )
                        
                        # Obtener clima usando el primer punto del cultivo
                        if info_cultivo.get("puntos"):
                            puntos = json.loads(info_cultivo["puntos"])
                            primer_punto = next((p for p in puntos if p is not None), None)
                            
                            if primer_punto:
                                # Obtener clima para ESTE cultivo específico
                                clima_response = clima_semana_service(
                                    primer_punto["latitud"],
                                    primer_punto["longitud"]
                                )
                                clima_cultivo = (clima_response.get("data", {})
                                        if clima_response.get("success") else {})
                                
                                # Guardar clima de ESTE cultivo
                                if clima_cultivo:
                                    guardar_clima_semanal(
                                        correo=correo,
                                        cultivo_nombre=cultivo_nombre,
                                        latitud=primer_punto["latitud"],
                                        longitud=primer_punto["longitud"],
                                        clima_dict=clima_cultivo
                                    )
                                    print(f"✅ Clima guardado para {cultivo_nombre}")
                                    
                                    # Usar el primer clima obtenido para el HTML
                                    if not clima:
                                        clima = clima_cultivo
                        
                        # Agregar info del cultivo a la lista
                        cultivos_info.append({
                            "nombre": cultivo_nombre,
                            "info": info_cultivo
                        })
                    
                    # Si no se pudo obtener clima de cultivos, usar ubicación del usuario
                    if not clima:
                        clima_response = clima_semana_service(
                            usuario["ubicacion"]["latitud"],
                            usuario["ubicacion"]["longitud"]
                        )
                        clima = (clima_response.get("data", {})
                                if clima_response.get("success") else {})
                    
                    # 2️⃣ GENERAR CONSEJOS (1 sola llamada a DeepSeek con TODOS los cultivos)
                    consejos = []
                    for cultivo_data in cultivos_info:
                        consejo = deepseek_para_correos(cultivo_data["info"])
                        consejos.append({
                            "cultivo": cultivo_data["nombre"],
                            "consejo": consejo
                        })
                    
                    # 3️⃣ GENERAR HTML Y ENVIAR
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