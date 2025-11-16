import re
from pathlib import Path
from services.notificaciones_service import (
    enviar_archivo,
    verificar_conexion_gmail,
)


def controller_enviar_html(correo):
    if not correo or not correo.strip():
        return {
            "success": False,
            "error": "El correo es obligatorio"
        }

    correo = correo.strip().lower()

    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"
    if not re.match(patron_email, correo):
        return {
            "success": False,
            "error": "Formato de correo inválido"
        }

    html_path = Path("services/Archivos_HTML/salida.html")
    if not html_path.exists():
        return {
            "success": False,
            "error": "Archivo HTML no encontrado. Genere el reporte primero"
        }

    if not html_path.is_file():
        return {
            "success": False,
            "error": "La ruta no es un archivo válido"
        }

    if html_path.stat().st_size == 0:
        return {
            "success": False,
            "error": "El archivo HTML está vacío"
        }

    return enviar_archivo(correo, str(html_path))


def controller_enviar_codigo(correo):
    if not correo or not correo.strip():
        return {
            "success": False,
            "error": "El correo es obligatorio"
        }

    correo = correo.strip().lower()

    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"
    if not re.match(patron_email, correo):
        return {
            "success": False,
            "error": "Formato de correo inválido"
        }

    return enviar_archivo(correo, None)


def controller_verificar_gmail():
    return verificar_conexion_gmail()
