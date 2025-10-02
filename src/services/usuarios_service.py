import json
from services.security import hash_password_simple, verify_password
from services.user_db_services import cargar_db, guardar_db

bandera_db_cargada=False

usuarios={}

def service_cargar_db(): #si la db no está cargada se carga
    global bandera_db_cargada
    global usuarios
    if(bandera_db_cargada is False):
        try: 
            usuarios=cargar_db()

            bandera_db_cargada=True
            #si no retorna nada es porque funcionó, de lo contrario reotrna una exepción
            # return True #si se cargó correctamente
        except FileNotFoundError: #en caso de que el archivo no se encuentre
            return {"error": "Archivo de usuarios no encontrado"}
        except UnicodeDecodeError: #en caso de que haya un error de escritura en el json
            return {"error": "Archivo JSON corrupto"}
        
def formatear_usuario_para_frontend(correo):# retorna  el usuario en el formato que espera el frontend, incluyendo 'id' dentro del diccionario.
    usuario = usuarios.get(correo)
    if not usuario:
        return  {"error": "Usuario no encontrado"}  
    
    # Formateo: agregamos 'id' dentro del dict
    return {"id": correo, **usuario}

def guardar_usuarios():
    try:
        guardar_db(usuarios)

        return True #si se guardó correctamente
        
    except FileNotFoundError:
        return {"error": "Archivo de usuarios no encontrado"} #si hubo una exception reotrna error

def service_leer_usuarios(): #leer el json y retonar todos los usuarios en un diccionario
    try: #cargar base de datos
        # with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo_usuarios: #r de read y archivoUsuarios es el nombre del archivo abierto
        #     usuarios=json.load(archivo_usuarios)
        service_cargar_db()
        return usuarios #si se cargó correctamente la db se retorna el diccionario de usuarios

    except FileNotFoundError: #en caso de que el archivo no se encuentre
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError: #en caso de que haya un error de escritura en el json
        return {"error": "Archivo JSON corrupto"}

def service_registrar_nuevo_usuario(correo, nombre, contrasena): #guardar/registrar un nuevo usuario
    try: #cargar base de datos
        service_cargar_db()
    except FileNotFoundError: #en caso de que el archivo no se encuentre
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError: #en caso de que haya un error de escritura en el json
        return {"error": "Archivo JSON corrupto"}

    contrasena_hasheada = hash_password_simple(contrasena)
    try:

        if correo in usuarios: #validaciones para registrar un usuario
            return {"error":"Correo ya utilizado"}
        
        #cambiar a la hora de sql
        nuevo_usuario={"nombre":nombre, #si el usuario o contraseña no existen se crea un nuevo usuario con los parametros de llegada y el resto se "inicializan" en nulo
                       "contrasena":contrasena_hasheada, 
                       "ubicacion":{"latitud":None, 
                                    "longitud":None,
                                    "ciudad":None,
                                    "region":None}, 
                       "cultivos":{}}
        usuarios[correo]=nuevo_usuario #ahora el id es el correo -> mucho mejor y se puede implementar eliminación de usuarios (no necesarios pero se podría ahora)

        if(guardar_usuarios() is True): #de haberse guardado correctamente
            return {"mensaje": "usuario registrado correctamente"}
        
        return {"error":"No se pudo guardar el nuevo usuario"} #si no se pudo guardar el nuevo usuario
    
    except FileNotFoundError: #si algo falla en service_leer_usuarios() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}
    
def service_obtener_usuario_frontend(correo): #retorna toda la informacion de un usuario en concreto
    try: #cargar base de datos
        service_cargar_db()

        #cambiar a la hora de sql
        usuario=usuarios[correo] #sacar el usuario de la db

        if(usuario is not None): #si el usuario existe se retorna al frontend en el formato que espera
            usuario_formateado=formatear_usuario_para_frontend(correo)
            return usuario_formateado
            
        return {"error": "Usuario no encontrado"} #si no se encuentra retornar error
    except FileNotFoundError: #si algo falla en service_leer_usuarios() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}
    
def service_obtener_cultivos_usuario(correo): #se obtienen todos los cultivos de un usuario, puede que posteriormente venga del frontend-----
    try: #cargar base de datos
        service_cargar_db()

        #cambiar a la hora de sql
        usuario=usuarios[correo] #sacar el usuario de la db -> mucho más rapido de esta nuevo forma!
        return usuario["cultivos"]
    
    except FileNotFoundError: #si algo falla en service_obtener_usuario() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}
    
#puede que despues esta funcion desaparezca y quede solo la de service_modificar_usuario()
def service_agregar_o_modificar_cultivo(correo, cultivo, herctareas): #se agrega el cultivo si no está, y si está se modifica -> tal vez ver si es mejor separar las funciones y permitir tener cultivos repetidos (puede que el usuario tenga 2 campos de maiz con distintas hectareas en cada campo)
    try: #cargar base de datos
        service_cargar_db()
        
        #cambiar a la hora de sql
        #verificar que cultivo entrada.lower no este repetido en los cultivos.lower del usuario
        cultivos_minusculas = [key.lower() for key in usuarios[correo]["cultivos"].keys()]
        if cultivo.lower() in cultivos_minusculas:
            return {"error": "El cultivo ya existe"}

        usuarios[correo]["cultivos"][cultivo]=int(herctareas) #-> crea cultivo : hectareas, si ya está en el diccionario lo modifica
        
        if(guardar_usuarios() is True): #de haberse guardado correctamente
            return {"mensaje": "cultivo" + cultivo + " guardado exitosamente"}
        
        return {"error":"No se pudo guardar el nuevo usuario"} #si no se pudo guardar el nuevo usuario

    except FileNotFoundError: #si algo falla en service_obtener_usuario() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}

