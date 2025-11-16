from services.usuarios_service import (
    service_leer_usuarios,
    service_obtener_info_cultivo,
    guardar_clima_semanal,
    service_obtener_usuario_para_frontend
)
from services.notificaciones_service import enviar_archivo
from services.modificadora_service import ( 
    modificar_html,
    modificar_warning_html
)
from services.clima_service import clima_semana_service
from services.ai_services import deepseek_para_correos
from tasks.sistema_de_alertas import analizar_condiciones_adversas
import json


def enviar_correos_a_todos():
    usuarios_data = service_leer_usuarios()
    for correo in usuarios_data.keys():
        usuario = usuarios_data[correo]
        if usuarios_data[correo]["notificaciones"]:
            if not len(usuarios_data[correo]["cultivos"]) == 0:
                try:
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
                    
                    consejos = []
                    for cultivo_data in cultivos_info:
                        consejo = deepseek_para_correos(cultivo_data["info"])
                        consejos.append({
                            "cultivo": cultivo_data["nombre"],
                            "consejo": consejo
                        })
            
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
            

def verificar_y_enviar_alertas_diarias():
    """Verifica condiciones adversas y envía correos de alerta si es necesario"""
    
    print("🔍 Iniciando verificación de condiciones adversas...")
    usuarios_data = service_leer_usuarios()
    
    for correo in usuarios_data.keys():
        usuario = usuarios_data[correo]
        
       
        if not usuario.get("notificaciones"):
            print(f"⏭️  {correo}: notificaciones desactivadas")
            continue
        
        if len(usuario.get("cultivos", {})) == 0:
            print(f"⏭️  {correo}: sin cultivos")
            continue
        
        try:
            
            resultado = analizar_condiciones_adversas(correo)
            
            if not resultado.get("success"):
                print(f"❌ Error al analizar {correo}: {resultado.get('error')}")
                continue
            
            alertas = resultado.get("alertas", [])
            
            
            if len(alertas) > 0:
                print(f"⚠️  {correo}: {len(alertas)} alerta(s) detectada(s)")
                
                
                consejos = []
                for alerta in alertas:
                   # usar deepseek--------------------------
                    consejo_texto = (
                        f"Alerta para {alerta['cultivo']}: {alerta['tipo_alerta']}. "
                        f"Se recomienda monitorear de cerca las condiciones y tomar medidas preventivas."
                    )
                    consejos.append({
                        "cultivo": alerta["cultivo"],
                        "consejo": consejo_texto,
                        "alerta": alerta["tipo_alerta"]
                    })
                
           
                enviar_correos_de_advertencia(correo, usuario, alertas, consejos)
                print(f"✅ Correo de alerta enviado a {correo}")
            else:
                print(f"✓ {correo}: sin alertas")
                
        except Exception as e:
            print(f"❌ Error al procesar alertas para {correo}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print("✅ Verificación de alertas completada\n")


def enviar_correos_de_advertencia(correo, usuario, alertas, consejos):
    """Envía correo con alertas de condiciones adversas"""
    try:
        
        cultivos_alertas = []
        condiciones_iniciales = []
        condiciones_actuales = []
        
        for alerta in alertas:
            cultivos_alertas.append({
                "nombre": alerta["cultivo"],
                "tipo_alerta": alerta["tipo_alerta"],
                "severidad": alerta["severidad"]
            })
            condiciones_iniciales.append(alerta.get("clima_inicial", {}))
            condiciones_actuales.append(alerta.get("clima_actual", {}))
        
        # Modificar HTML con las alertas
        modificar_warning_html(
            correo,
            usuario,
            cultivos_alertas,
            condiciones_iniciales,
            condiciones_actuales,
            consejos
        )
        
        # Enviar el correo
        enviar_archivo(
            correo, 
            "services/Archivos_HTML/warning_salida.html"
        )
        
    except Exception as e:
        print(f"❌ Error al enviar correo de advertencia a {correo}: {e}")
        raise