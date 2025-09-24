# src/services/security.py
import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

# Configuración razonable por defecto, ajustar si hace falta
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2, hash_len=32)

def hash_password_simple(password: str) -> str:
    return ph.hash(password)