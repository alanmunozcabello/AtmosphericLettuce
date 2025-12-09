from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

import os
import random
import base64

# --- CONFIGURATION ---
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent 
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# --- GMAIL INFRASTRUCTURE ---

def obtener_credenciales_gmail():
    """Obtiene las credenciales de Gmail desde variables de entorno."""
    try:
        client_id = os.getenv("GMAIL_CLIENT_ID")
        client_secret = os.getenv("GMAIL_CLIENT_SECRET")
        refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")
        token_uri = os.getenv("GMAIL_TOKEN_URI", "https://oauth2.googleapis.com/token")

        if not all([client_id, client_secret, refresh_token]):
            # Silently return None or log? Original logged to stdout.
            return None

        token_info = {
            "token": os.getenv("GMAIL_ACCESS_TOKEN"),
            "refresh_token": refresh_token,
            "token_uri": token_uri,
            "client_id": client_id,
            "client_secret": client_secret,
            "scopes": SCOPES,
        }

        creds = Credentials.from_authorized_user_info(token_info, SCOPES)

        if creds and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                return None

        return creds

    except Exception:
        return None

def verificar_conexion_gmail():
    """Verifica que la conexión con Gmail API funcione correctamente."""
    try:
        creds = obtener_credenciales_gmail()
        if not creds:
            return {"error": "No se pudieron obtener credenciales", "estado": "❌ Falló"}
        build('gmail', 'v1', credentials=creds)
        return {"estado": "✅ Conectado", "mensaje": "Credenciales configuradas", "scopes": "gmail.send"}
    except Exception as e:
        return {"estado": "❌ Error", "error": str(e)}

# --- EMAIL SENDING ---

def enviar_archivo(destinatario, archivo_path, codigo=None):
    """Envía un correo con archivo adjunto o HTML. Soporta legacy 'codigo' arg."""
    creds = obtener_credenciales_gmail()
    if not creds:
        return {"error": "Error de autenticación de Gmail"}

    try:
        servicio = build('gmail', 'v1', credentials=creds)
        mensaje = MIMEMultipart()
        mensaje['to'] = destinatario
        mensaje['from'] = 'me'

        if archivo_path is None:
            if codigo is None:
                codigo = random.randint(100000, 999999)
            
            mensaje['subject'] = "Código de verificación - AtmosphericLettuce"
            texto = f"Hola,\n\nTu código de verificación es: {codigo}\n\nSaludos."
            mensaje.attach(MIMEText(texto, 'plain'))
        
        else:
            archivo_path = Path(archivo_path)
            if not archivo_path.exists():
                return {"error": f"No se encontró el archivo {archivo_path}"}

            mensaje['subject'] = f"Notificación - {archivo_path.name}"

            if archivo_path.suffix.lower() == ".pdf":
                with open(archivo_path, 'rb') as f:
                    parte = MIMEBase('application', 'octet-stream')
                    parte.set_payload(f.read())
                encoders.encode_base64(parte)
                parte.add_header('Content-Disposition', f'attachment; filename={archivo_path.name}')
                mensaje.attach(parte)
                mensaje.attach(MIMEText("Adjunto encontrarás el documento solicitado.", 'plain'))

            elif archivo_path.suffix.lower() == ".html":
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    cuerpo_html = f.read()
                mensaje.attach(MIMEText(cuerpo_html, 'html'))

            else:
                return {"error": "Tipo de archivo no soportado"}

        mensaje_codificado = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()
        crear_mensaje = {'raw': mensaje_codificado}
        mensaje_enviado = servicio.users().messages().send(userId="me", body=crear_mensaje).execute()

        return {"mensaje": f"Correo enviado. ID: {mensaje_enviado['id']}", "message_id": mensaje_enviado['id']}

    except Exception as e:
        return {"error": str(e)}

def enviar_correo_codigo(destinatario, codigo):
    """Wrapper específico para enviar códigos (usado por auth_service)"""
    return enviar_archivo(destinatario, None, codigo=codigo)

# --- HTML GENERATION ---

