# src/services/security.py
import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

# Configuración razonable por defecto, ajustar si hace falta
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2, hash_len=32)

def hash_password_simple(password: str) -> str:
    return ph.hash(password)

def verify_password(hash, password):
    try:
        if ph.verify(hash, password):
            print("Contraseña correcta")
            return True
    except VerifyMismatchError:
        print("Contraseña incorrecta")
        return False
    # Opcional: si cambias parámetros, puedes actualizar el hash:
    if ph.check_needs_rehash(hash):
        new_hash = ph.hash(password)
        # guarda new_hash en la BD