import requests
import base64
import json
from dotenv import load_dotenv
import os
# prueba de respuesta de la API
# OBS: funciona bien, se desmoró aproximadamente 3 segundos, pero logró identificar correctamente la afección de la lechuga

load_dotenv()
API_KEY=os.getenv("CROPHEALTH_API_KEY")

def preguntar_enfermedad(imagen):#la imágen viene en formato Base64 -> String desde el frontend

    url = "https://crop.kindwise.com/api/v1/identification" #end point

    headers={'Api-Key': API_KEY, #API
            'Content-Type': 'aplication/json'} #requerido por crop.health
    payload = {
        "images": [imagen],  #lista de imágenes en Base64 (debe ser una lista aunque sea una sola imágen)
    }

    try:
        respuesta = requests.post(url, headers=headers, json=payload) #se hace la request

        if respuesta.status_code==201: #si la respuesta es exitosa se muestra/maneja, tal parece que el code:200 para estos tipos tambien es de error xd
            return respuesta.text 
        else:
            return f"error {respuesta.status_code}: {respuesta.text}"
    except Exception as e: #manejo de errores "potente"
        return "error:", e


# llamada de prueba unicamente, luego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
# if __name__=="__main__":
#     print(preguntar_enfermedad()) #PASS