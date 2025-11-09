import pytest
import random
from services.usuarios_service import service_registrar_usuario


def test_registrar_usuario_service():
    correo = f"usuario{random.randint(1000, 9999)}@ejemplo.com"
    respuesta = service_registrar_usuario(
        correo,
        "ejemplo",
        "ejemplo1234"
    )
    assert isinstance(respuesta, dict)
    # Puede retornar mensaje de éxito o error si ya existe
    assert "mensaje" in respuesta or "error" in respuesta
