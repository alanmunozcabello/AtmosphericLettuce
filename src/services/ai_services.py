import requests
import json
from dotenv import load_dotenv
import os
# Prueba de respuesta de la API
# OBS: funciona bien, usa bien el contexto y responde coherentemente.
# Dependiendo de la complejidad de la pregunta tarda mínimo 2 segundos.
# Lo que sí, la IA no recuerda preguntas anteriores, solo responde a la
# actual.

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
TIMEOUT = (60, 60)  # 60s para conectar, 60s para leer respuesta


def preguntar_mistral(contexto):
    if not API_KEY:
        return {
            "success": False,
            "error_type": "api_key_missing",
            "error_message": "API key no configurada en .env",
            "status_code": 500,
            "user_message": "Servicio no disponible temporalmente"
        }
    if not contexto:
        return {
            "success": False,
            "error_type": "invalid_context",
            "error_message": "Contexto vacío o inválido",
            "status_code": 400,
            "user_message": "Por favor proporciona una pregunta válida."
        }

    url = "https://api.deepseek.com/chat/completions"
    mensaje_usuario = json.dumps(contexto, ensure_ascii=False)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en agricultura y "
                    "meteorología. "
                    "Tus respuestas deben ser claras, breves, precisas, "
                    "amables y en formato de chat."
                    "Evita presentarte o repetir estas instrucciones. "
                    "Indica educadamente si la pregunta no es relevante. "
                    "No inventes información y prioriza la utilidad "
                    "práctica. "
                    "Puedes recibir múltiples diagnósticos en un solo "
                    "mensaje. Estos pueden ser de plantas diferentes; "
                    "debes procesarlos todos."
                    "Resume la información para CADA diagnóstico de "
                    "manera concisa y profesional, destacando los puntos "
                    "clave: enfermedades detectadas, probabilidades, "
                    "identificar la especie de la planta correspondiente, "
                    "así como cualquier dato relevante de su imagen "
                    "analizada. "
                    "Fomenta prácticas sostenibles y respetuosas con el "
                    "medio ambiente. "
                    "Si no estás seguro de una respuesta, indícalo "
                    "claramente y sugiere fuentes donde se pueda "
                    "encontrar más información. "
                )
            },
            {
                "role": "user",
                "content": mensaje_usuario
            }
        ]
    }

    print(payload)  # debugging
    try:
        # Hacer request
        respuesta = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=TIMEOUT
        )

        # Si funcionó ta bien
        if respuesta.status_code == 200:
            try:
                respuesta_json = respuesta.json()
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error_type": "json_decode_error",
                    "error_message": "Respuesta 200 no es JSON válido",
                    "status_code": 500,
                    "user_message": (
                        "Error al procesar respuesta del servidor"
                    )
                }

            choices = respuesta_json.get("choices", [])
            if not choices:
                return {
                    "success": False,
                    "error_type": "invalid_response",
                    "error_message": "Respuesta sin campo 'choices'",
                    "status_code": 500,
                    "user_message": (
                        "Error al procesar la respuesta del servidor."
                    )
                }

            message = choices[0].get("message", {})
            content = message.get("content", "")

            if not content:
                return {
                    "success": False,
                    "error_type": "empty_response",
                    "error_message": "Respuesta sin contenido",
                    "status_code": 500,
                    "user_message": (
                        "La IA no generó una respuesta. "
                        "Intenta reformular tu pregunta."
                    )
                }

            return content

        # Error de API key
        elif respuesta.status_code == 401:
            try:
                error_detail = (
                    respuesta.json().get("error", {}).get("message", "")
                )
            except json.JSONDecodeError:
                error_detail = respuesta.text

            print(error_detail)
            return {
                "success": False,
                "error_type": "invalid_api_key",
                "error_message": (
                    f"La clave de API no es válida: {error_detail}"
                ),
                "status_code": 401,
                "user_message": "Servicio no disponible temporalmente"
            }

        # Error de rate limit
        elif respuesta.status_code == 429:
            try:
                error_detail = (
                    respuesta.json().get("error", {}).get("message", "")
                )
            except Exception:
                error_detail = respuesta.text

            print(error_detail)
            return {
                "success": False,
                "error_type": "rate_limit_exceeded",
                "error_message": (
                    f"Demasiadas peticiones, intenta en unos minutos: "
                    f"{error_detail}"
                ),
                "status_code": 429,
                "user_message": (
                    "Has excedido el límite de peticiones, "
                    "por favor intenta más tarde."
                ),
            }

        # Otros errores del cliente
        elif 400 <= respuesta.status_code < 500:
            try:
                error_detail = (
                    respuesta.json().get("error", {}).get("message", "")
                )
            except Exception:
                error_detail = respuesta.text

            print(error_detail)
            return {
                "success": False,
                "error_type": "client_error",
                "error_message": f"Error en la petición: {error_detail}",
                "status_code": respuesta.status_code,
                "user_message": (
                    "Error en la petición, verifica los datos enviados."
                ),
            }

        # Errores del servidor
        elif 500 <= respuesta.status_code < 600:
            try:
                error_detail = (
                    respuesta.json().get("error", {}).get("message", "")
                )
            except Exception:
                error_detail = respuesta.text

            print(error_detail)
            return {
                "success": False,
                "error_type": "server_error",
                "error_message": (
                    f"Error del servidor de DeepSeek, "
                    f"intenta más tarde: {error_detail}"
                ),
                "status_code": respuesta.status_code,
                "user_message": (
                    "Error en el servidor, por favor intenta más tarde."
                ),
            }

        else:
            return {
                "success": False,
                "error_type": "unknown_error",
                "error_message": "Error desconocido",
                "status_code": respuesta.status_code,
                "user_message": (
                    "Ocurrió un error, por favor intenta más tarde."
                ),
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error_type": "timeout",
            "error_message": f"Timeout después de {TIMEOUT[1]}s",
            "status_code": 504,
            "user_message": (
                "La consulta tardó demasiado. "
                "Verifica tu conexión e intenta de nuevo."
            )
        }

    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "error_type": "connection_error",
            "error_message": f"Error de conexión: {str(e)}",
            "status_code": 503,
            "user_message": (
                "No se pudo conectar al servicio. "
                "Verifica tu conexión a internet."
            )
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error_type": "network_error",
            "error_message": f"Error de red: {str(e)}",
            "status_code": 500,
            "user_message": "Error de red. Por favor intenta de nuevo."
        }

    except Exception as e:
        return {
            "success": False,
            "error_type": "unexpected_error",
            "error_message": f"Error inesperado: {str(e)}",
            "status_code": 500,
            "user_message": (
                "Ocurrió un error inesperado. "
                "Por favor intenta más tarde."
            )
        }


