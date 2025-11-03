import json
import requests
from dotenv import load_dotenv
import os
import datetime
# prueba de respuesta de la API
# OBS: funciona bien, dependiendo de la cantidad de infromacion se desmora entre 0.2 y 1.5 segundos

load_dotenv()
API_KEY=os.getenv("OPENWEATHER_API_KEY")
TIMEOUT = (10, 30)

def filtrar_informacion_semana(respuesta): #la idea de esta funcion es filtrar la respuesta de la api para obtener solo la info que nos importa
    try:
        respuesta_formateada = {}
        
        dias = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
        }
        
        # Validar que existe "list"
        lista_dias = respuesta.get("list", [])
        if not lista_dias:
            return {
                "success": False,
                "error_type": "no_data",
                "error_message": "No hay datos de clima en la respuesta",
                "status_code": 500
            }
        
        i = 1
        for dia in lista_dias:
            # Acceso seguro a todos los campos
            dt = dia.get("dt")
            if not dt:
                continue  # Saltar este día si no tiene timestamp
            
            fecha = datetime.datetime.fromtimestamp(dt)
            dia_semana_eng = fecha.strftime("%A")
            dia_semana_esp = dias.get(dia_semana_eng, "Desconocido")
            
            # Validar weather
            weather = dia.get("weather", [])
            if weather:
                estado = weather[0].get("main", "Desconocido")
            else:
                estado = "Desconocido"
            
            # Validar temp con valores por defecto
            temp_data = dia.get("temp", {})
            temp = temp_data.get("day", 273.15) - 273.15
            temp_min = temp_data.get("min", 273.15) - 273.15
            temp_max = temp_data.get("max", 273.15) - 273.15
            
            respuesta_formateada[str(i)] = {
                "dia": dia_semana_esp,
                "estado": estado,
                "temp": round(temp, 1),
                "min": round(temp_min, 1),
                "max": round(temp_max, 1)
            }
            
            i += 1
        
        return {
            "success": True,
            "data": respuesta_formateada
        }
        
    except Exception as e:
        return {
            "success": False,
            "error_type": "filtering_error",
            "error_message": f"Error al filtrar clima semanal: {str(e)}",
            "status_code": 500
        }

def filtrar_informacion_dia(respuesta):
    try:
        dias = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
        }
        
        # Acceso seguro a todos los campos
        dt = respuesta.get("dt")
        if not dt:
            return {
                "success": False,
                "error_type": "no_timestamp",
                "error_message": "No se encontró timestamp en la respuesta",
                "status_code": 500
            }
        
        fecha = datetime.datetime.fromtimestamp(dt)
        dia_semana_eng = fecha.strftime("%A")
        dia_semana_esp = dias.get(dia_semana_eng, "Desconocido")
        
        # Validar weather
        weather = respuesta.get("weather", [])
        if weather:
            estado = weather[0].get("main", "Desconocido")
        else:
            estado = "Desconocido"
        
        # Validar main con valores por defecto
        main_data = respuesta.get("main", {})
        temp = main_data.get("temp", 273.15) - 273.15
        temp_min = main_data.get("temp_min", 273.15) - 273.15
        temp_max = main_data.get("temp_max", 273.15) - 273.15
        
        return {
            "success": True,
            "data": {
                "dia": dia_semana_esp,
                "estado": estado,
                "temp": round(temp, 1),
                "min": round(temp_min, 1),
                "max": round(temp_max, 1)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error_type": "filtering_error",
            "error_message": f"Error al filtrar clima del día: {str(e)}",
            "status_code": 500
        }

def filtrar_informacion_hora(respuesta):
    try:
        respuesta_filtrada = {
            "Lunes": [],
            "Martes": [],
            "Miércoles": [],
            "Jueves": [],
            "Viernes": [],
            "Sábado": [],
            "Domingo": []
        }
        
        dias = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
        }
        
        # Validar que existe "list"
        lista_horas = respuesta.get("list", [])
        if not lista_horas:
            return {
                "success": False,
                "error_type": "no_data",
                "error_message": "No hay datos de clima por hora en la respuesta",
                "status_code": 500
            }
        
        for hora_iter in lista_horas:
            # Acceso seguro a timestamp
            dt = hora_iter.get("dt")
            if not dt:
                continue  # Saltar esta hora si no tiene timestamp
            
            fecha = datetime.datetime.fromtimestamp(dt)
            dia_semana_eng = fecha.strftime("%A")
            dia_semana_esp = dias.get(dia_semana_eng, "Desconocido")
            
            # Validar weather
            weather = hora_iter.get("weather", [])
            if weather:
                estado = weather[0].get("main", "Desconocido")
            else:
                estado = "Desconocido"
            
            # Validar main
            main_data = hora_iter.get("main", {})
            temp = main_data.get("temp", 273.15) - 273.15
            humedad = main_data.get("humidity", 0)
            
            # Extraer hora de dt_txt
            dt_txt = hora_iter.get("dt_txt", "")
            if len(dt_txt) >= 16:
                hora = dt_txt[11:16]
            else:
                hora = "00:00"
            
            # Agregar al día correspondiente
            if dia_semana_esp in respuesta_filtrada:
                respuesta_filtrada[dia_semana_esp].append({
                    "hora": hora,
                    "estado": estado,
                    "temp": round(temp, 1),
                    "humedad": humedad
                })
        
        return {
            "success": True,
            "data": respuesta_filtrada
        }
        
    except Exception as e:
        return {
            "success": False,
            "error_type": "filtering_error",
            "error_message": f"Error al filtrar clima por hora: {str(e)}",
            "status_code": 500
        }

