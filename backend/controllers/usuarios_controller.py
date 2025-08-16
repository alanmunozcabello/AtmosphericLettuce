from services.usuarios_service import leer_usuarios #importar los servicios de usuarios

def obtener_todos_los_usuarios(): #retornar todos los usuarios
    return leer_usuarios()