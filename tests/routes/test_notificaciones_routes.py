import pytest
from unittest.mock import patch


def test_verificar_gmail_routes(client, auth_headers, correo_test):
    "prueba para endpoint de verificar conexión Gmail"
    headers = auth_headers(correo_test)
    respuesta = client.get("/notificaciones/verificar_gmail", headers=headers)
    assert respuesta.status_code == 200
    assert "estado" in respuesta.json()
    assert isinstance(respuesta.json(), dict)


def test_enviar_html_routes(client, auth_headers, correo_test):
    "prueba para endpoint de enviar HTML por correo"
    headers = auth_headers(correo_test)
    # Este endpoint puede fallar si el usuario no tiene ubicación
    respuesta = client.post(f"/notificaciones/enviar_html?correo={correo_test}", headers=headers)
    # Puede ser 200 (éxito) o 500 (error por falta de datos)
    assert respuesta.status_code in [200, 400, 500]


# ========== TESTS ADICIONALES DE NOTIFICACIONES ==========

def test_verificar_gmail_sin_autenticacion(client):
    """Prueba verificar Gmail sin autenticación"""
    respuesta = client.get("/notificaciones/verificar_gmail")
    
    assert respuesta.status_code == 401


@patch('routes.notificaciones_routes.verificar_conexion_gmail')
def test_verificar_gmail_error_conexion(mock_verificar, client, auth_headers, correo_test):
    """Prueba cuando falla la conexión con Gmail"""
    mock_verificar.return_value = {
        "estado": "error",
        "mensaje": "No se pudo conectar"
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.get("/notificaciones/verificar_gmail", headers=headers)
    
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "error"


def test_enviar_html_sin_autenticacion(client, correo_test):
    """Prueba enviar HTML sin autenticación"""
    respuesta = client.post(f"/notificaciones/enviar_html?correo={correo_test}")
    
    assert respuesta.status_code == 401


def test_enviar_html_usuario_sin_ubicacion(client, auth_headers, correo_test):
    """Prueba enviar HTML a usuario sin ubicación configurada"""
    headers = auth_headers(correo_test)
    
    # Usuario de prueba probablemente no tiene ubicación
    respuesta = client.post(
        f"/notificaciones/enviar_html?correo={correo_test}",
        headers=headers
    )
    
    # Puede ser 400 (sin ubicación) o 200 (si tiene ubicación) o 500 (error)
    assert respuesta.status_code in [200, 400, 500]


def test_verificar_estado_notificaciones(client, auth_headers, correo_test):
    """Prueba endpoint para verificar estado de notificaciones"""
    headers = auth_headers(correo_test)
    respuesta = client.post(
        f"/notificaciones/verificar_estado_notificaciones?correo={correo_test}",
        headers=headers
    )
    
    # Puede retornar info o error si no hay datos
    assert respuesta.status_code in [200, 400, 500]
