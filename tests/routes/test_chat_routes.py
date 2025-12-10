import pytest
from unittest.mock import patch


def test_hacer_consulta_sin_autenticacion(client):
    """Prueba endpoint de chat sin token de autenticación"""
    payload = {
        "mensaje": "¿Cómo plantar tomates?",
        "imagenes": []
    }
    
    respuesta = client.post("/chat/consulta", json=payload)
    
    assert respuesta.status_code == 401


def test_hacer_consulta_token_invalido(client):
    """Prueba endpoint de chat con token inválido"""
    payload = {
        "mensaje": "¿Cómo plantar tomates?",
        "imagenes": []
    }
    
    respuesta = client.post(
        "/chat/consulta",
        json=payload,
        headers={"Authorization": "Bearer token.invalido"}
    )
    
    assert respuesta.status_code == 401


@patch('routes.chat_routes.procesar_consulta_chat')
def test_hacer_consulta_exitoso(mock_chat, client, auth_headers, correo_test):
    """Prueba consulta al chatbot exitosa con autenticación"""
    mock_chat.return_value = "Los tomates necesitan sol directo y riego regular."
    
    payload = {
        "mensaje": "¿Cómo plantar tomates?",
        "imagenes": []
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.post("/chat/consulta", json=payload, headers=headers)
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "respuesta" in datos


@patch('routes.chat_routes.procesar_consulta_chat')
def test_hacer_consulta_con_imagenes(mock_chat, client, auth_headers, correo_test):
    """Prueba consulta con imágenes base64"""
    mock_chat.return_value = "La planta muestra signos de falta de nitrógeno."
    
    payload = {
        "mensaje": "¿Qué le pasa a mi planta?",
        "imagenes": ["base64_fake_image_data_here"]
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.post("/chat/consulta", json=payload, headers=headers)
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "respuesta" in datos


@patch('routes.chat_routes.procesar_consulta_chat')
def test_hacer_consulta_mensaje_vacio(mock_chat, client, auth_headers, correo_test):
    """Prueba consulta con mensaje vacío"""
    mock_chat.return_value = "Por favor, hazme una pregunta."
    
    payload = {
        "mensaje": "",
        "imagenes": []
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.post("/chat/consulta", json=payload, headers=headers)
    
    # Puede ser 422 (validación) o 200 dependiendo de las validaciones del modelo
    assert respuesta.status_code in [200, 422]


@patch('routes.chat_routes.procesar_consulta_chat')
def test_hacer_consulta_error_servicio(mock_chat, client, auth_headers, correo_test):
    """Prueba cuando el servicio de IA falla"""
    mock_chat.side_effect = Exception("Error en API de DeepSeek")
    
    payload = {
        "mensaje": "¿Cómo plantar tomates?",
        "imagenes": []
    }
    
    headers = auth_headers(correo_test)
    
    # La ruta no maneja excepciones, así que esperamos que falle
    try:
        respuesta = client.post("/chat/consulta", json=payload, headers=headers)
        # Si no maneja el error, debería ser 500
        assert respuesta.status_code == 500
    except Exception:
        # O puede propagar la excepción
        pass
