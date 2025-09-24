import json

def cargar_db(): #cargar la db en un dict
    db = {}
    with open("usuarios.json", "r") as f:
        db = json.load(f)
        return db

def guardar_db(db): #guardar la db en el json
    with open("usuarios.json", "w") as f:
        json.dump(db, f, indent=2)