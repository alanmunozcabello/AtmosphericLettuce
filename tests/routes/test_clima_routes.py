import pytest


def test_clima_hora_routes(client):
    "prueba para endpoint de clima por hora"
    lat = -33.4489
    lon = -70.6693
    respuesta = client.get(f"/clima/hora/{lat}/{lon}")
    assert respuesta.status_code == 200
    assert "success" in respuesta.json()
    assert "data" in respuesta.json()


def test_clima_hoy_routes(client):
    "prueba para endpoint de clima del día"
    lat = -33.4489
    lon = -70.6693
    respuesta = client.get(f"/clima/hoy/{lat}/{lon}")
    assert respuesta.status_code == 200
    assert "success" in respuesta.json()
    assert "data" in respuesta.json()


def test_clima_semana_routes(client):
    "prueba para endpoint de clima de la semana"
    lat = -33.4489
    lon = -70.6693
    respuesta = client.get(f"/clima/semana/{lat}/{lon}")
    assert respuesta.status_code == 200
    assert "success" in respuesta.json()
    assert "data" in respuesta.json()
