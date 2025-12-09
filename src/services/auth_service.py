from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
import os
from pathlib import Path
import random
import string

import sqlite3
# from services.user_service import usuario_existe, modificar_usuario, get_db_connection (Removed to avoid cycle)
from services.notification_service import enviar_correo_codigo

# --- CONFIGURATION ---
# Load .env
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")

# --- DATABASE HELPERS ---

DB_PATH = "data/DataBase.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

if not SECRET_KEY:
    # Fallback or strict error? Stick to original behavior somewhat but arguably strict is better.
    # Original raised ValueError.
    pass # Will fail later if used

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Password Hashing
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2, hash_len=32)

# --- SECURITY & HASHING ---

def hash_password_simple(contrasena: str) -> str:
    return ph.hash(contrasena)

def verify_password(hash, contrasena):
    try:
        if ph.verify(hash, contrasena):
            return True
    except VerifyMismatchError:
        return False
    if ph.check_needs_rehash(hash):
        return ph.hash(contrasena)

# --- JWT TOKENS ---

def crear_token(correo: str) -> str:
    """Genera un JWT con el correo del usuario"""
    if not SECRET_KEY:
         raise ValueError("SECRET_KEY no configurada")
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos = {
        "sub": correo,
        "exp": expiracion
    }
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str) -> Optional[str]:
    """Verifica el token y devuelve el correo si es válido"""
    if not SECRET_KEY:
        return None
    try:
        carga_util = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = carga_util.get("sub")
        return correo if correo else None
    except JWTError:
        return None

# --- RECOVERY ---

def generar_codigo_recuperacion(correo: str) -> Dict[str, Any]:
    """
    Genera un código, lo guarda en BD y lo envía por correo.
    """
    from services.user_service import usuario_existe
    if not usuario_existe(correo):
        return {"error": "Usuario no encontrado"}

    codigo = ''.join(random.choices(string.digits, k=6))
    expiracion = datetime.now() + timedelta(minutes=15)

    try:
        conn = get_db_connection()
        conn.execute("""
            INSERT OR REPLACE INTO codigos_recuperacion (correo, codigo, expiracion)
            VALUES (?, ?, ?)
        """, (correo, codigo, expiracion))
        conn.commit()
        conn.close()

        # Enviar correo using the NEW notification service eventually, 
        # but for now we import the function we will create in notification_service.
        # Check dependencies: auth_service depends on notification_service.
        from services.notification_service import enviar_correo_codigo
        
        resultado_envio = enviar_correo_codigo(correo, codigo)
        
        if "error" in resultado_envio:
             return {"error": "Error al enviar el correo. Inténtalo más tarde."}

        return {"mensaje": "Código enviado a tu correo"}

    except Exception as e:
        return {"error": str(e)}

def verificar_codigo(correo: str, codigo: str) -> Dict[str, Any]:
    """
    Verifica si el código es válido y no ha expirado.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, expiracion FROM codigos_recuperacion WHERE correo = ?", (correo,))
        resultado = cursor.fetchone()
        conn.close()

        if not resultado:
            return {"valid": False, "error": "No se encontró una solicitud para este correo"}

        codigo_db, expiracion_str = resultado
        
        # Parse expiration
        if isinstance(expiracion_str, str):
            try:
                expiracion = datetime.strptime(expiracion_str, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                expiracion = datetime.strptime(expiracion_str, "%Y-%m-%d %H:%M:%S")
        else:
             expiracion = expiracion_str

        if datetime.now() > expiracion:
            return {"valid": False, "error": "El código ha expirado"}

        if codigo_db != codigo:
            return {"valid": False, "error": "Código incorrecto"}

        return {"valid": True, "mensaje": "Código verificado"}

    except Exception as e:
        return {"valid": False, "error": str(e)}

def cambiar_contrasena_recuperacion(correo: str, codigo: str, nueva_contrasena: str) -> Dict[str, Any]:
    """
    Verifica el código nuevamente y cambia la contraseña.
    """
    validacion = verificar_codigo(correo, codigo)
    if not validacion["valid"]:
        return {"error": validacion.get("error", "Código inválido")}
    
    try:
        conn = get_db_connection()
        nueva_pass_hash = hash_password_simple(nueva_contrasena)
        
        conn.execute("UPDATE usuarios SET contrasena = ? WHERE correo = ?", (nueva_pass_hash, correo))
        
        # Eliminar código usado
        conn.execute("DELETE FROM codigos_recuperacion WHERE correo = ?", (correo,))
        
        conn.commit()
        conn.close()
        
        return {"mensaje": "Contraseña actualizada exitosamente"}
        
    except Exception as e:
        return {"error": str(e)}
