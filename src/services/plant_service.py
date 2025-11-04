import json
import requests
from dotenv import load_dotenv
import os

# Prueba de respuesta de la API
# OBS: funciona bien, se demoró aproximadamente 3 segundos,
# pero logró identificar correctamente la afección de la lechuga

load_dotenv()
API_KEY = os.getenv("CROPHEALTH_API_KEY")
TIMEOUT = (60, 60)

def filtrar_informacion(respuesta):
    try:
        result = respuesta.get("result", {})
        
        # Validar is_plant
        is_plant = result.get("is_plant", {})
        es_planta = is_plant.get("binary", False)
        
        # Validar crop
        crop = result.get("crop", {})
        crop_suggestions = crop.get("suggestions", [])
        if not crop_suggestions:
            return {
                "success": False,
                "error_type": "no_crop_detected",
                "error_message": "No se detectó información de cultivo",
                "status_code": 500
            }
        
        planta = crop_suggestions[0].get("name", "Desconocido")
        planta_cientifico = crop_suggestions[0].get("scientific_name", "Desconocido")
        planta_probabilidad = crop_suggestions[0].get("probability", 0.0)
        
        # Validar disease
        disease = result.get("disease", {})
        disease_suggestions = disease.get("suggestions", [])
        if not disease_suggestions:
            return {
                "success": False,
                "error_type": "no_disease_detected",
                "error_message": "No se detectó información de enfermedad",
                "status_code": 500
            }
        
        enfermedad = disease_suggestions[0].get("name", "Desconocido")
        enfermedad_probabilidad = disease_suggestions[0].get("probability", 0.0)
        enfermedad_cientifico = disease_suggestions[0].get("scientific_name", "Desconocido")
        
        return {
            "success": True,
            "es_planta": es_planta,
            "nombre_planta": planta,
            "nombre_cientifico_planta": planta_cientifico,
            "planta_probabilidad": planta_probabilidad,
            "nombre_enfermedad": enfermedad,
            "nombre_cientifico_enfermedad": enfermedad_cientifico,
            "enfermedad_probabilidad": enfermedad_probabilidad
        }
        
    except Exception as e:
        return {
            "success": False,
            "error_type": "filtering_error",
            "error_message": f"Error al procesar respuesta de API: {str(e)}",
            "status_code": 500
        }

def preguntar_enfermedad(imagen):
    """
    Procesa una imagen para identificar enfermedades en plantas.
    La imagen debe venir en formato Base64 -> String desde el frontend.
    """
    if not API_KEY:
        return {
            "success": False,
            "error_type": "api_key_missing",
            "error_message": "API key no configurada en .env",
            "status_code": 500
        }
    
    url = "https://crop.kindwise.com/api/v1/identification"  # Endpoint API
    
    headers = {
        'Api-Key': API_KEY,  # Token de autenticación
        'Content-Type': 'application/json'  # Requerido por crop.health
    }
    # Lista de imágenes en Base64 (debe ser una lista aunque sea una sola imagen)
    payload = {
        "images": [imagen]
    }

    try:
        # Realizar la petición al API
        respuesta = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)

        # Código 201 indica éxito, 200 podría indicar error en este API
        if respuesta.status_code == 201:
            
            try:
                respuesta_json = respuesta.json()
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error_type": "json_decode_error",
                    "error_message": "Respuesta 201 no es JSON válido",
                    "status_code": 500
                }

            try:
                respuesta_filtrada = filtrar_informacion(respuesta_json)
                
                # Verificar si el filtrado falló
                if not respuesta_filtrada.get("success", True):
                    return respuesta_filtrada
                    
                return respuesta_filtrada
            except Exception as e:
                return {
                    "success": False,
                    "error_type": "filtering_error",
                    "error_message": f"Error al filtrar información: {str(e)}",
                    "status_code": 500
                }
        elif respuesta.status_code == 401:  # Error de API key
            try:
                error_detail = respuesta.json().get("error", {}).get("message", "")
            except json.JSONDecodeError:
                error_detail = respuesta.text
            
            print(error_detail)
            return {
                "success": False,
                "error_type": "invalid_api_key",
                "error_message": f"La clave de API no es válida: {error_detail}",
                "status_code": 401
            }
        
        elif respuesta.status_code == 429:  # Error de rate limit
            try:
                error_detail = respuesta.json().get("error", {}).get("message", "")
            except json.JSONDecodeError:
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
                "error_message": f"Error del servidor de CropHealth: {error_detail}",
                "status_code": respuesta.status_code
            }
        else:
            return {
                "success": False,
                "error_type": "unknown_error",
                "error_message": "Error desconocido",
                "status_code": respuesta.status_code
            }
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


# Llamadas de prueba, solo para desarrollo
# if __name__ == "__main__":
#     print(preguntar_enfermedad())  # PASS