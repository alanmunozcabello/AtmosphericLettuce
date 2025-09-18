import requests
from dotenv import load_dotenv
import os
import datetime
# prueba de respuesta de la API
# OBS: funciona bien, dependiendo de la cantidad de infromacion se desmora entre 0.2 y 1.5 segundos

load_dotenv()
API_KEY=os.getenv("OPENWEATHER_API_KEY")

def filtrar_informacion_semana(respuesta): #la idea de esta funcion es filtrar la respuesta de la api para obtener solo la info que nos importa
    respuesta_formateada={}    
    
    dias = { #diccionario de dias en español, basicamente un traductor
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }

    i=1
    for dia in respuesta["list"]:
        dt=dia["dt"] #dia es una serie de numeros raros
        fecha = datetime.datetime.fromtimestamp(dt) #convertir a objeto datetime
        dia_semana_eng = fecha.strftime("%A") #día de la semana en inglés ("Monday", "Tuesday", ...)
        dia_semana_esp = dias[dia_semana_eng] #ahora queda en español

        estado=dia["weather"][0]["main"]
        temp=dia["temp"]["day"]-273.15 #pasar las temperaturas de kelvin a celcius :p
        temp_min=dia["temp"]["min"]-273.15
        temp_max=dia["temp"]["max"]-273.15

        respuesta_formateada[i]={ #comienza en 1 por dia 1, dia 2, dia 3...
            "dia":dia_semana_esp,
            "estado":estado,
            "temp":temp,
            "min":temp_min,
            "max":temp_max
        }
        
        i+=1

    return respuesta_formateada

def filtrar_informacion_dia(respuesta):
    dias = { #diccionario de dias en español, basicamente un traductor
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
    }

    dt=respuesta["dt"] #dia es una serie de numeros raros
    fecha = datetime.datetime.fromtimestamp(dt) #convertir a objeto datetime
    dia_semana_eng = fecha.strftime("%A") #día de la semana en inglés ("Monday", "Tuesday", ...)
    dia_semana_esp = dias[dia_semana_eng] #ahora queda en español

    estado=respuesta["weather"][0]["main"]
    temp=respuesta["main"]["temp"]-273.15 #pasar las temperaturas de kelvin a celcius :p
    temp_min=respuesta["main"]["temp_min"]-273.15
    temp_max=respuesta["main"]["temp_max"]-273.15

    respuesta_filtrada={
        "dia":dia_semana_esp,
        "estado":estado,
        "temp":temp,
        "min":temp_min,
        "max":temp_max
    }

    return respuesta_filtrada

def filtrar_informacion_hora(respuesta):
    respuesta_filtrada={
        "Lunes":[],
        "Martes":[],
        "Miércoles":[],
        "Jueves":[],
        "Viernes":[],
        "Sábado":[],
        "Domingo":[]
    }

    dias = { #diccionario de dias en español, basicamente un traductor
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
    }

    for hora_iter in respuesta["list"]: #iterar hora por hora, los 4 dias categorizando por dia de la semana
        dt=hora_iter["dt"] #dia es una serie de numeros raros
        fecha = datetime.datetime.fromtimestamp(dt) #convertir a objeto datetime
        dia_semana_eng = fecha.strftime("%A") #día de la semana en inglés ("Monday", "Tuesday", ...)
        dia_semana_esp = dias[dia_semana_eng] #ahora queda en español
  
        estado=hora_iter["weather"][0]["main"]
        temp=hora_iter["main"]["temp"]-273.15 #pasar las temperaturas de kelvin a celcius :p
        humedad=hora_iter["main"]["humidity"] #en porcentaje al apreces :p

        hora=hora_iter["dt_txt"][11:16] #extraer la hora del string ej: "2023-10-05 12:00:00"

        #segun sea el dia de la semana, se agrega al arreglo correspondiente
        if(dia_semana_esp=="Lunes"):
            respuesta_filtrada["Lunes"].append({
                "hora":hora,
                "estado":estado,
                "temp":temp,
                "humedad":humedad
            })
        elif(dia_semana_esp=="Martes"):
            respuesta_filtrada["Martes"].append({
                "hora":hora,
                "estado":estado,
                "temp":temp,
                "humedad":humedad
            })
        elif(dia_semana_esp=="Miércoles"):
            respuesta_filtrada["Miércoles"].append({
                "hora":hora,
                "estado":estado,
                "temp":temp,
                "humedad":humedad
            })
        elif(dia_semana_esp=="Jueves"):
            respuesta_filtrada["Jueves"].append({
                "hora":hora,
                "estado":estado,
                "temp":temp,
                "humedad":humedad
            })
        elif(dia_semana_esp=="Viernes"):
            respuesta_filtrada["Viernes"].append({
                "hora":hora,
                "estado":estado,
                "temp":temp,
                "humedad":humedad
            })
        elif(dia_semana_esp=="Sábado"):
            respuesta_filtrada["Sábado"].append({
                "hora":hora,
                "estado":estado,
                "temp":temp,
                "humedad":humedad
            })
        elif(dia_semana_esp=="Domingo"):
            respuesta_filtrada["Domingo"].append({
                "hora":hora,
                "estado":estado,
                "temp":temp,
                "humedad":humedad
            })
    
    return respuesta_filtrada

def clima_hora_service(lat, lon): #da clima hora a hora de 4 dias
    url= f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_KEY}"#url de donde se sacará la información del clima
           #aquí despues hay que cambiar la latitud y longitud, eso debe venir del frontend o ser procesada la dirección inicial en el backend

    try:
        respuesta = requests.get(url) #se hace la request
        if respuesta.status_code == 200: #codigo 200 es el estandar de respuesta correcta
            respuesta = respuesta.json() #la respuesta se transforma a un formato legible y manejable (json)
            
            #filtrar la info
            respuesta_filtrada=filtrar_informacion_hora(respuesta)
            
            return respuesta_filtrada #despues la respuesta se procesará y filtrarán los datos que se requieren y los que no
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

            #filtrar la info
            respuesta_filtrada=filtrar_informacion_dia(respuesta)

            return respuesta_filtrada 
        else:
            return {"error": respuesta.json()}
    except Exception as e: 
        return "error:", e
    
def clima_semana_service(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={7}&appid={API_KEY}" #solo este servício no está funcionando

    try:
        respuesta = requests.get(url) 
        if respuesta.status_code == 200: 
            respuesta = respuesta.json() 

            #filtrar la info
            respuesta_filtrada=filtrar_informacion_semana(respuesta)

            return respuesta_filtrada
        else:
            return {"error": respuesta.json()}
    except Exception as e: 
        return "error:", e

# llamada de prueba unicamente, luego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
# if __name__ == "__main__":
    ##pruebas de datos es bruto de la api
    # print(clima_hora_service("-35.083414", "-71.082620")) #PASS
    # print(clima_hoy_service("-35", "-71")) #PASS
    # print(clima_semana_service("0", "0")) #PASS

##pruebas de datos filtrados de la api
    # respuesta=clima_semana_service(0,0)
    # print(filtrar_informacion_semana(respuesta))

    # respuesta=clima_hora_service(0,0)
    # print(filtrar_informacion_hora(respuesta))

    # respuesta=clima_hoy_service(0,0)
    # print(filtrar_informacion_dia(respuesta))