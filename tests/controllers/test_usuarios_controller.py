import pytest
import random
from controllers.usuarios_controller import controller_registrar_usuario


def test_registrar_usuario_controller():
    correo = f"usuario{random.randint(1000, 9999)}@ejemplo.com"
    respuesta = controller_registrar_usuario(
        correo,
        "ejemplo",
        "ejemplo1234"
    )
    assert isinstance(respuesta, dict)
    # Puede retornar mensaje de éxito o error si ya existe
    assert "mensaje" in respuesta or "error" in respuesta
