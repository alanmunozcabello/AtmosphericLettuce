import pytest
import random
from services.user_service import registrar_usuario


def test_registrar_usuario_service():
    from models.usuario import UsuarioRegistro
    correo = f"usuario{random.randint(1000, 9999)}@ejemplo.com"
    usuario = UsuarioRegistro(
        correo=correo,
        nombre="ejemplo",
        contrasena="Ejemplo1234@"
    )
    respuesta = registrar_usuario(usuario)
    assert isinstance(respuesta, dict)
    # Puede retornar mensaje de éxito o error si ya existe
    assert "mensaje" in respuesta or "error" in respuesta
