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

    return service_obtener_usuario_para_frontend(correo)


def controller_registrar_usuario(correo, nombre, contrasena):
    # guardar un nuevo usario -> llama al servicio
    # si nombre, contraseña y correo son minimamente validos se
    # llama al servicio
    # estructura minima de correo con expresiones regulares
    if not correo or not nombre or not contrasena:
        return {
            "success": False,
            "error": "Campos incompletos"
        }

    correo = correo.strip().lower()
    nombre = nombre.strip()
    contrasena = contrasena.strip()

    if not nombre or not contrasena:
        return {
            "success": False,
            "error": "Los campos no pueden estar vacíos"
        }

    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"
    if not re.match(patron_email, correo):
        return {
            "success": False,
            "error": "Formato de correo inválido"
        }

    if len(contrasena) < 6 or len(contrasena) > 25:
        return {
            "success": False,
            "error": "La contraseña debe tener entre 6 y 25 caracteres"
        }

    patron_password = (
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])"
        r"[A-Za-z\d@$!%*?&]{6,25}$"
    )
    if not re.match(patron_password, contrasena):
        return {
            "success": False,
            "error": ("La contraseña debe contener al menos una letra "
                      "mayúscula, una letra minúscula, un número y un "
                      "carácter especial")
        }

    if len(nombre) < 1 or len(nombre) > 60:
        return {
            "success": False,
            "error": "El nombre debe tener entre 1 y 60 caracteres"
        }

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
        return {
            "success": False,
            "error": "El nombre solo puede contener letras y espacios"
        }

    return service_registrar_usuario(correo, nombre, contrasena)


def controller_obtener_cultivos_usuario(correo):
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

    return service_obtener_cultivos_usuario(correo)


def controller_eliminar_cultivo(correo, cultivo):
    if not correo or not correo.strip():
        return {
            "success": False,
            "error": "El correo es obligatorio"
        }

    if not cultivo or not cultivo.strip():
        return {
            "success": False,
            "error": "El nombre del cultivo es obligatorio"
        }

    correo = correo.strip().lower()
    cultivo = cultivo.strip()

    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"
    if not re.match(patron_email, correo):
        return {
            "success": False,
            "error": "Formato de correo inválido"
        }

    return service_eliminar_cultivo(correo, cultivo)


# funcion no tan necesaria, el frontend puede saltarse esta
# y llamar directamente a service_obtener_usuario(correo)
def controller_iniciar_sesion(correo, contrasena):
    # suponer que las validaciones y gestion de inicio de sesion
    # se hacen en el frontend
    if not correo or not contrasena:
        return {
            "success": False,
            "error": "Correo y contraseña son obligatorios"
        }

    correo = correo.strip().lower()

    if not correo or not contrasena.strip():
        return {
            "success": False,
            "error": "Correo y contraseña no pueden estar vacíos"
        }

    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"
    if not re.match(patron_email, correo):
        return {
            "success": False,
            "error": "Formato de correo inválido"
        }

    return service_iniciar_sesion(correo, contrasena)


def controller_modificar_usuario(correo, usuarioMOD):
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

    usuario_dict = usuarioMOD.dict(exclude_unset=True)

    if not usuario_dict:
        return {
            "success": False,
            "error": "No hay datos para actualizar"
        }

    if "nombre" in usuario_dict:
        nombre = usuario_dict["nombre"].strip()

        if not nombre:
            return {
                "success": False,
                "error": "El nombre no puede estar vacío"
            }

        if len(nombre) < 1 or len(nombre) > 60:
            return {
                "success": False,
                "error": "El nombre debe tener entre 1 y 60 caracteres"
            }

        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            return {
                "success": False,
                "error": "El nombre solo puede contener letras y espacios"
            }

        usuario_dict["nombre"] = nombre

    if "ciudad" in usuario_dict:
        ciudad = usuario_dict["ciudad"].strip()

        # ciudad solo puede tener letras y espacios
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", ciudad):
            if ciudad == "":
                usuario_dict["ciudad"] = ciudad
            else:
                return {
                    "success": False,
                    "error": ("El nombre de ciudad solo puede contener "
                              "letras y espacios")
                }

        usuario_dict["ciudad"] = ciudad

    if "region" in usuario_dict:
        region = usuario_dict["region"].strip()

        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", region):
            if region == "":
                usuario_dict["region"] = region
            else:
                return {
                    "success": False,
                    "error": ("El nombre de región solo puede contener "
                              "letras y espacios")
                }

        usuario_dict["region"] = region

    return service_modificar_usuario(correo, usuario_dict)


