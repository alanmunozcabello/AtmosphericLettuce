import re
from services.modificadora_service import modificar_html
from controllers.usuarios_controller import controller_obtener_usuario
from controllers.clima_controller import clima_semana_controller


def controller_modificar_html(correo):
    if not correo or not correo.strip():
        return {
            "success": False,
            "error": "El correo es obligatorio"
        }

    correo = correo.strip().lower()

    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(patron_email, correo):
        return {
            "success": False,
            "error": "Formato de correo inválido"
        }

    usuario = controller_obtener_usuario(correo)

    if not usuario:
        return {
            "success": False,
            "error": "Usuario no encontrado"
        }

    clima = clima_semana_controller(
        usuario['ubicacion']['latitud'],
        usuario['ubicacion']['longitud'],
    )
    # queda pendiente la logica de la ia
    consejos = ""
    return modificar_html(correo, usuario, clima, consejos)
