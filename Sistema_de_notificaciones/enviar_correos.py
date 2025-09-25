import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Define los alcances (scopes). Si los modificas, borra el archivo token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def enviar_pdf(destinatario):
    """Función principal para autenticar y enviar el correo."""
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario.
    # Se crea automáticamente la primera vez que se completa la autorización.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si no hay credenciales válidas disponibles, permite que el usuario inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima ejecución
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Llama a la API de Gmail
        service = build('gmail', 'v1', credentials=creds)

        # --- Crea el mensaje del correo ---
        message = MIMEMultipart()
        message['to'] = destinatario
        message['from'] = 'tu_correo@gmail.com'
        message['subject'] = 'Asunto del correo con PDF'


        #--------------------------aqui cambia recordar 
        # Cuerpo del correo
        cuerpo_del_mensaje = 'Hola,\n\nTe envío el documento solicitado.\n\nSaludos.'
        message.attach(MIMEText(cuerpo_del_mensaje, 'plain'))

        # --- Adjunta el archivo PDF ---
        nombre_archivo = 'pdf_modificado.pdf' # Asegúrate que este archivo exista en la carpeta
        
        try:
            with open(nombre_archivo, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {nombre_archivo}',
            )
            message.attach(part)
        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
            return

        # --- Codifica y envía el correo ---
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        # Envía el mensaje
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(f'Correo enviado. Message ID: {send_message["id"]}')

    except HttpError as error:
        print(f'Ocurrió un error: {error}')

def main(destinatario):
    """Función principal para autenticar y enviar el correo con cuerpo HTML."""
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario.
    # Se crea automáticamente la primera vez que se completa la autorización.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si no hay credenciales válidas disponibles, permite que el usuario inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima ejecución
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Llama a la API de Gmail
        service = build('gmail', 'v1', credentials=creds)

        # --- Crea el mensaje del correo ---
        message = MIMEMultipart()
        message['to'] = destinatario
        # IMPORTANTE: Reemplaza con tu dirección de correo electrónico
        message['from'] = 'tu_correo@gmail.com'
        message['subject'] = 'Asunto del correo con cuerpo HTML'

        # --- Carga la plantilla HTML y los estilos CSS desde archivos externos ---
        try:
            # Define las rutas a tus archivos
            ruta_html = os.path.join('Plantilla_HTML', 'index.html')
            ruta_css = os.path.join('Plantilla_HTML', 'estilos.css')
            
            # Lee el contenido de los archivos
            with open(ruta_html, 'r', encoding='utf-8') as f:
                html_template = f.read()
            with open(ruta_css, 'r', encoding='utf-8') as f:
                css_styles = f.read()
            
            # Inyecta el CSS dentro de una etiqueta <style> en el <head> del HTML
            # Esto asegura la máxima compatibilidad con los clientes de correo
            cuerpo_html_final = html_template.replace('</head>', f'<style>{css_styles}</style></head>')

        except FileNotFoundError as e:
            print(f"Error: No se pudo encontrar la plantilla HTML o el archivo CSS.")
            print(f"Detalle del error: {e}")
            return # Detiene la ejecución si no se encuentran los archivos

        # Adjunta el cuerpo HTML final. El segundo parámetro 'html' es crucial.
        message.attach(MIMEText(cuerpo_html_final, 'html'))

        # --- Codifica y envía el correo ---
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        # Envía el mensaje
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(f'Correo enviado. Message ID: {send_message["id"]}')

    except HttpError as error:
        print(f'Ocurrió un error: {error}')
    except FileNotFoundError:
        print("\nERROR: No se encontró el archivo 'credentials.json'.")
        print("Asegúrate de tenerlo en la misma carpeta que este script.")
