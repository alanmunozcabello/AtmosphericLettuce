import json

#ruta de los usuarios
RUTA_USUARIOS="data/usuarios.json"

def leer_usuarios(): #leer el json y retonar todos los usuarios en un diccionario
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo_usuarios: #r de read y archivoUsuarios es el nombre del archivo abierto
            usuarios=json.load(archivo_usuarios)
        return usuarios
    except FileNotFoundError as e: #en caso de que el archivo no se encuentre
        return {"error": e}
    except UnicodeDecodeError as e: #en caso de que haya un error de escritura en el json
        return {"error": e}

def guardar_nuevo_usuario(correo, nombre, contrasena): #escribe la lista de usuarios en el json

    usuarios=leer_usuarios() #validaciones para registrar un usuario

    try:

        if any(usuario["nombre"]==nombre or usuario["correo"]==correo for usuario in usuarios):
            return {"mensaje":"nombre de usuario o correo ya utilizado"}
        nuevo_usuario={"id":len(usuarios)+1,"correo":correo ,"nombre":nombre, "contrasena":contrasena} #si el usuario o contraseña no existen se crea un nuevo usuario con los parametros de llegada
        usuarios.append(nuevo_usuario) #id poco práctico, pero no creo que creemos la funcionalidad de eliminar usuarios.

        try:

            with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo_usuarios: #w de write
                json.dump(usuarios, archivo_usuarios, indent=4, ensure_ascii=False) #indent=4 es para que al guardarlo se vea bonito y no en una sola linea (no es necesario)
                                                                                #ensure_ascii=Fasle es para guardar de manera legible los caracteres especiales

            return {"mensaje":"usuario registrado correctamente"}
        
        except FileNotFoundError as e:
            return {"error": e}
    
    except Exception as e:
        return {"error": e}