def procesar_status_code_error(respuesta):
    if respuesta.status_code == 401: #error de autenticación
        try:
            error_detail = respuesta.json().get("error", {}).get("message", "")
        except:
            error_detail = respuesta.text
        
        print(error_detail)
        return {
            "success": False,
            "error_type": "invalid_api_key",
            "error_message": f"La clave de API no es válida: {error_detail}",
            "status_code": 401
            }
    elif respuesta.status_code == 429: #error de rate limit
        try:
            error_detail = respuesta.json().get("error", {}).get("message", "")
        except:
            error_detail = respuesta.text
        
        print(error_detail)
        return {
            "success": False,
            "error_type": "rate_limit_exceeded",
            "error_message": f"Demasiadas peticiones, intenta en unos minutos: {error_detail}",
            "status_code": 429
        }
    elif 400 <= respuesta.status_code < 500: #otros errores del cliente
        try:
            error_detail = respuesta.json().get("error", {}).get("message", "")
        except:
            error_detail = respuesta.text
        
        print(error_detail)
        return {
            "success": False,
            "error_type": "client_error",
            "error_message": f"Error en la petición: {error_detail}",
            "status_code": respuesta.status_code
        }
    elif 500 <= respuesta.status_code < 600: #errores del servidor
        try:
            error_detail = respuesta.json().get("error", {}).get("message", "")
        except:
            error_detail = respuesta.text
        
        print(error_detail)
        return {
            "success": False,
            "error_type": "server_error",
            "error_message": f"Error del servidor de OpenWeather: {error_detail}",
            "status_code": respuesta.status_code
        }
    else:
        return {
            "success": False,
            "error_type": "unknown_error",
            "error_message": f"Error desconocido: {respuesta.text}",
            "status_code": respuesta.status_code
        }

