import json

#ruta de los usuarios
RUTA_USUARIOS="data/usuarios.json"

def leer_usuarios(): #leer el json y retonar todos los usuarios en un diccionario
    with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivoUsuarios: #r de read y archivoUsuarios es el nombre del archivo abierto
        usuarios=json.load(archivoUsuarios)
    return usuarios

def guardar_nuevo_usuario(nombre, contrasena): #escribe la lista de usuarios en el json

    usuarios=leer_usuarios() #validaciones para registrar un usuario

    if any(usuario["nombre"]==nombre for usuario in usuarios):
        return {"mensaje":"nombre de usuario ya utilizado"}
    nuevo_usuario={"id":len(usuarios)+1, "nombre":nombre, "contrasena":contrasena} #si el usuario o contraseña no existen se crea un nuevo usuario con los parametros de llegada
    usuarios.append(nuevo_usuario)

    with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivoUsuarios: #w de write
        json.dump(usuarios, archivoUsuarios, indent=4, ensure_ascii=False) #indent=4 es para que al guardarlo se vea bonito y no en una sola linea (no e snecesario)
                                                                           #ensure_ascii=Fasle es para guardar de manera legible los caracteres especiales

    return {"mensaje":"usuario registrado correctamente"}