import json
import sqlite3
from services.security import hash_password_simple, verify_password
from datetime import datetime

DB_PATH = "data/usuarios.db" 

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def service_obtener_usuario_para_frontend(correo):
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        if not usuario:
            conexion.close()
            return {"error": "Usuario no encontrado"}
        cursor.execute("""
            SELECT nombre_cultivo, hectareas 
            FROM cultivos 
            WHERE usuario_correo = ?
            ORDER BY nombre_cultivo
        """, (correo,))
        cultivos_rows = cursor.fetchall()
        conexion.close()
        cultivos = {}
        for nombre_cultivo, hectareas in cultivos_rows:
            cultivos[nombre_cultivo] = hectareas
        usuario_dict = {
            "nombre": usuario[1],
            "ubicacion": {
                "latitud": usuario[3] if usuario[3] else 0,
                "longitud": usuario[4] if usuario[4] else 0,
                "ciudad": usuario[5] if usuario[5] else "",
                "region": usuario[6] if usuario[6] else ""
            },
            "cultivos": cultivos,
            "foto_perfil": usuario[7] 
        }
        
        return {"id": correo, **usuario_dict}
    
    except Exception as e:
        return {"error": str(e)}

def service_leer_usuarios():
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY created_at")
        usuarios_rows = cursor.fetchall()
        usuarios_db = {}
        for usuario_row in usuarios_rows:
            correo = usuario_row[0]
            cursor.execute("""
                SELECT nombre_cultivo, hectareas 
                FROM cultivos 
                WHERE usuario_correo = ?
                ORDER BY nombre_cultivo
            """, (correo,))
            cultivos_rows = cursor.fetchall()
            cultivos = {}
            for nombre_cultivo, hectareas in cultivos_rows:
                cultivos[nombre_cultivo] = hectareas
            usuario_dict = {
                "nombre": usuario_row[1],
                "ubicacion": {
                    "latitud": usuario_row[3] if usuario_row[3] else 0,
                    "longitud": usuario_row[4] if usuario_row[4] else 0,
                    "ciudad": usuario_row[5] if usuario_row[5] else "",
                    "region": usuario_row[6] if usuario_row[6] else ""
                },
                "cultivos": cultivos,
                "foto_perfil": usuario_row[7]
            }
            usuarios_db[correo] = usuario_dict
        conexion.close()
        return usuarios_db
        
    except Exception as e:
        return {"error": str(e)}

def service_existe_usuario(correo):
    """Verificar si un usuario existe en la BD"""
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE correo = ?", (correo,))
        existe = cursor.fetchone() is not None
        conexion.close()
        return existe
    except Exception as e:
        return False

def service_registrar_usuario(correo, nombre, contrasena):
    try:
        if not correo or not nombre or not contrasena:
            return {"error": "Faltan datos requeridos"}
        if service_existe_usuario(correo):
            return {"error": "Usuario ya existe"}
        conexion = get_db_connection()
        cursor = conexion.cursor()

        contrasena_hash = hash_password_simple(contrasena)

        cursor.execute("""
            INSERT INTO usuarios 
            (correo, nombre, contrasena, latitud, longitud, ciudad, region, foto_perfil, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            correo,
            nombre,
            contrasena_hash,
            None,
            None,
            None,
            None,
            None,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))

        conexion.commit()
        conexion.close()
        
        return {"mensaje": "Usuario registrado exitosamente"}

    except Exception as e:
        return {"error": str(e)}

def service_agregar_o_modificar_cultivo(correo, nombre_cultivo, hectareas):
    try:
        #Verificar que usuario existe
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        #Verificar si cultivo ya existe para este usuario
        cursor.execute("""
            SELECT id FROM cultivos 
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (correo, nombre_cultivo))
        
        cultivo_existente = cursor.fetchone()
        
        if cultivo_existente:
            #Actualizar cultivo existente
            cursor.execute("""
                UPDATE cultivos 
                SET hectareas = ? 
                WHERE usuario_correo = ? AND nombre_cultivo = ?
            """, (hectareas, correo, nombre_cultivo))
            mensaje = f"Cultivo {nombre_cultivo} actualizado"
        else:
            cursor.execute("""
                INSERT INTO cultivos (usuario_correo, nombre_cultivo, hectareas, created_at)
                VALUES (?, ?, ?, ?)
            """, (correo, nombre_cultivo, hectareas, datetime.now().isoformat()))
            mensaje = f"Cultivo {nombre_cultivo} agregado"
        
        conexion.commit()
        conexion.close()
        
        return {"mensaje": mensaje}
        
    except Exception as e:
        return {"error": str(e)}

def service_eliminar_cultivo(correo, nombre_cultivo):
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        # Verificar si cultivo existe
        cursor.execute("""
            SELECT id FROM cultivos 
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (correo, nombre_cultivo))
        
        if not cursor.fetchone():
            conexion.close()
            return {"error": "Cultivo no encontrado"}
        
        # Eliminar cultivo
        cursor.execute("""
            DELETE FROM cultivos 
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (correo, nombre_cultivo))
        
        conexion.commit()
        conexion.close()
        
        return {"mensaje": f"Cultivo {nombre_cultivo} eliminado"}
        
    except Exception as e:
        return {"error": str(e)}

