from services.usuarios_service import leer_usuarios, guardar_usuarios #importar los servicios de usuarios

def obtener_todos_los_usuarios(): #retornar todos los usuarios
    return leer_usuarios()

def guardar_nuevos_usuarios(usuarios): #guardar un nuevo usario -> llama al servicio
    guardar_usuarios(usuarios)