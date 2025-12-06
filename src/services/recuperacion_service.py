
import sqlite3
import random
import string
from datetime import datetime, timedelta
from services.notificaciones_service import enviar_archivo
from services.usuarios_service import get_db_connection, service_modificar_usuario, service_existe_usuario, hash_password_simple



def generar_codigo_recuperacion(correo):
    """
    Genera un código, lo guarda en BD y lo envía por correo.
    """
    if not service_existe_usuario(correo):
        return {"error": "Usuario no encontrado"}

    codigo = ''.join(random.choices(string.digits, k=6))
    expiracion = datetime.now() + timedelta(minutes=15)

    try:
        conn = get_db_connection()
        # Upsert: Insertar o actualizar si ya existe
        conn.execute("""
            INSERT OR REPLACE INTO codigos_recuperacion (correo, codigo, expiracion)
            VALUES (?, ?, ?)
        """, (correo, codigo, expiracion))
        conn.commit()
        conn.close()

        # Enviar correo
        resultado_envio = enviar_archivo(correo, None, codigo)
        
        if "error" in resultado_envio:
             return {"error": "Error al enviar el correo. Inténtalo más tarde."}

        return {"mensaje": "Código enviado a tu correo"}

    except Exception as e:
        return {"error": str(e)}

def verificar_codigo(correo, codigo):
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
        
        # Convertir string de fecha a datetime si es necesario (sqlite devuelve string)
        if isinstance(expiracion_str, str):
            try:
                # Intenta formato con microsegundos
                expiracion = datetime.strptime(expiracion_str, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                 # Intento formato sin microsegundos
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

def cambiar_contrasena_recuperacion(correo, codigo, nueva_contrasena):
    """
    Verifica el código nuevamente y cambia la contraseña.
    """
    validacion = verificar_codigo(correo, codigo)
    if not validacion["valid"]:
        return {"error": validacion.get("error", "Código inválido")}

    # Cambiar contraseña
    # Usamos direct update aquí o service_modificar_usuario?
    # service_modificar_usuario usa campos específicos, mejor hacer update directo de pass
    
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
