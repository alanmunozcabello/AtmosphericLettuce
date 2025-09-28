import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PATH = "Tokens/token.json"
CREDENTIALS_PATH = "Tokens/credentials.json"


def enviar_archivo(destinatario, archivo_path):
    """Envía un correo a 'destinatario' con un archivo adjunto o HTML según su extensión."""
    archivo_path = Path(archivo_path)

    # Validar que el archivo exista
    if not archivo_path.exists():
        print(f"❌ No se encontró el archivo en {archivo_path}")
        return

    creds = None
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    except Exception:
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEMultipart()
        message['to'] = destinatario
        message['from'] = 'tu_correo@gmail.com'
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
