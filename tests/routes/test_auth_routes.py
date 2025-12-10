import pytest


def test_validar_token_sin_header(client):
    """Prueba validar token sin enviar header de autorización"""
    respuesta = client.get("/api/validar-token")
    
    assert respuesta.status_code == 401
    assert "Token no proporcionado" in respuesta.json()["detail"]


def test_validar_token_header_invalido(client):
    """Prueba validar token con header inválido (sin Bearer)"""
    respuesta = client.get(
        "/api/validar-token",
        headers={"Authorization": "InvalidFormat"}
    )
    
    assert respuesta.status_code == 401


def test_validar_token_token_invalido(client):
    """Prueba validar token con token inválido"""
    respuesta = client.get(
        "/api/validar-token",
        headers={"Authorization": "Bearer token.invalido.xyz"}
    )
    
    assert respuesta.status_code == 401
    assert "inválido" in respuesta.json()["detail"].lower()


def test_validar_token_exitoso(client, auth_headers, correo_test):
    """Prueba validar token con token válido"""
    headers = auth_headers(correo_test)
    
    respuesta = client.get("/api/validar-token", headers=headers)
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["valido"] is True
    assert datos["correo"] == correo_test


def test_validar_token_expirado(client):
    """Prueba validar token expirado"""
    from datetime import datetime, timedelta
    from jose import jwt
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # Crear token expirado
    payload = {
        "sub": "test@test.com",
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    token_expirado = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    respuesta = client.get(
        "/api/validar-token",
        headers={"Authorization": f"Bearer {token_expirado}"}
    )
    
    assert respuesta.status_code == 401
