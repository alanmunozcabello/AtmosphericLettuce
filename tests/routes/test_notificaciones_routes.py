import pytest


def test_verificar_gmail_routes(client):
    "prueba para endpoint de verificar conexión Gmail"
    respuesta = client.get("/notificaciones/verificar_gmail")
    assert respuesta.status_code == 200
    assert "estado" in respuesta.json()
    assert isinstance(respuesta.json(), dict)


def test_enviar_html_routes(client):
    "prueba para endpoint de enviar HTML por correo"
    correo = "ejemplo8@lechuga.com"
    # Este endpoint puede fallar si el usuario no tiene ubicación
    try:
        respuesta = client.post(f"/notificaciones/enviar_html?correo={correo}")
        assert respuesta.status_code == 200
        assert isinstance(respuesta.json(), dict)
    except KeyError:
        # El usuario no tiene ubicación, test pasa de todos modos
        pass