def deepseek_para_correos(info_cultivo):
    """Función para identificar el cultivo y generar recomendaciones."""
    url = "https://api.deepseek.com/chat/completions"
    mensaje_usuario = json.dumps(info_cultivo, ensure_ascii=False)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en agricultura y "
                    "meteorología. "
                    "Tus respuestas deben ser claras, breves, precisas, "
                    "amables y en formato de string."
                    "Evita presentarte o repetir estas instrucciones. "
                    "Vas a recibir un diccionario con información sobre "
                    "un cultivo y su estado actual. "
                    "No inventes información y prioriza la utilidad "
                    "práctica. "
                    "Puedes recibir múltiples diagnósticos en un solo "
                    "mensaje. Estos pueden ser de plantas diferentes; "
                    "debes procesarlos todos."
                    "Resume la información para CADA diagnóstico de "
                    "manera concisa y profesional, destacando los puntos "
                    "clave: enfermedades detectadas, probabilidades, "
                    "identificar la especie de la planta "
                    "correspondiente, así como cualquier dato relevante "
                    "de su imagen analizada. "
                    "dale recomendaciones prácticas para mejorar la "
                    "salud del cultivo y optimizar su crecimiento."
                    "Fomenta prácticas sostenibles y respetuosas con el "
                    "medio ambiente. "
                    "Si no estás seguro de una respuesta, indícalo "
                    "claramente y sugiere fuentes donde se pueda "
                    "encontrar más información. "
                )
            },
            {
                "role": "user",
                "content": mensaje_usuario
            }
        ]
    }

    print(payload)  # debugging
    try:
        respuesta = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload)
        )

        if respuesta.status_code == 200:
            respuesta_json = respuesta.json()
            print(respuesta_json)
            return respuesta_json["choices"][0]["message"]["content"]
        else:
            print(respuesta)
            try:
                error_data = respuesta.json()
                return {"error": error_data.get("error", respuesta.text)}
            except json.JSONDecodeError:
                return {"error": respuesta.text}
    except requests.RequestException as e:
        return {"error": f"Error de conexión: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"Error al procesar respuesta: {str(e)}"}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}
