import requests
from dotenv import load_dotenv
import os
# prueba de respuesta de la API
# OBS: funciona bien, dependiendo de la cantidad de infromacion se desmora entre 0.2 y 1.5 segundos

load_dotenv()
API_KEY=os.getenv("OPENWEATHER_API_KEY")

def clima_hora_service(lat, lon): #da clima hora a hora de 4 dias
    url= f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_KEY}"#url de donde se sacará la información del clima
           #aquí despues hay que cambiar la latitud y longitud, eso debe venir del frontend o ser procesada la dirección inicial en el backend

    try:
        respuesta = requests.get(url) #se hace la request
        if respuesta.status_code == 200: #codigo 200 es el estandar de respuesta correcta
            respuesta = respuesta.json() #la respuesta se transforma a un formato legible y manejable (json)
            return respuesta #despues la respuesta se procesará y filtrarán los datos que se requieren y los que no
        else:
            return {"error": respuesta.json} #si no funcionó se muestra el error o se procesa
    except Exception as e: #manejo de errores "potente"
        return "error:", e

def clima_hoy_service(lat, lon): 
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    try:
        respuesta = requests.get(url) 
        if respuesta.status_code == 200: 
            respuesta = respuesta.json() 
            return respuesta 
        else:
            return {"error": respuesta.json()}
    except Exception as e: 
        return "error:", e
    
def clima_semana_service(lat, lon):
    url = f"api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={7}&appid={API_KEY}" #solo este servício no está funcionando

    try:
        respuesta = requests.get(url) 
        if respuesta.status_code == 200: 
            respuesta = respuesta.json() 
            return respuesta 
        else:
            return f"error {respuesta.status_code}: {respuesta.text}"
    except Exception as e: 
        return "error:", e

# llamada de prueba unicamente, luego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
# if __name__ == "__main__":
#     print(clima_hora_service("-35.083414", "-71.082620")) #PASS
#     print(clima_hoy_service("-35", "-71")) #PASS
#     print(clima_semana_service("0", "0")) #PASS