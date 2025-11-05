import pytest
from controllers.usuarios_controller import controller_registrar_usuario


def test_registrar_usuario_controller():
    respuesta = controller_registrar_usuario(
        "ejemplo9@lechuga.com",
        "ejemplo",
        "ejemplo1234"
    )
    assert "mensaje" in respuesta
    assert "Usuario registrado exitosamente" in respuesta["mensaje"]
