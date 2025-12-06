import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

import os
import random

# Cargar variables de entorno desde el directorio raíz del proyecto
# Detectar automáticamente la ruta correcta del .env
current_dir = Path(__file__).resolve().parent  # services/
project_root = current_dir.parent.parent  # AtmosphericLettuce/
env_path = project_root / '.env'

load_dotenv(dotenv_path=env_path)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def obtener_credenciales_gmail():
    """Obtiene las credenciales de Gmail desde variables de entorno."""
    try:
        # Verificar que las variables existan
        client_id = os.getenv("GMAIL_CLIENT_ID")
        client_secret = os.getenv("GMAIL_CLIENT_SECRET")
        refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")
        token_uri = os.getenv(
            "GMAIL_TOKEN_URI", "https://oauth2.googleapis.com/token"
        )

        if not all([client_id, client_secret, refresh_token]):
            print("❌ Faltan variables de entorno de Gmail")
            print(f"CLIENT_ID: {'✅' if client_id else '❌'}")
            print(f"CLIENT_SECRET: {'✅' if client_secret else '❌'}")
            print(f"REFRESH_TOKEN: {'✅' if refresh_token else '❌'}")
            return None

        # Crear credenciales desde variables de entorno
        token_info = {
            "token": os.getenv("GMAIL_ACCESS_TOKEN"),
            "refresh_token": refresh_token,
            "token_uri": token_uri,
            "client_id": client_id,
            "client_secret": client_secret,
            "scopes": SCOPES,
        }

        creds = Credentials.from_authorized_user_info(token_info, SCOPES)

        # Renovar token SIEMPRE (por si acaso está expirado)
        if creds and creds.refresh_token:
            print("🔄 Refrescando token de Gmail...")
            try:
                creds.refresh(Request())
                print("✅ Token refrescado exitosamente")
            except Exception as refresh_error:
                print(f"❌ Error al refrescar token: {refresh_error}")
                return None

        return creds

    except Exception as e:
        print(f"❌ Error al obtener credenciales de Gmail: {e}")
        import traceback
        traceback.print_exc()
        return None


def enviar_archivo(destinatario, archivo_path, codigo=None):
    """Envía un correo con archivo adjunto o HTML según extensión."""

    # Obtener credenciales desde variables de entorno
    creds = obtener_credenciales_gmail()

    if not creds:
        print("❌ No se pudieron obtener las credenciales de Gmail")
        return {
            "error": "Error de autenticación de Gmail. "
                     "Verifica las credenciales en .env"
        }

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEMultipart()
        message['to'] = destinatario
        message['from'] = 'me'  # Gmail usa 'me' como remitente autenticado

        # Caso especial: enviar código de verificación (sin archivo)
        if archivo_path is None:
            # Si no se proporciona código, generar uno
            if codigo is None:
                codigo = random.randint(100000, 999999)
            
            message['subject'] = (
                "Código de verificación - AtmosphericLettuce"
            )
            texto = (
                f"Hola,\n\n"
                f"Tu código de verificación es: {codigo}\n\n"
                f"Saludos."
            )
            message.attach(MIMEText(texto, 'plain'))
            print(f"📧 Enviando código {codigo} a {destinatario}")

        else:
            # Procesar archivo
            archivo_path = Path(archivo_path)

            # Validar que el archivo exista
            if not archivo_path.exists():
                error_msg = f"No se encontró el archivo en {archivo_path}"
                print(f"❌ {error_msg}")
                return {"error": error_msg}

            message['subject'] = f"Notificación - {archivo_path.name}"

            # Detectar tipo de archivo
            if archivo_path.suffix.lower() == ".pdf":
                # Adjuntar PDF
                with open(archivo_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={archivo_path.name}',
                )
                message.attach(part)
                texto_pdf = (
                    "Hola,\n\n"
                    "Te envío el documento solicitado de "
                    "AtmosphericLettuce.\n\n"
                    "Saludos."
                )
                message.attach(MIMEText(texto_pdf, 'plain'))
                print(f"📎 Adjuntando PDF: {archivo_path.name}")

            elif archivo_path.suffix.lower() == ".html":
                # Cuerpo HTML
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    cuerpo_html = f.read()
                message.attach(MIMEText(cuerpo_html, 'html'))
                print(f"📄 Enviando HTML: {archivo_path.name}")

            else:
                error_msg = (
                    f"Tipo de archivo no soportado: "
                    f"{archivo_path.suffix}"
                )
                print(f"❌ {error_msg}")
                return {"error": error_msg}

        # Enviar correo
        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()
        create_message = {'raw': encoded_message}
        send_message = (
            service.users().messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        success_msg = (
            f"Correo enviado exitosamente. ID: {send_message['id']}"
        )
        print(f"✅ {success_msg}")
        return {
            "mensaje": success_msg,
            "message_id": send_message['id']
        }

    except HttpError as error:
        error_msg = f"Error HTTP de Gmail: {error}"
        print(f"❌ {error_msg}")
        return {"error": error_msg}

    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return {"error": error_msg}


def verificar_conexion_gmail():
    """Verifica que la conexión con Gmail API funcione correctamente."""
    try:
        creds = obtener_credenciales_gmail()

        if not creds:
            return {
                "error": "No se pudieron obtener credenciales",
                "estado": "❌ Falló"
            }

        # Intentar construir el servicio
        build('gmail', 'v1', credentials=creds)

        # Simplemente verificar que las credenciales funcionan
        # No enviamos realmente, solo verificamos permisos

        return {
            "estado": "✅ Conectado",
            "mensaje": "Credenciales de Gmail configuradas correctamente",
            "scopes": "gmail.send"
        }

    except HttpError as error:
        return {
            "estado": "❌ Error HTTP",
            "error": str(error),
            "mensaje": (
                "Verifica que la API esté habilitada en "
                "Google Cloud Console"
            )
        }

    except Exception as e:
        return {
            "estado": "❌ Error",
            "error": str(e),
            "mensaje": "Error al conectar con Gmail"
        }
