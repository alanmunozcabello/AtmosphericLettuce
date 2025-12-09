import json
import sqlite3
from services.auth_service import hash_password_simple, verify_password
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
        # Obtener TODOS los cultivos sin paginación para el perfil
        cultivos = service_obtener_todos_cultivos_usuario(correo)
        
        # Manejar respuesta
        if isinstance(cultivos, dict) and "error" in cultivos:
            return cultivos
        
        if isinstance(cultivos, dict) and "mensaje" in cultivos:
            cultivos = []
        
        # ✅ DEVOLVER CULTIVOS COMPLETOS (no solo nombre: hectareas)
        # El frontend necesita puntos, formulario, etc.
        usuario_dict = {
            "nombre": usuario[1],
            "ubicacion": {
                "latitud": usuario[3] if usuario[3] else 0,
                "longitud": usuario[4] if usuario[4] else 0,
                "ciudad": usuario[5] if usuario[5] else "",
                "region": usuario[6] if usuario[6] else ""
            },
            "cultivos": cultivos,  # ✅ Array completo de cultivos
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


def service_obtener_todos_cultivos_usuario(correo):
    """
    Obtiene TODOS los cultivos de un usuario SIN paginación.
    Solo para uso interno (ej: obtener_usuario_para_frontend).
    
    Retorna directamente el arreglo de cultivos en formato completo,
    o un dict con error/mensaje si hay problemas.
    """
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
            ORDER BY nombre_cultivo ASC
        """, (correo,))

        cultivos_rows = cursor.fetchall()
        conexion.close()

        if not cultivos_rows:
            return {"mensaje": "Usuario no posee cultivos"}

        cultivos = []
        default_consejos = "Aquí están los consejos de la IA"
        for row in cultivos_rows:
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

        return cultivos

    except Exception as e:
        return {"error": str(e)}


def service_obtener_nombres_cultivos(correo):
    """
    Obtiene solo los nombres de los cultivos para selectores ligeros.
    Retorna lista simple de strings: ["Tomate", "Lechuga", ...]
    """
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT nombre_cultivo
            FROM cultivos
            WHERE usuario_correo = ?
            ORDER BY nombre_cultivo ASC
        """, (correo,))

        rows = cursor.fetchall()
        conexion.close()

        # Retornar lista plana
        return [row[0] for row in rows]

    except Exception as e:
        return {"error": str(e)}


