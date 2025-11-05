import pytest
from services.usuarios_service import service_registrar_usuario


def test_registrar_usuario_service():
    respuesta = service_registrar_usuario(
        "ejemplo7@lechuga.com",
        "ejemplo",
        "ejemplo1234"
    )
    assert "mensaje" in respuesta
    assert "Usuario registrado exitosamente" in respuesta["mensaje"]