def service_modificar_usuario(correo, datos_nuevos):
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        campos_permitidos = ["nombre", "latitud", "longitud", "ciudad", "region", "foto_perfil"]
        campos_update = []
        valores = []
        
        for campo in campos_permitidos:
            if campo in datos_nuevos:
                campos_update.append(f"{campo} = ?")
                valores.append(datos_nuevos[campo])
        
        if not campos_update:
            conexion.close()
            return {"error": "No hay campos válidos para actualizar"}
        
        campos_update.append("updated_at = ?")
        valores.append(datetime.now().isoformat())
        valores.append(correo) 
        
        query = f"UPDATE usuarios SET {', '.join(campos_update)} WHERE correo = ?"
        cursor.execute(query, valores)
        
        conexion.commit()
        conexion.close()
        
        return {"mensaje": "Usuario actualizado exitosamente"}
        
    except Exception as e:
        return {"error": str(e)}

def service_modificar_ubicacion_usuario(correo, latitud, longitud):
    datos_ubicacion = {
        "latitud": latitud,
        "longitud": longitud
    }   
    return service_modificar_usuario(correo, datos_ubicacion)

def service_eliminar_usuario(correo):
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM usuarios WHERE correo = ?", (correo,))
        
        conexion.commit()
        conexion.close()
        
        return {"mensaje": "Usuario eliminado exitosamente"}
        
    except Exception as e:
        return {"error": str(e)}


def service_obtener_cultivos_usuario(correo):
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT id, nombre_cultivo, hectareas, fecha_siembra, notas, created_at
            FROM cultivos 
            WHERE usuario_correo = ?
            ORDER BY nombre_cultivo
        """, (correo,))
        
        cultivos_rows = cursor.fetchall()
        conexion.close()
        
        cultivos = []
        for row in cultivos_rows:
            cultivos.append({
                "id": row[0],
                "nombre": row[1],
                "hectareas": row[2],
                "fecha_siembra": row[3],
                "notas": row[4],
                "created_at": row[5]
            })
        
        if not cultivos:
            return {"mensaje": "Usuario no posee cultivos"}

        return cultivos
        
    except Exception as e:
        return {"error": str(e)}

def service_iniciar_sesion(correo, contrasena):
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT contrasena FROM usuarios WHERE correo = ?", (correo,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if not resultado:
            return {"error": "Credenciales incorrectas"}
        
        contrasena_hash = resultado[0]
        if not verify_password(contrasena_hash, contrasena):
            return {"error": "Credenciales incorrectas"}
        
        return service_obtener_usuario_para_frontend(correo)

    except Exception as e:
        return {"error": str(e)}

def service_modificar_region_ciudad_usuario(correo, region, ciudad):
    return service_modificar_usuario(correo, {
        "region": region,   
        "ciudad": ciudad
    })

def service_actualizar_foto_perfil_base64(correo, imagen_base64):
    """Actualizar foto de perfil usando datos Base64"""
    try:
        # Validar formato Base64
        if not imagen_base64.startswith('data:image/'):
            return {"error": "Formato de imagen inválido. Debe ser data:image/..."}
        
        # Validar tamaño (máximo ~300KB en Base64 = ~225KB imagen)
        if len(imagen_base64) > 400000:  # ~300KB en Base64
            return {"error": "Imagen muy grande. Máximo 225KB"}
        
        # Actualizar en BD
        resultado = service_modificar_usuario(correo, {"foto_perfil": imagen_base64})
        
        if "error" not in resultado:
            return {"mensaje": "Foto de perfil actualizada correctamente"}
        else:
            return resultado
            
    except Exception as e:
        return {"error": str(e)}

def service_validar_imagen_base64(imagen_base64):
    """Validar que la cadena Base64 sea una imagen válida"""
    try:
        import base64
        
        # Verificar formato data:image/...
        if not imagen_base64.startswith('data:image/'):
            return {"valida": False, "error": "No es formato data:image/"}
        
        # Extraer datos Base64 y tipo MIME
        header, data = imagen_base64.split(',', 1)
        mime_type = header.split(':')[1].split(';')[0]
        
        # Verificar tipos MIME soportados
        tipos_soportados = [
            'image/jpeg', 'image/jpg', 'image/png', 
            'image/gif', 'image/webp'
        ]
        
        if mime_type not in tipos_soportados:
            return {"valida": False, "error": f"Tipo {mime_type} no soportado"}
        
        # Decodificar Base64 para verificar validez
        try:
            image_data = base64.b64decode(data, validate=True)
        except:
            return {"valida": False, "error": "Datos Base64 inválidos"}
        
        # Verificar que tenga contenido
        if len(image_data) < 100:  # Muy pequeño para ser imagen
            return {"valida": False, "error": "Imagen muy pequeña o corrupta"}
        
        # Verificar tamaños
        size_kb = len(image_data) / 1024
        base64_size_kb = len(imagen_base64) / 1024
        
        # Límite de 300KB para imagen original
        if size_kb > 300:
            return {"valida": False, "error": f"Imagen muy grande: {size_kb:.1f}KB (máx: 300KB)"}
        
        return {
            "valida": True, 
            "tipo": mime_type,
            "tamaño_kb": round(size_kb, 2),
            "tamaño_base64_kb": round(base64_size_kb, 2)
        }
        
    except Exception as e:
        return {"valida": False, "error": str(e)}