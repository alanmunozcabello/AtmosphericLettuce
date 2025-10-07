import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import json
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

import os
import random

# Cargar variables de entorno desde el directorio raíz del proyecto
load_dotenv(dotenv_path='../../.env')

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def obtener_credenciales_gmail():
    """Obtiene las credenciales de Gmail desde variables de entorno."""
    try:
        # Crear credenciales desde variables de entorno
        token_info = {
            "token": os.getenv("GMAIL_ACCESS_TOKEN"),
            "refresh_token": os.getenv("GMAIL_REFRESH_TOKEN"),
            "token_uri": os.getenv("GMAIL_TOKEN_URI"),
            "client_id": os.getenv("GMAIL_CLIENT_ID"),
            "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
            "scopes": SCOPES,
        }
        
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
        
        # Renovar token si ha expirado
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            
        return creds
        
    except Exception as e:
        print(f"❌ Error al obtener credenciales de Gmail: {e}")
        return None


def enviar_archivo(destinatario, archivo_path):
    """Envía un correo a 'destinatario' con un archivo adjunto o HTML según su extensión."""
    
    # Obtener credenciales desde variables de entorno
    creds = obtener_credenciales_gmail()
    
    if not creds:
        print("❌ No se pudieron obtener las credenciales de Gmail")
        return {"error": "Error de autenticación de Gmail"}

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEMultipart()
        message['to'] = destinatario
        message['from'] = 'tu_correo@gmail.com'
        
        # Caso especial: enviar código de verificación (sin archivo)
        if archivo_path is None:
            codigo = random.randint(100000, 999999)
            message['subject'] = "Código de verificación"
            message.attach(MIMEText(f"Hola,\n\nTu código de verificación es: {codigo}\n\nSaludos.", 'plain'))
        
        else:
            # Procesar archivo
            archivo_path = Path(archivo_path)
            
            # Validar que el archivo exista
            if not archivo_path.exists():
                print(f"❌ No se encontró el archivo en {archivo_path}")
                return
                
            message['subject'] = f"Correo con {archivo_path.name}"
            
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
                message.attach(MIMEText("Hola,\n\nTe envío el documento solicitado.\n\nSaludos.", 'plain'))

            elif archivo_path.suffix.lower() == ".html":
                # Cuerpo HTML
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    cuerpo_html = f.read()
                message.attach(MIMEText(cuerpo_html, 'html'))
            
            else:
                print(f"❌ Tipo de archivo no soportado: {archivo_path.suffix}")
                return

        # Enviar correo
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"📩 Correo enviado. Message ID: {send_message['id']}")

    except HttpError as error:
        print(f"Ocurrió un error: {error}")