def service_eliminar_cultivo(correo, cultivo): #busca un cultivo por el nombre y lo elimina -> tal vez sea util
    try: #cargar base de datos
        service_cargar_db()

        #cambiar a la hora de sql
        usuarios[correo]["cultivos"].pop(cultivo)

        if(guardar_usuarios() is True): #de haberse guardado correctamente
            return {"mensaje": "cultivo" + cultivo + " guardado exitosamente"}
       
        return guardar_usuarios()
    
    except FileNotFoundError: #si algo falla en service_obtener_usuario() se capta cualquiera que sea la exception
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return {"error": e}

def service_modificar_usuario(correo, usuarioMOD): #modifica el nombre, ciudad o region de un usuario
    try: #cargar base de datos
        service_cargar_db()

        #cambiar a la hora de sql
        # correo=usuarioMOD["correo"] #correo del usuario a modificar
        usuarioOG=usuarios[correo] #ussuario original para comparar cambios

        #modificar nombre
        if(usuarioOG["nombre"]!=usuarioMOD.nombre):
            usuarios[correo]["nombre"]=usuarioMOD.nombre

        #modificar ciudad
        if(usuarioOG["ubicacion"]["ciudad"]!=usuarioMOD.ciudad):
            usuarios[correo]["ubicacion"]["ciudad"]=usuarioMOD.ciudad

        #modificar region
        if(usuarioOG["ubicacion"]["region"]!=usuarioMOD.region):
            usuarios[correo]["ubicacion"]["region"]=usuarioMOD.region

        if(guardar_usuarios() is True):
            return {"mensaje":"usuario modificado correctamente"}

        return guardar_usuarios() #-> retorna error
        # return {"mensaje":"usuario modificado exitosamente"}
    
    except FileNotFoundError: #tomar las excepciones que puedan saltar de service_leer_usuarios()
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return{"error": e}
    
def service_modificar_ubicacion_usuario(correo, lat, lon):
    try: #cargar base de datos
        service_cargar_db()

        #cambiar a la hora de sql
        usuarios[correo]["ubicacion"]["latitud"]=float(lat)
        usuarios[correo]["ubicacion"]["longitud"]=float(lon)

        if(guardar_usuarios() is True):
            return {"mensaje":"ubicación modificada correctamente"}

        return guardar_usuarios() #-> retorna error
    
    except FileNotFoundError: #tomar las excepciones que puedan saltar de service_modificar_usuario()
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return{"error": e}
    
def service_iniciar_sesion(correo_entrada, contrasena_entrada):
    try:#cargar base de datos
        service_cargar_db()

        #cambiar a la hora de sql
        datos_usuario = usuarios.get(correo_entrada)
        if not datos_usuario:  #no encontró el usuario
            return {"error": "Usuario no encontrado"}

        hash_guardado_o_claro = datos_usuario.get("contrasena")

        # Bandera de verificación de contraseña
        contraseña_valida = False
        if hash_guardado_o_claro:
            # Ve si el hash coincide con la contraseña
            if verify_password(hash_guardado_o_claro, contrasena_entrada):
                contraseña_valida = True

        if not contraseña_valida:
            return {"error": "Contraseña incorrecta"}

        # Sanitizar: no devolver la contraseña, ni el hash al frontend
        usuario_sin_credenciales = {clave: valor for clave, valor in datos_usuario.items() if clave != "contrasena"}
        usuario_sin_credenciales["id"] = correo_entrada  # útil para el frontend

        return {"id":correo_entrada, **usuario_sin_credenciales}
        
    except FileNotFoundError: #tomar las excepciones que puedan saltar de service_modificar_usuario
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return{"error": e}

def service_modificar_region_ciudad_usuario(correo, region, ciudad):
    try: #cargar base de datos
        service_cargar_db()
    
        #cambiar a la hora de sql
        usuarios[correo]["ubicacion"]["ciudad"]=ciudad
        usuarios[correo]["ubicacion"]["region"]=region
        if(guardar_usuarios() is True):
            return {"mensaje":"ubicación modificada correctamente"}
        
        return guardar_usuarios() #-> retorna error
    
    except FileNotFoundError: #tomar las excepciones que puedan saltar de service_modificar_usuario()
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return{"error": e}
    
def service_eliminar_usuario(correo):
    try: #cargar base de datos
        service_cargar_db()

        #cambiar a la hora de sql
        usuarios.pop(correo)
        if(guardar_usuarios() is True): #de haberse guardado correctamente
            return {"mensaje" : "Usuario " + correo + " eliminado"}
        
        return guardar_usuarios()

    except FileNotFoundError: #tomar las excepciones que puedan saltar de service_modificar_usuario()
        return {"error": "Archivo de usuarios no encontrado"}
    except UnicodeDecodeError:
        return {"error": "Archivo JSON corrupto"}
    except Exception as e:
        return{"error": e}