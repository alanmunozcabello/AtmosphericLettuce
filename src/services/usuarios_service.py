import json
import sqlite3
from services.security import hash_password_simple, verify_password
from datetime import datetime

DB_PATH = "data/DataBase.db"


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

        conexion.close()
        cultivos = service_obtener_cultivos_usuario(correo)
        usuario_dict = {
            "nombre": usuario[1],
            "ubicacion": {
                "latitud": usuario[3] if usuario[3] else 0,
                "longitud": usuario[4] if usuario[4] else 0,
                "ciudad": usuario[5] if usuario[5] else "",
                "region": usuario[6] if usuario[6] else ""
            },
            "cultivos": cultivos,
            "foto_perfil": usuario[7],
            "notificaciones": bool(usuario[10]) if len(usuario) > 10
            and usuario[10] is not None else True
        }
        return {"id": correo, **usuario_dict}

    except Exception as e:
        return {"error": str(e)}


# Útil para el FastAPI
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
                "foto_perfil": usuario_row[7],
                "notificaciones": bool(usuario_row[10]) if
                len(usuario_row) > 10 and usuario_row[10] is not None else True
            }
            usuarios_db[correo] = usuario_dict
        conexion.close()
        return usuarios_db

    except Exception as e:
        return {"error": str(e)}


def service_existe_usuario(correo):
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE correo = ?", (correo,))
        existe = cursor.fetchone() is not None
        conexion.close()
        return existe
    except Exception:
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
            (correo, nombre, contrasena, latitud, longitud, ciudad,
            region, foto_perfil, created_at, updated_at, notificaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            correo, nombre,
            contrasena_hash, None, None, None, None, None,
            datetime.now().isoformat(), datetime.now().isoformat(), True
        ))
        conexion.commit()
        conexion.close()
        return {"mensaje": "Usuario registrado exitosamente"}

    except Exception as e:
        return {"error": str(e)}


def service_agregar_cultivo(correo, nombre_cultivo, hectareas):
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""SELECT id FROM cultivos WHERE
        usuario_correo = ? AND nombre_cultivo = ?""", (correo, nombre_cultivo))
        if cursor.fetchone():
            conexion.close()
            return {"error": "Cultivo ya existe para este usuario"}

        cursor.execute("""
        INSERT INTO cultivos (
            usuario_correo, nombre_cultivo,
            hectareas, fecha_siembra, notas, puntos,
            etapa_planta, tipo_riego, ultimo_riego, frecuencia_riego,
            humedad_suelo, textura_suelo, variedad_planta, estado_planta,
            estres_hidrico, profundidad_radical, densidad_plantacion,
            tipo_sensor, eficiencia_riego, caudal, ph_agua, acolchado,
            consejos_ia, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            correo, nombre_cultivo, hectareas, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None,
            "Aquí están los consejos de la IA", datetime.now().isoformat()
        ))
        conexion.commit()
        conexion.close()
        return {"mensaje": f"Cultivo {nombre_cultivo} agregado exitosamente"}

    except Exception as e:
        return {"error": str(e)}


def service_modificar_formulario_cultivo(correo, datos_nuevos):
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""SELECT id FROM cultivos WHERE usuario_correo = ?
        AND nombre_cultivo = ?""", (correo, datos_nuevos["nombre_cultivo"]))
        if not cursor.fetchone():
            conexion.close()
            return {"error": "Cultivo no encontrado para este usuario"}

        campos_permitidos = [
            "fecha_siembra", "notas", "etapa_planta", "tipo_riego",
            "ultimo_riego", "frecuencia_riego", "humedad_suelo",
            "textura_suelo", "variedad_planta", "estado_planta",
            "estres_hidrico", "profundidad_radical", "densidad_plantacion",
            "tipo_sensor", "eficiencia_riego", "caudal", "ph_agua",
            "acolchado", "consejos_ia"
        ]
        campos_update = []
        valores = []
        for campo in campos_permitidos:
            if campo in datos_nuevos:
                campos_update.append(f"{campo} = ?")
                valores.append(datos_nuevos[campo])
        if not campos_update:
            conexion.close()
            return {"error": "No hay campos válidos para actualizar"}

        cursor.execute(f"""
            UPDATE cultivos
            SET {', '.join(campos_update)}
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (*valores, correo, datos_nuevos["nombre_cultivo"]))

        conexion.commit()
        conexion.close()
        nombre = datos_nuevos['nombre_cultivo']
        return {"mensaje": f"Cultivo {nombre} modificado exitosamente"}

    except Exception as e:
        return {"error": str(e)}


