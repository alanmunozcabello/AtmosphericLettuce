import json

#ruta de los usuarios
RUTA_USUARIOS="data/usuarios.json"

def guardar_usuarios(usuarios):
    try:

        with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo_usuarios: #w de write
            json.dump(usuarios, archivo_usuarios, indent=4, ensure_ascii=False) #indent=4 es para que al guardarlo se vea bonito y no en una sola linea (no es necesario)
                                                                            #ensure_ascii=Fasle es para guardar de manera legible los caracteres especiales
        return {"mensaje":"usuario registrado correctamente"}
        
    except FileNotFoundError:
        return {"error": "Archivo de usuarios no encontrado"}

def service_leer_usuarios(): #leer el json y retonar todos los usuarios en un diccionario
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo_usuarios: #r de read y archivoUsuarios es el nombre del archivo abierto
            usuarios=json.load(archivo_usuarios)
        return usuarios
    except FileNotFoundError: #en caso de que el archivo no se encuentre
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError: #en caso de que haya un error de escritura en el json
        return {"error": "Archivo JSON corrupto"}

def service_guardar_nuevo_usuario(correo, nombre, contrasena): #escribe la lista de usuarios en el json

    usuarios=service_leer_usuarios() #validaciones para registrar un usuario

    try:

        if any(usuario["nombre"]==nombre or usuario["id"]==correo for usuario in usuarios):
            return {"error":"nombre de usuario o correo ya utilizado"}
        nuevo_usuario={"id":correo ,"nombre":nombre, "contrasena":contrasena} #si el usuario o contraseña no existen se crea un nuevo usuario con los parametros de llegada
        usuarios.append(nuevo_usuario) #ahora el id es el correo -> mucho mejor y se puede implementar eliminación de usuarios (no necesarios pero se podría ahora)

        return guardar_usuarios(usuarios)
    
    except FileNotFoundError: #si algo falla en service_leer_usuarios() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}
    
def service_obtener_usuario(correo): #retorna toda la informacion de un usuario en concreto
    try:
        usuarios = service_leer_usuarios() #recolectar todos los usuarios
        
        for usuario in usuarios: #iterar en cada usuario buscando por el id unico (correo)
            if usuario["id"] == correo:
                return usuario
            
        return {"error": "Usuario no encontrado"} #si no se encuentra retornar error
    except FileNotFoundError: #si algo falla en service_leer_usuarios() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}
    
def service_obtener_cultivos_usuario(correo): #se obtienen todos los cultivos de un usuario, puede que posteriormente venga del frontend-----
    try:
        usuario=service_obtener_usuario(correo)
        return usuario["cultivos"]
    
    except FileNotFoundError: #si algo falla en service_obtener_usuario() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}

def service_agregar_o_modificar_cultivo(correo, cultivo, herctareas): #se agrega el cultivo si no está, y si está se modifica -> tal vez ver si es mejor separar las funciones y permitir tener cultivos repetidos (puede que el usuario tenga 2 campos de maiz con distintas hectareas en cada campo)
    try:                                                              #puede que despues esta funcion desaparezca y quede solo la de service_modificar_usuario()
        usuario=service_obtener_usuario(correo)

        usuario["cultivos"][cultivo]=herctareas #-> crea cultivo : hectareas, si ya está en el diccionario lo modifica
        return {"mensaje": "cultivo" + cultivo + " guardado exitosamente"}

    except FileNotFoundError: #si algo falla en service_obtener_usuario() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}

def service_eliminar_cultivo(correo, cultivo): #busca un cultivo por el nombre y lo elimina -> tal vez sea util
    try:
        usuario=service_obtener_usuario(correo)

        usuario["cultivos"].pop(cultivo)
        return {"mensaje": "cultivo "+ cultivo + " eliminado exitosamente"}
    
    except FileNotFoundError: #si algo falla en service_obtener_usuario() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}

def service_modificar_usuario(correo, usuarioMOD): #suponiendo que del frontend viene la infromación completa del usuario ya verificada y lista en formato dict, osea json
    try:
        usuarios=service_leer_usuarios() #arreglo de diccionarios con todos los usuarios

        #del arreglo usuarios hay que reemplazar al usuario con el id=correo por el usuarioMOD
        longitud=len(usuarios)

        if isinstance(usuarioMOD, str):  
            usuarioMOD = json.loads(usuarioMOD)
        
        i=0
        while(i<longitud):#iterar sobre cada usuario hasta encontrar el que se desea modificar
            if(usuarios[i]["id"]==correo):
                print(i)
                usuarios[i]=usuarioMOD #reemplazar el usuario antiguo por el modificado
                break
            i+=1 #no olvidar el i+=1 porfavor :cccccc

        guardar_usuarios(usuarios)

        return {"mensaje":"usuario modificado exitosamente"}
    
    except FileNotFoundError: #tomar las excepciones que puedan saltar de service_leer_usuarios()
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return{"error": e}