def controller_modificar_ubicacion_usuario(correo, lat, lon):
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

    if lat is None or lon is None:
        return {
            "success": False,
            "error": "Latitud y longitud son obligatorias"
        }

    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return {
            "success": False,
            "error": "Latitud y longitud deben ser números válidos"
        }

    if not (-90 <= lat <= 90):
        return {
            "success": False,
            "error": "Latitud debe estar entre -90 y 90"
        }

    if not (-180 <= lon <= 180):
        return {
            "success": False,
            "error": "Longitud debe estar entre -180 y 180"
        }

    return service_modificar_ubicacion_usuario(correo, lat, lon)


def controller_modificar_region_ciudad_usuario(correo, region, ciudad):
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

    if region is None and ciudad is None:
        return {
            "success": False,
            "error": "Debe proporcionar al menos región o ciudad"
        }

    if region is not None:
        region = region.strip()

        if region and not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", region):
            return {
                "success": False,
                "error": "Región solo puede contener letras y espacios"
            }

    if ciudad is not None:
        ciudad = ciudad.strip()

        if ciudad and not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", ciudad):
            return {
                "success": False,
                "error": "Ciudad solo puede contener letras y espacios"
            }

    return service_modificar_region_ciudad_usuario(correo, region, ciudad)


def controller_eliminar_usuario(correo):
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

    return service_eliminar_usuario(correo)


def controller_agregar_cultivo(correo, cultivo, hectareas):
    if not correo or not correo.strip():
        return {
            "success": False,
            "error": "El correo es obligatorio"
        }

    if not cultivo or not cultivo.strip():
        return {
            "success": False,
            "error": "El nombre del cultivo es obligatorio"
        }

    if hectareas is None:
        return {
            "success": False,
            "error": "Las hectáreas son obligatorias"
        }

    correo = correo.strip().lower()
    cultivo = cultivo.strip()

    patron_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"
    if not re.match(patron_email, correo):
        return {
            "success": False,
            "error": "Formato de correo inválido"
        }

    patron_cultivo = r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-]+$"
    if not re.match(patron_cultivo, cultivo):
        return {
            "success": False,
            "error": ("Nombre de cultivo solo puede contener letras, "
                      "números, espacios y guiones")
        }

    try:
        hectareas = float(hectareas)
    except (ValueError, TypeError):
        return {
            "success": False,
            "error": "Las hectáreas deben ser un número válido"
        }

    if hectareas <= 0:
        return {
            "success": False,
            "error": "Las hectáreas deben ser mayores a 0"
        }

    if round(hectareas, 2) != hectareas:
        hectareas = round(hectareas, 2)

    return service_agregar_cultivo(correo, cultivo, hectareas)


def controller_modificar_formulario_cultivo(correo, cultivo_datos):
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

    cultivo_dict = cultivo_datos.dict(exclude_unset=True)

    if not cultivo_dict:
        return {
            "success": False,
            "error": "No hay datos para actualizar"
        }

    if "nombre_cultivo" not in cultivo_dict:
        return {
            "success": False,
            "error": "El nombre del cultivo es obligatorio para identificarlo"
        }

    nombre_cultivo = cultivo_dict["nombre_cultivo"].strip()

    if not nombre_cultivo:
        return {
            "success": False,
            "error": "El nombre del cultivo no puede estar vacío"
        }

    cultivo_dict["nombre_cultivo"] = nombre_cultivo

    return service_modificar_formulario_cultivo(correo, cultivo_dict)


def controller_modificar_area_cultivo(correo, area_cultivo_datos):
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

    area_cultivo_dict = area_cultivo_datos.dict()

    if "cultivo" not in area_cultivo_dict:
        return {
            "success": False,
            "error": "El nombre del cultivo es obligatorio"
        }
    nombre_cultivo = area_cultivo_dict["cultivo"].strip()

    if not nombre_cultivo:
        return {
            "success": False,
            "error": "El nombre del cultivo no puede estar vacío"
        }

    area_cultivo_dict["cultivo"] = nombre_cultivo

    return service_modificar_area_cultivo(correo, area_cultivo_dict)


def controller_modificar_notificaciones_usuario(correo, notificaciones):
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

    return service_modificar_notificaciones_usuario(correo, notificaciones)
