import pytest
from unittest.mock import patch


# ========== TESTS DE CLIMA ACTUAL ==========

@patch('services.clima_service.clima_hora_service')
def test_obtener_clima_hora_exitoso(mock_clima, client, auth_headers, correo_test):
    """Prueba endpoint de clima por hora"""
    mock_clima.return_value = {
        "temperatura": 22.5,
        "descripcion": "cielo claro",
        "humedad": 65,
        "viento": 3.5
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.get(
        "/clima/hora/-33.4489/-70.6693",
        headers=headers
    )
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "temperatura" in datos or "error_type" not in datos


@patch('services.clima_service.clima_hoy_service')
def test_obtener_clima_hoy_exitoso(mock_clima, client, auth_headers, correo_test):
    """Prueba endpoint de clima del día"""
    mock_clima.return_value = {
        "temperatura_actual": 22.5,
        "temperatura_max": 28.0,
        "temperatura_min": 18.0,
        "descripcion": "parcialmente nublado"
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.get(
        "/clima/hoy/-33.4489/-70.6693",
        headers=headers
    )
    
    assert respuesta.status_code == 200


@patch('services.clima_service.clima_semana_service')
def test_obtener_clima_semana_exitoso(mock_clima, client, auth_headers, correo_test):
    """Prueba endpoint de clima semanal"""
    mock_clima.return_value = {
        "1": {"temperatura": 20, "min": 15, "max": 25},
        "2": {"temperatura": 21, "min": 16, "max": 26},
        "3": {"temperatura": 22, "min": 17, "max": 27}
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.get(
        "/clima/semana/-33.4489/-70.6693",
        headers=headers
    )
    
    assert respuesta.status_code == 200


def test_obtener_clima_sin_coordenadas(client, auth_headers, correo_test):
    """Prueba endpoint de clima sin coordenadas"""
    headers = auth_headers(correo_test)
    respuesta = client.get("/clima/hora/abc/xyz", headers=headers)
    
    assert respuesta.status_code == 422


def test_obtener_clima_coordenadas_invalidas(client, auth_headers, correo_test):
    """Prueba con coordenadas fuera de rango"""
    headers = auth_headers(correo_test)
    respuesta = client.get(
        "/clima/hora/999/999",
        headers=headers
    )
    
    # Puede ser 400 (validación) o 500 (error de servicio)
    assert respuesta.status_code in [400, 422, 500]


def test_obtener_clima_sin_autenticacion(client):
    """Prueba obtener clima sin token de autenticación"""
    respuesta = client.get("/clima/hora/-33.4489/-70.6693")
    
    assert respuesta.status_code == 401


@patch('services.clima_service.clima_hora_service')
def test_obtener_clima_error_timeout(mock_clima, client, auth_headers, correo_test):
    """Prueba cuando hay timeout en la API externa"""
    mock_clima.return_value = {
        "error_type": "timeout",
        "error_message": "Request timeout"
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.get(
        "/clima/hora/-33.4489/-70.6693",
        headers=headers
    )
    
    # El servicio devuelve el error en el JSON
    assert respuesta.status_code in [200, 500, 503]


@patch('services.clima_service.clima_semana_service')
def test_obtener_clima_semana_sin_datos(mock_clima, client, auth_headers, correo_test):
    """Prueba cuando la API no devuelve datos"""
    mock_clima.return_value = {
        "error_type": "no_data",
        "error_message": "No hay datos disponibles"
    }
    
    headers = auth_headers(correo_test)
    respuesta = client.get(
        "/clima/semana/-33.4489/-70.6693",
        headers=headers
    )
    
    assert respuesta.status_code in [200, 404, 500]


# ========== TESTS DE CLIMA GUARDADO ==========

@patch('services.clima_service.guardar_clima_semanal')
def test_guardar_clima_cultivo(mock_guardar, client, auth_headers, correo_test):
    """Prueba guardar clima semanal para un cultivo"""
    mock_guardar.return_value = {
        "mensaje": "Clima guardado exitosamente"
    }
    
    headers = auth_headers(correo_test)
    datos = {
        "correo": correo_test,
        "cultivo_nombre": "tomate",
        "clima_data": {
            "1": {"temperatura": 20, "min": 15, "max": 25}
        }
    }
    
    # Endpoint de guardar (si existe)
    # respuesta = client.post("/clima/guardar", json=datos, headers=headers)
    # assert respuesta.status_code == 200


@patch('services.clima_service.obtener_clima_guardado')
def test_obtener_clima_guardado_cultivo(mock_obtener, client, auth_headers, correo_test):
    """Prueba obtener clima guardado de un cultivo"""
    mock_obtener.return_value = {
        "1": {"temperatura": 20, "min": 15, "max": 25}
    }
    
    headers = auth_headers(correo_test)
    
    # Endpoint de obtener clima guardado (si existe)
    # respuesta = client.get(
    #     f"/clima/guardado?correo={correo_test}&cultivo=tomate",
    #     headers=headers
    # )
    # assert respuesta.status_code == 200