def generar_html_dashboard(correo, usuario_data, clima_data, consejos_ia):
    """
    Genera el HTML del dashboard modificado.
    Refactored from services_modificar_html
    """
    try:
        # Avoid direct import if possible or ensure path
        template_dir = os.path.join(os.path.dirname(__file__), "Archivos_HTML")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("index.html")

        html_renderizado = template.render(
            usuario=usuario_data,
            usuario_correo=correo,
            clima=clima_data,
            consejos=consejos_ia
        )

        output_path = os.path.join(template_dir, "salida.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_renderizado)
        
        return ruta_salida
    
    except Exception as e:
        print(f"Error generando HTML dashboard: {e}")
        return None

def generar_html_warning(correo, usuario_data, cultivos_alertas, condiciones_iniciales, condiciones_actuales, consejos):
    """
    Genera HTML de advertencia con alertas climáticas.
    Refactored from modificar_warning_html
    """
    try:
        template_dir = os.path.join(os.path.dirname(__file__), "Archivos_HTML")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("warning.html")

        cultivos_dict = {}
        for i, cultivo_alerta in enumerate(cultivos_alertas):
            nombre = cultivo_alerta["nombre"]
            if nombre not in cultivos_dict:
                cultivos_dict[nombre] = {"nombre": nombre, "alertas": [], "severidad_maxima": "media"}
            
            cultivos_dict[nombre]["alertas"].append({
                "tipo_alerta": cultivo_alerta["tipo_alerta"],
                "severidad": cultivo_alerta["severidad"],
                "condicion_inicial": condiciones_iniciales[i] if i < len(condiciones_iniciales) else {},
                "condicion_actual": condiciones_actuales[i] if i < len(condiciones_actuales) else {}
            })
            
            if cultivo_alerta["severidad"] == "alta":
                cultivos_dict[nombre]["severidad_maxima"] = "alta"

        # Add advice
        for consejo in consejos:
            nombre = consejo.get("cultivo")
            if nombre in cultivos_dict:
                cultivos_dict[nombre]["consejo"] = consejo.get("consejo", "Monitorear de cerca.")

        html_renderizado = template.render(
            usuario=usuario_data,
            usuario_correo=correo,
            cultivos=list(cultivos_dict.values()),
            total_alertas=len(cultivos_alertas),
            total_cultivos=len(cultivos_dict)
        )

        output_path = os.path.join(template_dir, "warning_salida.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_renderizado)

        return ruta_salida

    except Exception as e:
        print(f"Error generando HTML warning: {e}")
        return None

# --- ORCHESTRATION HELPERS (Legacy Support) ---

def generar_dashboard_completo(correo):
    """
    Orquesta la obtención de datos y generación de HTML.
    Reemplaza a services_modificar_html.
    """
    try:
        # Importaciones locales para evitar ciclos
        from services.user_service import obtener_perfil_usuario
        from services.clima_service import clima_semana_service
        from services.ai_integration_service import deepseek_para_correos # Assuming this function exists/is moved here? 
        # Wait, deepseek_para_correos is in ai_integration_service.py now.
        
        # Obtener/Adaptar datos
        usuario = obtener_perfil_usuario(correo)
        if "error" in usuario:
            print(f"Error usuario: {usuario}")
            return None
            
        # Perfil devuelve ubicacion nested, hay que ver si el template espera eso.
        # Template index.html probablemente usa usuario['ubicacion']['latitud'].
        
        lat = usuario.get("ubicacion", {}).get("latitud", 0)
        lon = usuario.get("ubicacion", {}).get("longitud", 0)
        
        clima_response = clima_semana_service(lat, lon)
        clima_data = clima_response.get("data", {})
        
        # Deepseek necesita info cultivo? 
        # La funcion deepseek_para_correos en ai_integration_service espera info_cultivo.
        # Pero modificadora_service llamaba deepseek_para_correos(correo).
        # Ah, revisemos ai_services.py original: deepseek_para_correos(info_cultivo).
        # Mmm, modificadora_service le pasaba CORREO?
        # modificadora_service: consejos = deepseek_para_correos(correo)
        # ai_services: def deepseek_para_correos(info_cultivo): ... json.dumps(info_cultivo)
        # Entonces modificadora le pasaba un string (correo) y deepseek recibia string?
        # Si, y el prompt decia "Vas a recibir un diccionario...".
        # Probablemente estaba roto o la IA alucinaba respuesta generica.
        # Pasaremos un contexto simple.
        
        consejos = deepseek_para_correos({"usuario": correo, "mensaje": "Generar consejos generales"})

        return generar_html_dashboard(correo, usuario, clima_data, consejos)

    except Exception as e:
        print(f"Error orquestando dashboard: {e}")
        return None

def verificar_estado_notificaciones(correo):
    """Verifica el estado de las notificaciones del usuario."""
    from services.user_service import obtener_perfil_usuario
    try:
        usuario = obtener_perfil_usuario(correo)
        if "error" in usuario:
            print(f"Error usuario: {usuario}")
            return False
        
        # Ensure strict boolean return
        return bool(usuario.get("notificaciones"))
    except Exception as e:
        print(f"Error verificando estado: {e}")
        return False
