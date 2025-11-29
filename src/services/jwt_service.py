from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from pathlib import Path

# Cargar .env desde la raíz del proyecto (un nivel arriba de src/)
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("❌ ERROR: SECRET_KEY no está definida en el archivo .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutos de duración (estándar)


def crear_token(correo: str) -> str:
    """Genera un JWT con el correo del usuario"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": correo,
        "exp": expire
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str) -> Optional[str]:
    """Verifica el token y devuelve el correo si es válido"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        return correo if correo else None
    except JWTError:
        return None