def clima_hora_service(lat, lon): #da clima hora a hora de 4 dias
    if not API_KEY:
        return {
            "success": False,
            "error_type": "api_key_missing",
            "error_message": "API key no configurada en .env",
            "status_code": 500
        }
    
    if lat is None or lon is None or lat == "" or lon == "":
        return {
            "success": False,
            "error_type": "invalid_coordinates",
            "error_message": "Latitud o longitud inválidas",
            "status_code": 400
        }
    
    url= f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_KEY}"#url de donde se sacará la información del clima
           #aquí despues hay que cambiar la latitud y longitud, eso debe venir del frontend o ser procesada la dirección inicial en el backend

    try:
        respuesta = requests.get(url, timeout=TIMEOUT) #se hace la request
        if respuesta.status_code == 200: #codigo 200 es el estandar de respuesta correcta
            try:
                respuesta_json = respuesta.json()
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error_type": "json_decode_error",
                    "error_message": "Respuesta 200 no es JSON válido",
                    "status_code": 500
                }
    
            # Filtrar la info
            respuesta_filtrada = filtrar_informacion_hora(respuesta_json)
    
            if not respuesta_filtrada.get("success", True):
                return respuesta_filtrada

            return respuesta_filtrada #despues la respuesta se procesará y filtrarán los datos que se requieren y los que no
        else:
            return procesar_status_code_error(respuesta)
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error_type": "timeout",
            "error_message": f"Timeout después de {TIMEOUT}s",
            "status_code": 504
        }
    
    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "error_type": "connection_error",
            "error_message": f"Error de conexión: {str(e)}",
            "status_code": 503
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error_type": "network_error",
            "error_message": f"Error de red: {str(e)}",
            "status_code": 500
        }
    
    except Exception as e:
        return {
            "success": False,
            "error_type": "unexpected_error",
            "error_message": f"Error inesperado: {str(e)}",
            "status_code": 500
        }

def clima_hoy_service(lat, lon): 
    if not API_KEY:
        return {
            "success": False,
            "error_type": "api_key_missing",
            "error_message": "API key no configurada en .env",
            "status_code": 500
        }
    
    if lat is None or lon is None or lat == "" or lon == "":
        return {
            "success": False,
            "error_type": "invalid_coordinates",
            "error_message": "Latitud o longitud inválidas",
            "status_code": 400
        }
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    try:
        respuesta = requests.get(url, timeout=TIMEOUT) 
        if respuesta.status_code == 200: 
            try:
                respuesta_json = respuesta.json()
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error_type": "json_decode_error",
                    "error_message": "Respuesta 200 no es JSON válido",
                    "status_code": 500
                }
    
            # Filtrar la info
            respuesta_filtrada = filtrar_informacion_dia(respuesta_json)
    
            if not respuesta_filtrada.get("success", True):
                return respuesta_filtrada

            return respuesta_filtrada
        else:
            return procesar_status_code_error(respuesta)
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error_type": "timeout",
            "error_message": f"Timeout después de {TIMEOUT}s",
            "status_code": 504
        }
    
    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "error_type": "connection_error",
            "error_message": f"Error de conexión: {str(e)}",
            "status_code": 503
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error_type": "network_error",
            "error_message": f"Error de red: {str(e)}",
            "status_code": 500
        }
    
    except Exception as e:
        return {
            "success": False,
            "error_type": "unexpected_error",
            "error_message": f"Error inesperado: {str(e)}",
            "status_code": 500
        }
    
def clima_semana_service(lat, lon):
    if not API_KEY:
        return {
            "success": False,
            "error_type": "api_key_missing",
            "error_message": "API key no configurada en .env",
            "status_code": 500
        }
    
    if lat is None or lon is None or lat == "" or lon == "":
        return {
            "success": False,
            "error_type": "invalid_coordinates",
            "error_message": "Latitud o longitud inválidas",
            "status_code": 400
        }
    
    url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={7}&appid={API_KEY}" #solo este servício no está funcionando

    try:
        respuesta = requests.get(url, timeout=TIMEOUT) 
        if respuesta.status_code == 200: 
            try:
                respuesta_json = respuesta.json()
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error_type": "json_decode_error",
                    "error_message": "Respuesta 200 no es JSON válido",
                    "status_code": 500
                }
    
            # Filtrar la info
            respuesta_filtrada = filtrar_informacion_semana(respuesta_json)
    
            if not respuesta_filtrada.get("success", True):
                return respuesta_filtrada

            return respuesta_filtrada
        else:
            return procesar_status_code_error(respuesta)
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error_type": "timeout",
            "error_message": f"Timeout después de {TIMEOUT[1]}s",
            "status_code": 504
        }
    
    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "error_type": "connection_error",
            "error_message": f"Error de conexión: {str(e)}",
            "status_code": 503
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error_type": "network_error",
            "error_message": f"Error de red: {str(e)}",
            "status_code": 500
        }
    
    except Exception as e:
        return {
            "success": False,
            "error_type": "unexpected_error",
            "error_message": f"Error inesperado: {str(e)}",
            "status_code": 500
        }

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