def service_modificar_area_cultivo(correo, area_cultivo_datos):
    try:
        # Verificar que usuario existe
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}
        conexion = get_db_connection()
        cursor = conexion.cursor()
        # Verificar si cultivo existe para este usuario
        cursor.execute("""
            SELECT id FROM cultivos
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (correo, area_cultivo_datos["cultivo"]))
        if not cursor.fetchone():
            conexion.close()
            return {"error": "Cultivo no encontrado para este usuario"}

        puntos_json = json.dumps(area_cultivo_datos["puntos"])

        cursor.execute("""
            UPDATE cultivos
            SET hectareas = ?, puntos = ?
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (area_cultivo_datos["area"], puntos_json, correo,
              area_cultivo_datos["cultivo"]))

        conexion.commit()
        conexion.close()
        cultivo = area_cultivo_datos['cultivo']
        return {"mensaje":
                f"Área del cultivo {cultivo} modificada exitosamente"}

    except Exception as e:
        return {"error": str(e)}


def service_eliminar_cultivo(correo, nombre_cultivo):
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}
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
        campos_permitidos = [
            "nombre", "latitud", "longitud", "ciudad",
            "region", "foto_perfil", "notificaciones"
        ]
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
            SELECT id, nombre_cultivo, hectareas, fecha_siembra, notas,
                puntos, Etapa_planta, Tipo_riego, Ultimo_riego,
                Frecuencia_Riego, Humedad_Suelo, Textura_suelo,
                Variedad_planta, Estado_Planta, Estres_Hidrico,
                Profundidad_radical, Densidad_plantacion, Tipo_Sensor,
                Eficiencia_riego, Caudal, pH_agua, acolchado,
                consejos_ia, created_at
            FROM cultivos
            WHERE usuario_correo = ?
            ORDER BY nombre_cultivo
        """, (correo,))

        cultivos_rows = cursor.fetchall()
        conexion.close()

        cultivos = []
        for row in cultivos_rows:
            default_consejos = "Aquí están los consejos de la IA"
            cultivos.append({
                "id": row[0],
                "nombre": row[1],
                "hectareas": row[2],
                "formulario": {
                    "fecha_siembra": row[3],
                    "notas": row[4],
                    "etapa_planta": row[6],
                    "tipo_riego": row[7],
                    "ultimo_riego": row[8],
                    "frecuencia_riego": row[9],
                    "humedad_suelo": row[10],
                    "textura_suelo": row[11],
                    "variedad_planta": row[12],
                    "estado_planta": row[13],
                    "estres_hidrico": row[14],
                    "profundidad_radical": row[15],
                    "densidad_plantacion": row[16],
                    "tipo_sensor": row[17],
                    "eficiencia_riego": row[18],
                    "caudal": row[19],
                    "ph_agua": row[20],
                    "acolchado": row[21],
                    "consejos_ia": row[22] if row[22] else default_consejos,
                    "created_at": row[23]
                },
                "puntos": json.loads(row[5]) if row[5] else [],
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
        query = "SELECT contrasena FROM usuarios WHERE correo = ?"
        cursor.execute(query, (correo,))
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
            error_msg = "Formato de imagen inválido. Debe ser data:image/..."
            return {"error": error_msg}

        # Validar tamaño (máximo ~300KB en Base64 = ~225KB imagen)
        if len(imagen_base64) > 400000:  # ~300KB en Base64
            return {"error": "Imagen muy grande. Máximo 225KB"}

        # Actualizar en BD
        datos = {"foto_perfil": imagen_base64}
        resultado = service_modificar_usuario(correo, datos)

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
            error = f"Tipo {mime_type} no soportado"
            return {"valida": False, "error": error}

        # Decodificar Base64 para verificar validez
        try:
            image_data = base64.b64decode(data, validate=True)
        except Exception:
            return {"valida": False, "error": "Datos Base64 inválidos"}

        # Verificar que tenga contenido
        if len(image_data) < 100:  # Muy pequeño para ser imagen
            error = "Imagen muy pequeña o corrupta"
            return {"valida": False, "error": error}

        # Verificar tamaños
        size_kb = len(image_data) / 1024
        base64_size_kb = len(imagen_base64) / 1024

        # Límite de 300KB para imagen original
        if size_kb > 300:
            error = (
                f"Imagen muy grande: {size_kb:.1f}KB (máx: 300KB)"
            )
            return {"valida": False, "error": error}

        return {
            "valida": True,
            "tipo": mime_type,
            "tamaño_kb": round(size_kb, 2),
            "tamaño_base64_kb": round(base64_size_kb, 2)
        }

    except Exception as e:
        return {"valida": False, "error": str(e)}


def service_modificar_notificaciones_usuario(correo, notificaciones):
    """Activa o desactiva las notificaciones por correo de un usuario"""
    if not service_existe_usuario(correo):
        return {"error": "Usuario no existe"}

    datos = {"notificaciones": notificaciones}
    return service_modificar_usuario(correo, datos)


def service_obtener_info_cultivo(correo, nombre_cultivo):
    """Obtiene toda la información completa de un cultivo específico"""
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM cultivos
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (correo, nombre_cultivo))

        cultivo_row = cursor.fetchone()
        conexion.close()

        if not cultivo_row:
            return {"error": "Cultivo no encontrado"}

        # Crear diccionario con toda la información del cultivo
        cultivo_info = {
            "id": cultivo_row[0],
            "usuario_correo": cultivo_row[1],
            "nombre_cultivo": cultivo_row[2],
            "hectareas": cultivo_row[3],
            "fecha_siembra": cultivo_row[4],
            "notas": cultivo_row[5],
            "puntos": cultivo_row[6],
            "etapa_planta": cultivo_row[7],
            "tipo_riego": cultivo_row[8],
            "ultimo_riego": cultivo_row[9],
            "frecuencia_riego": cultivo_row[10],
            "humedad_suelo": cultivo_row[11],
            "textura_suelo": cultivo_row[12],
            "variedad_planta": cultivo_row[13],
            "estado_planta": cultivo_row[14],
            "estres_hidrico": cultivo_row[15],
            "profundidad_radical": cultivo_row[16],
            "densidad_plantacion": cultivo_row[17],
            "tipo_sensor": cultivo_row[18],
            "consejos_ia": cultivo_row[19] if len(cultivo_row) > 19 else None
        }

        return cultivo_info

    except Exception as e:
        error_msg = f"Error al obtener información del cultivo: {str(e)}"
        return {"error": error_msg}


def guardar_clima_semanal(
        correo, cultivo_nombre, latitud, longitud, clima_dict):
    """
    Guarda o actualiza el clima semanal de un cultivo en la base de datos
    """
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()

        clima_json = json.dumps(clima_dict)

        cursor.execute("""
            INSERT OR REPLACE INTO clima_guardado
            (correo, cultivo_nombre, latitud, longitud,
             clima_json, fecha_guardado)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (correo, cultivo_nombre, latitud, longitud, clima_json))

        conexion.commit()
        conexion.close()

        return {"mensaje": f"Clima guardado para {cultivo_nombre}"}

    except Exception as e:
        return {"error": str(e)}


def obtener_clima_guardado(correo, cultivo_nombre):
    """Obtiene el clima guardado de un cultivo específico"""
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT clima_json, fecha_guardado, latitud, longitud
            FROM clima_guardado
            WHERE correo = ? AND cultivo_nombre = ?
        """, (correo, cultivo_nombre))

        resultado = cursor.fetchone()
        conexion.close()

        if not resultado:
            return {"error": "No hay clima guardado para este cultivo"}

        clima_dict = json.loads(resultado[0])

        return {
            "clima": clima_dict,
            "fecha_guardado": resultado[1],
            "latitud": resultado[2],
            "longitud": resultado[3]
        }

    except Exception as e:
        return {"error": str(e)}
