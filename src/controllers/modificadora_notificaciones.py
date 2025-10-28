from services.modificadora_service import modificar_html
from controllers.usuarios_controller import controller_obtener_usuario
from controllers.clima_controller import clima_semana_controller

def controller_modificar_html(correo):
    usuario=controller_obtener_usuario(correo)
    clima=clima_semana_controller(usuario['ubicacion']['latitud'],usuario['ubicacion']['longitud'])
    #queda pendiente la logica de la ia
    consejos=""
    return modificar_html(correo,usuario,clima,consejos)


    
    