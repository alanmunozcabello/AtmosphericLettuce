import requests
from dotenv import load_dotenv
import os
# prueba de respuesta de la API
# OBS: funciona bien, dependiendo de la cantidad de infromacion se desmora entre 0.2 y 1.5 segundos

load_dotenv()
APY_KEY=os.getenv("OPENWEATHER_API_KEY")

def preguntar_clima(lat, lon): 
    url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={APY_KEY}"#url de donde se sacará la información del clima
           #aquí despues hay que cambiar la latitud y longitud, eso debe venir del frontend o ser procesada la dirección inicial en el backend
    try:
        respuesta = requests.get(url) #se hace la request
        if respuesta.status_code == 200: #codigo 200 es el estandar de respuesta correcta
            respuesta = respuesta.json() #la respuesta se transforma a un formato legible y manejable (json)
            return respuesta #despues la respuesta se procesará y filtrarán los datos que se requieren y los que no
        else:
            return f"error {respuesta.status_code}: {respuesta.text}" #si no funcionó se muestra el error o se procesa
    except Exception as e: #manejo de errores "potente"
        return "error:", e

# llamada de prueba unicamenteluego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
if __name__ == "__main__":
    print(preguntar_clima("-35.083414", "-71.082620")) #PASS
    print(preguntar_clima("-35", "-71")) #PASS
    print(preguntar_clima("0", "0")) #PASS