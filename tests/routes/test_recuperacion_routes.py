import pytest
from unittest.mock import patch


@patch('routes.recuperacion_routes.generar_codigo_recuperacion')
def test_solicitar_recuperacion_correo_valido(mock_generar, client):
    """Prueba solicitar código de recuperación con correo válido"""
    payload = {
        "correo": "ejemplo8@lechuga.com"
    }
    
    mock_generar.return_value = {
        "mensaje": "Código enviado a tu correo"
    }
    
    respuesta = client.post("/api/recuperacion/solicitar", json=payload)
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "mensaje" in datos


@patch('routes.recuperacion_routes.generar_codigo_recuperacion')
def test_solicitar_recuperacion_correo_invalido(mock_generar, client):
    """Prueba solicitar recuperación con correo que no existe"""
    payload = {
        "correo": "noexiste@ejemplo.com"
    }
    
    mock_generar.return_value = {
        "error": "Usuario no encontrado"
    }
    
    respuesta = client.post("/api/recuperacion/solicitar", json=payload)
    
    assert respuesta.status_code == 400


def test_solicitar_recuperacion_sin_correo(client):
    """Prueba solicitar recuperación sin enviar correo"""
    respuesta = client.post("/api/recuperacion/solicitar", json={})
    
    assert respuesta.status_code == 422  # Unprocessable Entity


@patch('routes.recuperacion_routes.verificar_codigo')
def test_verificar_codigo_correcto(mock_verificar, client):
    """Prueba verificar código de recuperación correcto"""
    payload = {
        "correo": "ejemplo8@lechuga.com",
        "codigo": "123456"
    }
    
    mock_verificar.return_value = {
        "valid": True
    }
    
    respuesta = client.post("/api/recuperacion/verificar", json=payload)
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "mensaje" in datos
    assert "válido" in datos["mensaje"].lower()


@patch('routes.recuperacion_routes.verificar_codigo')
def test_verificar_codigo_incorrecto(mock_verificar, client):
    """Prueba verificar código incorrecto"""
    payload = {
        "correo": "ejemplo8@lechuga.com",
        "codigo": "000000"
    }
    
    mock_verificar.return_value = {
        "valid": False,
        "error": "Código incorrecto"
    }
    
    respuesta = client.post("/api/recuperacion/verificar", json=payload)
    
    assert respuesta.status_code == 400


@patch('routes.recuperacion_routes.verificar_codigo')
def test_verificar_codigo_expirado(mock_verificar, client):
    """Prueba verificar código expirado"""
    payload = {
        "correo": "ejemplo8@lechuga.com",
        "codigo": "123456"
    }
    
    mock_verificar.return_value = {
        "valid": False,
        "error": "Código expirado"
    }
    
    respuesta = client.post("/api/recuperacion/verificar", json=payload)
    
    assert respuesta.status_code == 400
    assert "expirado" in respuesta.json()["detail"].lower()


@patch('routes.recuperacion_routes.cambiar_contrasena_recuperacion')
def test_cambiar_contrasena_exitoso(mock_cambiar, client):
    """Prueba cambiar contraseña con código válido"""
    payload = {
        "correo": "ejemplo8@lechuga.com",
        "codigo": "123456",
        "nueva_contrasena": "NuevaPassword123@"
    }
    
    mock_cambiar.return_value = {
        "mensaje": "Contraseña actualizada exitosamente"
    }
    
    respuesta = client.post("/api/recuperacion/cambiar", json=payload)
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "mensaje" in datos


@patch('routes.recuperacion_routes.cambiar_contrasena_recuperacion')
def test_cambiar_contrasena_codigo_invalido(mock_cambiar, client):
    """Prueba cambiar contraseña con código inválido"""
    payload = {
        "correo": "ejemplo8@lechuga.com",
        "codigo": "000000",
        "nueva_contrasena": "NuevaPassword123@"
    }
    
    mock_cambiar.return_value = {
        "error": "Código inválido o expirado"
    }
    
    respuesta = client.post("/api/recuperacion/cambiar", json=payload)
    
    assert respuesta.status_code == 400


def test_cambiar_contrasena_debil(client):
    """Prueba cambiar contraseña con contraseña débil"""
    payload = {
        "correo": "ejemplo8@lechuga.com",
        "codigo": "123456",
        "nueva_contrasena": "123"  # Contraseña muy débil
    }
    
    # Puede fallar en validación del modelo o del servicio
    respuesta = client.post("/api/recuperacion/cambiar", json=payload)
    
    assert respuesta.status_code in [400, 422]


def test_cambiar_contrasena_sin_datos(client):
    """Prueba cambiar contraseña sin enviar datos requeridos"""
    respuesta = client.post("/api/recuperacion/cambiar", json={})
    
    assert respuesta.status_code == 422


@patch('routes.recuperacion_routes.generar_codigo_recuperacion')
@patch('routes.recuperacion_routes.verificar_codigo')
@patch('routes.recuperacion_routes.cambiar_contrasena_recuperacion')
def test_flujo_completo_recuperacion(mock_cambiar, mock_verificar, mock_generar, client):
    """Prueba el flujo completo de recuperación de contraseña"""
    correo = "ejemplo8@lechuga.com"
    
    # Paso 1: Solicitar código
    mock_generar.return_value = {"mensaje": "Código enviado a tu correo"}
    
    respuesta1 = client.post("/api/recuperacion/solicitar", json={"correo": correo})
    assert respuesta1.status_code == 200
    
    # Paso 2: Verificar código
    mock_verificar.return_value = {"valid": True}
    
    respuesta2 = client.post("/api/recuperacion/verificar", json={
        "correo": correo,
        "codigo": "123456"
    })
    assert respuesta2.status_code == 200
    
    # Paso 3: Cambiar contraseña
    mock_cambiar.return_value = {"mensaje": "Contraseña actualizada exitosamente"}
    
    respuesta3 = client.post("/api/recuperacion/cambiar", json={
        "correo": correo,
        "codigo": "123456",
        "nueva_contrasena": "NuevaPassword123@"
    })
    assert respuesta3.status_code == 200
