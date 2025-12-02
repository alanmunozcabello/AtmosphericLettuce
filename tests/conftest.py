import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from services.jwt_service import crear_token
from app import app

@pytest.fixture
def client():
    """Simula un cliente HTTP para probar tu API"""
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """Headers de autenticación para tests"""
    def _auth_headers(correo: str):
        token = crear_token(correo)
        return {"Authorization": f"Bearer {token}"}
    return _auth_headers

@pytest.fixture
def correo_test():
    """Correo de prueba por defecto"""
    return "ejemplo8@lechuga.com"