import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    """Simula un cliente HTTP para probar tu API"""
    return TestClient(app)