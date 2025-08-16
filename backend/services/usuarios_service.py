import json

#ruta de los usuarios
RUTA_USUARIOS="data/usuarios.json"

def leer_usuarios(): #leer el json y retonar todos los usuarios en un diccionario
    with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivoUsuarios: #r de read y archivoUsuarios es el nombre del archivo abierto
        usuarios=json.load(archivoUsuarios)
    return usuarios

def guardar_usuarios(usuarios): #escribe la lista de usuarios en el json
    with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivoUsuarios: #w de write
        json.dump(usuarios, archivoUsuarios, indent=4, ensure_ascii=False) #indent=4 es para que al guardarlo se vea bonito y no en una sola linea (no e snecesario)
                                                                           #ensure_ascii=Fasle es para guardar de manera legible los caracteres especiales