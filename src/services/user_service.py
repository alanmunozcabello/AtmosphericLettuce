import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

from services.auth_service import hash_password_simple, verify_password
from models.usuario import UsuarioRegistro, UsuarioModificado, UsuarioResponse, UbicacionUsuario

import os

# DB_PATH = "data/DataBase.db"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "DataBase.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def usuario_existe(correo: str) -> bool:
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE correo = ?", (correo,))
        existe = cursor.fetchone() is not None
        conexion.close()
        return existe
    except Exception:
        return False

def registrar_usuario(usuario: UsuarioRegistro) -> Dict[str, Any]:
    try:
        if usuario_existe(usuario.correo):
            return {"error": "Usuario ya existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()

        contrasena_hash = hash_password_simple(usuario.contrasena)

        cursor.execute("""
            INSERT INTO usuarios
            (correo, nombre, contrasena, latitud, longitud, ciudad,
            region, foto_perfil, created_at, updated_at, notificaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            usuario.correo, usuario.nombre,
            contrasena_hash, None, None, None, None, None,
            datetime.now().isoformat(), datetime.now().isoformat(), False
        ))
        conexion.commit()
        conexion.close()
        return {"mensaje": "Usuario registrado exitosamente"}

    except Exception as e:
        return {"error": str(e)}

def iniciar_sesion(correo: str, contrasena: str) -> Dict[str, Any]:
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        query = "SELECT contrasena FROM usuarios WHERE correo = ?"
        cursor.execute(query, (correo,))
        resultado = cursor.fetchone()
        conexion.close()

        if not resultado:
            return {"error": "Credenciales incorrectas"}

        contrasena_hash = resultado[0]
        if not verify_password(contrasena_hash, contrasena):
            return {"error": "Credenciales incorrectas"}

        return obtener_perfil_usuario(correo)

    except Exception as e:
        return {"error": str(e)}

def obtener_perfil_usuario(correo: str) -> Dict[str, Any]:
    """
    Obtiene SOLO la información del perfil del usuario, sin cultivos pesados.
    """
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        conexion.close()

        if not usuario:
            return {"error": "Usuario no encontrado"}

        # Mapeo manual o usar Pydantic si se prefiere
        usuario_dict = {
            "id": correo,
            "nombre": usuario[1],
            "ubicacion": {
                "latitud": usuario[3] if usuario[3] else 0,
                "longitud": usuario[4] if usuario[4] else 0,
                "ciudad": usuario[5] if usuario[5] else "",
                "region": usuario[6] if usuario[6] else ""
            },
            "foto_perfil": usuario[7],
            "notificaciones": bool(usuario[10]) if len(usuario) > 10 and usuario[10] is not None else True,
            # Ya no devolvemos cultivos aquí
        }
        return usuario_dict

    except Exception as e:
        return {"error": str(e)}

def modificar_usuario(correo: str, datos: Union[UsuarioModificado, UbicacionUsuario]) -> Dict[str, Any]:
    try:
        if not usuario_existe(correo):
            return {"error": "Usuario no existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Convertir modelo a dict excluyendo nulos
        datos_dict = datos.model_dump(exclude_unset=True)
        
        if not datos_dict:
             conexion.close()
             return {"error": "No hay campos válidos para actualizar"}

        campos_update = []
        valores = []

        for campo, valor in datos_dict.items():
            campos_update.append(f"{campo} = ?")
            valores.append(valor)

        campos_update.append("updated_at = ?")
        valores.append(datetime.now().isoformat())
        valores.append(correo)

        query = (
            f"UPDATE usuarios SET {', '.join(campos_update)} "
            "WHERE correo = ?"
        )
        cursor.execute(query, valores)

        conexion.commit()
        conexion.close()

        return {"mensaje": "Usuario actualizado exitosamente"}

    except Exception as e:
        return {"error": str(e)}

def eliminar_usuario(correo: str) -> Dict[str, Any]:
    try:
        if not usuario_existe(correo):
            return {"error": "Usuario no existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM usuarios WHERE correo = ?", (correo,))

        conexion.commit()
        conexion.close()

        return {"mensaje": "Usuario eliminado exitosamente"}

    except Exception as e:
        return {"error": str(e)}

def obtener_todos_usuarios() -> Dict[str, Any]:
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY created_at")
        usuarios_rows = cursor.fetchall()
        usuarios_db = {}
        
        for usuario_row in usuarios_rows:
            correo = usuario_row[0]
            usuario_dict = {
                "nombre": usuario_row[1],
                "ubicacion": {
                    "latitud": usuario_row[3] if usuario_row[3] else 0,
                    "longitud": usuario_row[4] if usuario_row[4] else 0,
                    "ciudad": usuario_row[5] if usuario_row[5] else "",
                    "region": usuario_row[6] if usuario_row[6] else ""
                },
                "foto_perfil": usuario_row[7],
                "notificaciones": bool(usuario_row[10]) if len(usuario_row) > 10 and usuario_row[10] is not None else True
            }
            usuarios_db[correo] = usuario_dict
            
        conexion.close()
        return usuarios_db

    except Exception as e:
        return {"error": str(e)}

def modificar_notificaciones(correo: str, notificaciones: bool) -> Dict[str, Any]:
    if not usuario_existe(correo):
        return {"error": "Usuario no existe"}
    
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET notificaciones = ?, updated_at = ? WHERE correo = ?", 
                       (notificaciones, datetime.now().isoformat(), correo))
        conexion.commit()
        conexion.close()
        return {"mensaje": "Notificaciones actualizadas"}
    except Exception as e:
        return {"error": str(e)}

def filtrar_usuarios_por_notificaciones() -> List[str]:
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT correo
            FROM usuarios
            WHERE notificaciones = 1
            AND EXISTS (
                SELECT 1 
                FROM cultivos 
                WHERE cultivos.usuario_correo = usuarios.correo
            )
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return [fila[0] for fila in resultados]
    except Exception:
        return []
