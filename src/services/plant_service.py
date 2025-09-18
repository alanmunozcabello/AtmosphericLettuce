import requests
import base64
import json
from dotenv import load_dotenv
import os
# prueba de respuesta de la API
# OBS: funciona bien, se desmoró aproximadamente 3 segundos, pero logró identificar correctamente la afección de la lechuga

load_dotenv()
API_KEY=os.getenv("CROPHEALTH_API_KEY")

def filtrar_informacion(respuesta):
    es_planta=(respuesta["result"]["is_plant"]["binary"]) #si lo de la imagen es una planta, si no la imagen no se ve claramente

    planta=respuesta["result"]["crop"]["suggestions"][0]["name"] #el primer elemento es el con más posibilidades
    planta_cientifico=respuesta["result"]["crop"]["suggestions"][0]["scientific_name"]
    planta_probabilidad=respuesta["result"]["crop"]["suggestions"][0]["probability"]

    enfermedad=respuesta["result"]["disease"]["suggestions"][0]["name"]
    enfermedad_probabilidad=respuesta["result"]["disease"]["suggestions"][0]["probability"] #el primer elemento es el con más posibilidades
    enfermedad_cientifico=respuesta["result"]["disease"]["suggestions"][0]["scientific_name"]

    respuesta_filtrada={
        "es_planta_probabilidad":es_planta,
        "nombre_planta":planta,
        "nombre_cientifico_planta":planta_cientifico,
        "planta_probabilidad":planta_probabilidad,
        "nombre_enfermedad":enfermedad,
        "nombre_cientifico_enfermedad":enfermedad_cientifico,
        "enfermedad_probabilidad":enfermedad_probabilidad
    }

    return respuesta_filtrada

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
            
            #filtrar informacion
            respuesta_filtrada=filtrar_informacion(respuesta.json())

            return respuesta_filtrada
        else:
            return {"error": {respuesta.text}} #si da error y no se entiende o no s epuede manipular cambiar .text -> .json()
    except Exception as e: #manejo de errores "potente"
        print(str(e))
        return "error:", str(e)


# llamada de prueba unicamente, luego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
# if __name__=="__main__":
#     print(preguntar_enfermedad()) #PASS