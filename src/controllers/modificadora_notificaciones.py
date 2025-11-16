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

    # 2. Sanitizar correo
    correo = correo.strip().lower()

    # 3. Validar formato de correo
    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(patron_email, correo):
        return {
            "success": False,
            "error": "Formato de correo inválido"
        }

    # 4. Obtener datos del usuario
    usuario = controller_obtener_usuario(correo)

    # 5. Validar que el usuario exista y sea válido
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
