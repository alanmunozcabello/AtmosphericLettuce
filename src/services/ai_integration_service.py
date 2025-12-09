import requests
import json
import base64
import fitz  # PyMuPDF
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

from services.user_service import obtener_perfil_usuario
from services.cultivo_service import obtener_detalle_cultivo
from services.clima_service import clima_semana_service

# Load .env
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
PLANT_API_KEY = os.getenv("CROPHEALTH_API_KEY")
TIMEOUT = (60, 60)

# --- PLANT ID (Computer Vision) ---

def preguntar_enfermedad(imagen_base64: str) -> Dict[str, Any]:
    """Identifica enfermedades en plantas usando CropHealth API"""
    if not PLANT_API_KEY:
        return {"success": False, "error_message": "API Key no configurada"}

    url = "https://crop.kindwise.com/api/v1/identification"
    headers = {'Api-Key': PLANT_API_KEY, 'Content-Type': 'application/json'}
    payload = {"images": [imagen_base64]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
        
        if response.status_code == 201:
            try:
                data = response.json()
                return _filtrar_informacion_planta(data)
            except json.JSONDecodeError:
                return {"success": False, "error_message": "Respuesta inválida"}
        else:
             return {"success": False, "status_code": response.status_code, "error_message": response.text}

    except Exception as e:
        return {"success": False, "error_message": str(e)}

def _filtrar_informacion_planta(data: Dict) -> Dict[str, Any]:
    """Helper privado para limpiar respuesta de PlantID"""
    try:
        resultado = data.get("result", {})
        es_planta = resultado.get("is_plant", {}).get("binary", False)
        
        sugerencias = resultado.get("crop", {}).get("suggestions", [])
        if not sugerencias:
             return {"success": False, "error_message": "No se detectó cultivo"}
        
        nombre_planta = sugerencias[0].get("name", "Desconocido")
        
        sug_enfermedad = resultado.get("disease", {}).get("suggestions", [])
        nombre_enfermedad = sug_enfermedad[0].get("name", "Desconocido") if sug_enfermedad else "Saludable"
        
        return {
            "success": True,
            "es_planta": es_planta,
            "nombre_planta": nombre_planta,
            "nombre_enfermedad": nombre_enfermedad,
            "raw": data # Opcional: mantener raw si es necesario
        }
    except Exception as e:
        return {"success": False, "error_message": str(e)}

# --- LLM Service (DeepSeek/Mistral) ---

def preguntar_mistral(contexto: List[Dict]) -> str | Dict:
    """Consulta al LLM con un contexto dado (chat)"""
    if not DEEPSEEK_API_KEY:
        return {"error": "API Key de IA no configurada"}
    
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system", 
                "content": "Eres un asistente experto en agricultura. Responde de forma breve y útil."
            },
            {"role": "user", "content": json.dumps(contexto, ensure_ascii=False)}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
        if response.status_code == 200:
            choices = response.json().get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
        return {"error": f"Error API: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def deepseek_para_correos(info_cultivo: Dict) -> str:
    """Genera consejos para correos basados en info de cultivo"""
    contexto = [{"info_cultivo": info_cultivo, "tarea": "Dar consejos cortos para este cultivo"}]
    # Reutilizamos la lógica de conexión
    respuesta = preguntar_mistral(contexto)
    if isinstance(respuesta, dict):
        return "No se pudieron generar consejos en este momento."
    return respuesta

# --- CHAT ORCHESTRATION ---

def procesar_consulta_chat(payload: Dict[str, Any]) -> str | Dict:
    """
    Procesa el payload del chat (texto, imágenes, pdf) y consulta a la IA.
    Refactored to use new services.
    """
    contexto = []
    
    if payload.get("texto"):
        contexto.append({"mensaje_usuario": payload["texto"]})
        
    if payload.get("imagen"):
        # Asumimos que imagen es una lista de base64 strings
        for img in payload["imagen"]:
            resultado_vision = preguntar_enfermedad(img)
            contexto.append({"analisis_vision": resultado_vision})

    if payload.get("correo") and payload.get("cultivo"):
        # Obtener datos reales del cultivo
        info_cultivo = obtener_detalle_cultivo(payload["correo"], payload["cultivo"])
        
        # Verificar errores
        if "error" not in info_cultivo:
            contexto.append({"info_cultivo": info_cultivo})
            
            # Determinar ubicación para clima
            lat, lon = 0, 0
            # Intentar obtener de puntos del cultivo primero
            puntos = info_cultivo.get("puntos", [])
            if puntos and len(puntos) > 0 and puntos[0]:
                 lat = puntos[0].get("latitud", 0)
                 lon = puntos[0].get("longitud", 0)
            
            if lat == 0:
                # Fallback al perfil de usuario
                perfil = obtener_perfil_usuario(payload["correo"])
                if "error" not in perfil:
                    # Perfil devuelve ubicacion nested
                    ubicacion = perfil.get("ubicacion", {})
                    lat = ubicacion.get("latitud", 0)
                    lon = ubicacion.get("longitud", 0)
            
            # Obtener clima
            clima = clima_semana_service(lat, lon)
            contexto.append({"clima_actual": clima})

    if payload.get("pdf"):
        for pdf_b64 in payload["pdf"]:
            try:
                # Decodificar y extraer texto
                datos_pdf = base64.b64decode(pdf_b64)
                doc = fitz.open(stream=datos_pdf, filetype="pdf")
                texto_pdf = ""
                for pagina in doc:
                    texto_pdf += pagina.get_text() + "\n"
                contexto.append({"contenido_pdf": texto_pdf})
            except Exception as e:
                contexto.append({"error_pdf": str(e)})

    return preguntar_mistral(contexto)
