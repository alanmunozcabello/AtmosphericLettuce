import json

#ruta de los usuarios
RUTA_USUARIOS="data/usuarios.json"

def cargar_db(): #cargar la db en un dict
    db = {}
    with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo_usuarios:
        db = json.load(archivo_usuarios)
        return db

def guardar_db(db): #guardar la db en el json
    try:
        with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo_usuarios: #w de write
            json.dump(db, archivo_usuarios, indent=4, ensure_ascii=False) #indent=4 es para que al guardarlo se vea bonito y no en una sola linea (no es necesario)
                                                                          #ensure_ascii=Fasle es para guardar de manera legible los caracteres especiales
    except FileNotFoundError:
        return {"error": "Archivo de usuarios no encontrado"} #si hubo una exception reotrna error