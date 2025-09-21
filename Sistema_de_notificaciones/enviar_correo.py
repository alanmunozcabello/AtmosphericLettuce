from __future__ import print_function
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Alcance: acceso para enviar correos
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_service():
    creds = None

    # Guardamos sesión en token.pickle para no pedir login siempre
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si no hay credenciales válidas, pedirá login en navegador
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # usa el archivo fijo
            creds = flow.run_local_server(port=0)

        # Guardamos la sesión en token.pickle
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"✅ Mensaje enviado! ID: {message['id']}")
        return message
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == '__main__':
    service = get_service()
    sender = "tucorreo@gmail.com"
    to = "destinatario@gmail.com"
    subject = "Correo enviado con la API de Gmail"
    body = "Hola 👋, este es un correo enviado usando la API de Gmail en Python."
    msg = create_message(sender, to, subject, body)
    send_message(service, "me", msg)
