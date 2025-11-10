import re
from services.usuarios_service import (
    service_leer_usuarios,
    service_registrar_usuario,
    service_obtener_usuario_para_frontend,
    service_obtener_cultivos_usuario,
    service_eliminar_cultivo,
    service_modificar_usuario,
    service_modificar_ubicacion_usuario,
    service_iniciar_sesion,
    service_modificar_region_ciudad_usuario,
    service_eliminar_usuario,
    service_agregar_cultivo,
    service_modificar_formulario_cultivo,
    service_modificar_area_cultivo,
    service_modificar_notificaciones_usuario,
)


def controller_obtener_todos_los_usuarios():
    # retornar todos los usuarios
    return service_leer_usuarios()


def controller_obtener_usuario(correo):
    return service_obtener_usuario_para_frontend(correo)


def controller_registrar_usuario(correo, nombre, contrasena):
    # guardar un nuevo usario -> llama al servicio
    # si nombre, contraseña y correo son minimamente validos se
    # llama al servicio
    # estructura minima de correo con expresiones regulares
    if (nombre.strip() != "" and contrasena.strip() != "" and
            re.match(r"[^@]+@[^@]+\.[^@]+", correo)):
        return service_registrar_usuario(correo, nombre, contrasena)
    else:
        return {"error": "Campos inválidos"}


def controller_obtener_cultivos_usuario(correo):
    return service_obtener_cultivos_usuario(correo)


def controller_eliminar_cultivo(correo, cultivo):
    return service_eliminar_cultivo(correo, cultivo)


# funcion no tan necesaria, el frontend puede saltarse esta
# y llamar directamente a service_obtener_usuario(correo)
def controller_iniciar_sesion(correo, contrasena):
    # suponer que las validaciones y gestion de inicio de sesion
    # se hacen en el frontend
    return service_iniciar_sesion(correo, contrasena)
    # return service_obtener_usuario(correo)


def controller_modificar_usuario(correo, usuarioMOD):
    usuario_dict = usuarioMOD.dict()
    return service_modificar_usuario(correo, usuario_dict)


def controller_modificar_ubicacion_usuario(correo, lat, lon):
    return service_modificar_ubicacion_usuario(correo, lat, lon)


def controller_modificar_region_ciudad_usuario(correo, region, ciudad):
    return service_modificar_region_ciudad_usuario(correo, region, ciudad)


def controller_eliminar_usuario(correo):
    return service_eliminar_usuario(correo)


def controller_agregar_cultivo(correo, cultivo, hectareas):
    return service_agregar_cultivo(correo, cultivo, hectareas)


def controller_modificar_formulario_cultivo(correo, cultivo_datos):
    cultivo_dict = cultivo_datos.dict()
    return service_modificar_formulario_cultivo(correo, cultivo_dict)


def controller_modificar_area_cultivo(correo, area_cultivo_datos):
    area_cultivo_dict = area_cultivo_datos.dict()
    return service_modificar_area_cultivo(correo, area_cultivo_dict)


def controller_modificar_notificaciones_usuario(correo, notificaciones):
    return service_modificar_notificaciones_usuario(correo, notificaciones)