def service_obtener_cultivos_usuario(correo, pagina=1, limite=20):
    try:
        if not service_existe_usuario(correo):
            return {"error": "Usuario no existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()

        # Calcular offset para paginación
        offset = (pagina - 1) * limite

        # Obtener total de cultivos
        cursor.execute("""
            SELECT COUNT(*)
            FROM cultivos
            WHERE usuario_correo = ?
        """, (correo,))
        total = cursor.fetchone()[0]

        # Obtener cultivos paginados
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
            LIMIT ? OFFSET ?
        """, (correo, limite, offset))

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

        # Retornar con metadata de paginación
        return {
            "cultivos": cultivos,
            "paginacion": {
                "pagina_actual": pagina,
                "limite": limite,
                "total": total,
                "total_paginas": (total + limite - 1) // limite,
                "tiene_siguiente": pagina * limite < total,
                "tiene_anterior": pagina > 1
            }
        }

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
        # Actualizar en BD (validaciones en UsuarioModificado)
        datos = {"foto_perfil": imagen_base64}
        resultado = service_modificar_usuario(correo, datos)

        if "error" not in resultado:
            return {"mensaje": "Foto de perfil actualizada correctamente"}
        else:
            return resultado

    except Exception as e:
        return {"error": str(e)}


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

#Obtiene una lista de correos de usuarios con notificaciones activadas 
#--------------------------------------------------
#filtradores
def filtrar_usuarios_por_notificaciones():
    
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

        correos = [fila[0] for fila in resultados]
        return correos

    except Exception as e:
        return {"error": str(e)}


# Filtrar cultivos de un usuario por algún parámetro específico
def service_filtrar_cultivos(
    correo=None,
    buscar=None,
    etapa_planta=None,
    fecha_siembra_desde=None,
    fecha_siembra_hasta=None,
    estado_planta=None,
    tipo_riego=None,
    tiene_area=None,
    tiene_formulario=None,
    ordenar_por="nombre_cultivo",
    orden="ASC",
    pagina=1,
    limite=20
):
    """
    Método universal para filtrar cultivos con cualquier combinación
    de criterios. Retorna los cultivos en el mismo formato que
    service_obtener_cultivos_usuario.

    Todos los parámetros son opcionales.
    """
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()

        # Construir query dinámicamente
        condiciones = []
        parametros = []

        # Filtro por usuario
        if correo:
            condiciones.append("usuario_correo = ?")
            parametros.append(correo)

        # Búsqueda por nombre
        if buscar:
            condiciones.append("nombre_cultivo LIKE ?")
            parametros.append(f"%{buscar}%")

        # Filtros exactos
        if etapa_planta:
            condiciones.append("Etapa_planta = ?")
            parametros.append(etapa_planta)

        if estado_planta:
            condiciones.append("Estado_Planta = ?")
            parametros.append(estado_planta)

        if tipo_riego:
            condiciones.append("Tipo_riego = ?")
            parametros.append(tipo_riego)

        # Rango de fechas
        if fecha_siembra_desde:
            condiciones.append("fecha_siembra >= ?")
            parametros.append(fecha_siembra_desde)

        if fecha_siembra_hasta:
            condiciones.append("fecha_siembra <= ?")
            parametros.append(fecha_siembra_hasta)

        # Filtros booleanos
        if tiene_area is not None:
            if tiene_area:
                condiciones.append("puntos IS NOT NULL AND puntos != '[]'")
            else:
                condiciones.append("(puntos IS NULL OR puntos = '[]')")

        if tiene_formulario is not None:
            if tiene_formulario:
                condiciones.append("fecha_siembra IS NOT NULL")
            else:
                condiciones.append("fecha_siembra IS NULL")

        # Construir WHERE
        where_clause = " AND ".join(condiciones) if condiciones else "1=1"

        # Validar campo de ordenamiento
        campos_validos = [
            "nombre_cultivo", "hectareas", "fecha_siembra",
            "Etapa_planta", "created_at"
        ]
        if ordenar_por not in campos_validos:
            ordenar_por = "nombre_cultivo"

        if orden.upper() not in ["ASC", "DESC"]:
            orden = "ASC"

        # Paginación
        offset = (pagina - 1) * limite

        # Query principal - MISMOS CAMPOS que service_obtener_cultivos_usuario
        query = f"""
            SELECT id, nombre_cultivo, hectareas, fecha_siembra, notas,
                puntos, Etapa_planta, Tipo_riego, Ultimo_riego,
                Frecuencia_Riego, Humedad_Suelo, Textura_suelo,
                Variedad_planta, Estado_Planta, Estres_Hidrico,
                Profundidad_radical, Densidad_plantacion, Tipo_Sensor,
                Eficiencia_riego, Caudal, pH_agua, acolchado,
                consejos_ia, created_at
            FROM cultivos
            WHERE {where_clause}
            ORDER BY {ordenar_por} {orden}
            LIMIT ? OFFSET ?
        """

        cursor.execute(query, (*parametros, limite, offset))
        cultivos_rows = cursor.fetchall()

        # Contar total para paginación
        query_count = f"""
            SELECT COUNT(*)
            FROM cultivos
            WHERE {where_clause}
        """
        cursor.execute(query_count, parametros)
        total = cursor.fetchone()[0]

        conexion.close()

        # Formatear resultados - MISMA ESTRUCTURA que
        # service_obtener_cultivos_usuario
        cultivos = []
        default_consejos = "Aquí están los consejos de la IA"
        for row in cultivos_rows:
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

        # SIEMPRE retornar un objeto con la lista, aunque esté vacía
        return {"cultivos": cultivos}

    except Exception as e:
        return {"error": str(e)}
    

def service_filtrar_usuarios(
    buscar=None,
    region=None,
    ciudad=None,
    notificaciones=None,
    tiene_cultivos=None,
    ordenar_por="created_at",
    orden="DESC",
    pagina=1,
    limite=20
):
    """
    Filtrar usuarios con múltiples criterios
    """
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()

        condiciones = []
        parametros = []

        # Búsqueda por nombre o correo
        if buscar:
            condiciones.append("(nombre LIKE ? OR correo LIKE ?)")
            parametros.extend([f"%{buscar}%", f"%{buscar}%"])

        # Filtro por región
        if region:
            condiciones.append("region = ?")
            parametros.append(region)

        # Filtro por ciudad
        if ciudad:
            condiciones.append("ciudad = ?")
            parametros.append(ciudad)

        # Filtro por notificaciones
        if notificaciones is not None:
            condiciones.append("notificaciones = ?")
            parametros.append(1 if notificaciones else 0)

        # Filtro por tiene cultivos (✅ CORRECTO)
        if tiene_cultivos is not None:
            if tiene_cultivos:
                condiciones.append("""
                    EXISTS (
                        SELECT 1 
                        FROM cultivos 
                        WHERE cultivos.usuario_correo = usuarios.correo
                    )
                """)
            else:
                condiciones.append("""
                    NOT EXISTS (
                        SELECT 1 
                        FROM cultivos 
                        WHERE cultivos.usuario_correo = usuarios.correo
                    )
                """)

        where_clause = " AND ".join(condiciones) if condiciones else "1=1"

        # Validar ordenamiento
        campos_validos = ["correo", "nombre", "created_at", "region", "ciudad"]
        if ordenar_por not in campos_validos:
            ordenar_por = "created_at"

        if orden.upper() not in ["ASC", "DESC"]:
            orden = "DESC"

        # Paginación
        offset = (pagina - 1) * limite

        # Query principal
        query = f"""
            SELECT correo, nombre, latitud, longitud, ciudad, region,
                   foto_perfil, notificaciones, created_at, updated_at
            FROM usuarios
            WHERE {where_clause}
            ORDER BY {ordenar_por} {orden}
            LIMIT ? OFFSET ?
        """

        cursor.execute(query, (*parametros, limite, offset))
        usuarios_rows = cursor.fetchall()

        # Contar total
        query_count = f"""
            SELECT COUNT(*)
            FROM usuarios
            WHERE {where_clause}
        """
        cursor.execute(query_count, parametros)
        total = cursor.fetchone()[0]

        conexion.close()

        # Formatear resultados
        usuarios = []
        for row in usuarios_rows:
            usuarios.append({
                "correo": row[0],
                "nombre": row[1],
                "ubicacion": {
                    "latitud": row[2] if row[2] else 0,
                    "longitud": row[3] if row[3] else 0,
                    "ciudad": row[4] if row[4] else "",
                    "region": row[5] if row[5] else ""
                },
                "foto_perfil": row[6],
                "notificaciones": bool(row[7]),
                "created_at": row[8],
                "updated_at": row[9]
            })

        if not usuarios:
            return {"mensaje": "No se encontraron usuarios con esos filtros"}

        return usuarios

    except Exception as e:
        return {"error": str(e)}
        
    
       