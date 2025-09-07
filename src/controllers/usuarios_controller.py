from services.usuarios_service import leer_usuarios, guardar_nuevo_usuario #importar los servicios de usuarios

def obtener_todos_los_usuarios(): #retornar todos los usuarios
    return leer_usuarios()

def registrar_usuario(correo, nombre, contrasena): #guardar un nuevo usario -> llama al servicio
    if(nombre!="" and nombre!=" " and contrasena!="" and contrasena!=" " and "@" in correo and len(correo)>=5):#si nombre, contraseña y correo son minimamente validos se llama al servicio
        return guardar_nuevo_usuario(correo, nombre, contrasena)                                               #estructura minima de correo: -@-.- len=5
    else:
        return {"mensaje":"nombre y contraseña no pueden estar en blanco"}#se llama al controlador para procese el guardado del nuevo usuario