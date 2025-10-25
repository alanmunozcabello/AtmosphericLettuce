import re
from services.usuarios_service import service_leer_usuarios, service_registrar_usuario, service_obtener_usuario_para_frontend, service_obtener_cultivos_usuario, service_eliminar_cultivo, service_modificar_usuario, service_modificar_ubicacion_usuario, service_iniciar_sesion, service_modificar_region_ciudad_usuario, service_eliminar_usuario, service_agregar_cultivo, service_modificar_formulario_cultivo, service_modificar_area_cultivo #importar los servicios de usuarios

def controller_obtener_todos_los_usuarios(): #retornar todos los usuarios
    return service_leer_usuarios()

def controller_obtener_usuario(correo):
    return service_obtener_usuario_para_frontend(correo)

def controller_registrar_usuario(correo, nombre, contrasena): #guardar un nuevo usario -> llama al servicio
    if(nombre.strip()!="" and contrasena.strip()!="" and re.match(r"[^@]+@[^@]+\.[^@]+", correo)):#si nombre, contraseña y correo son minimamente validos se llama al servicio
        return service_registrar_usuario(correo, nombre, contrasena)                                               #estructura minima de correo con expresiones regulares -> lpp lo vió venir >:)
    else:
        return {"error": "Campos inválidos"}#se llama al controlador para procese el guardado del nuevo usuario
    
def controller_obtener_cultivos_usuario(correo):
    return service_obtener_cultivos_usuario(correo)

# def controller_agregar_o_modificar_cultivo(correo, cultivo, hectareas, fecha_siembra=None, notas=None, 
#     etapa_planta=None, tipo_riego=None, ultimo_riego=None,
#     frecuencia_riego=None, humedad_suelo=None, textura_suelo=None,
#     variedad_planta=None, estado_planta=None, estres_hidrico=None,
#     profundidad_radical=None, densidad_plantacion=None, tipo_sensor=None,
#     eficiencia_riego=None, caudal=None, ph_agua=None, acolchado=None):
#     return service_agregar_o_modificar_cultivo(
#         correo, cultivo, hectareas, fecha_siembra, notas, 
#         etapa_planta, tipo_riego, ultimo_riego, frecuencia_riego, 
#         humedad_suelo, textura_suelo, variedad_planta, estado_planta, 
#         estres_hidrico, profundidad_radical, densidad_plantacion, 
#         tipo_sensor, eficiencia_riego, caudal, ph_agua, acolchado
#     )

def controller_eliminar_cultivo(correo, cultivo):
    return service_eliminar_cultivo(correo, cultivo)

#funcion no tan necesaria, el frontend puede saltarse esta y llamar directamente a service_obtener_usuario(correo)
def controller_iniciar_sesion(correo, contrasena): #suponer que las validaciones y gestion de inicio de sesion se hacen en el frontend
    return service_iniciar_sesion(correo, contrasena)
    #return service_obtener_usuario(correo)

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