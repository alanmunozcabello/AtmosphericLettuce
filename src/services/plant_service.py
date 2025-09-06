import requests
import base64
import json
from dotenv import load_dotenv
import os
# prueba de respuesta de la API
# OBS: funciona bien, se desmoró aproximadamente 3 segundos, pero logró identificar correctamente la afección de la lechuga

load_dotenv()
API_KEY=os.getenv("CROPHEALTH_API_KEY")

def preguntar_enfermedad():#POSIBLEMENTE sea mejor pasar la imágen desde el frontend lista como String!!!!!!!!!!! esto elimina la necesidad de guardar la imágen y acceder a ella como archivo
    with open("src/services/botrytis.png", "rb") as imagen: #lechuga.png es la imágen de prueba
        imagen_base64=base64.b64encode(imagen.read()).decode("utf-8") #se abre la imágen en binario y se transforma a string (base64 codificada en utf-8)

    imagen_base64=f"data:image/jpeg;base64,{imagen_base64}" #prefijo necesario para que no explote (requerimiento de crop.health)

    url = "https://crop.kindwise.com/api/v1/identification" #end point

    headers={'Api-Key': API_KEY, #API
            'Content-Type': 'aplication/json'} #requerido por crop.health
    payload = {
        "images": [imagen_base64],  #lista de imágenes en Base64 (debe ser una lista aunque sea una sola imágen)
    }

    try:
        respuesta = requests.post(url, headers=headers, json=payload) #se hace la request

        if respuesta.status_code==200: #si la respuesta es exitosa se muestra/maneja
            return respuesta.text 
        else:
            return f"error {respuesta.status_code}: {respuesta.text}"
    except Exception as e: #manejo de errores "potente"
        return "error:", e


# llamada de prueba unicamente, luego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
if __name__=="__main__":
    print(preguntar_enfermedad()) #PASS