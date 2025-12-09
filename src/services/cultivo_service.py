import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

from models.cultivo import CultivoCreate, CultivoDatos, AreaCultivoDatos, CultivoResponse
from services.user_service import usuario_existe

import os

# DB_PATH = "data/DataBase.db"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "DataBase.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def agregar_cultivo(correo: str, cultivo: CultivoCreate) -> Dict[str, Any]:
    try:
        if not usuario_existe(correo):
            return {"error": "Usuario no existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""SELECT id FROM cultivos WHERE
        usuario_correo = ? AND nombre_cultivo = ?""", (correo, cultivo.nombre_cultivo))
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
            correo, cultivo.nombre_cultivo, cultivo.hectareas, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None,
            "Aquí están los consejos de la IA", datetime.now().isoformat()
        ))
        conexion.commit()
        conexion.close()
        return {"mensaje": f"Cultivo {cultivo.nombre_cultivo} agregado exitosamente"}

    except Exception as e:
        return {"error": str(e)}

def modificar_formulario_cultivo(correo: str, datos: CultivoDatos) -> Dict[str, Any]:
    try:
        if not usuario_existe(correo):
            return {"error": "Usuario no existe"}

        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""SELECT id FROM cultivos WHERE usuario_correo = ?
        AND nombre_cultivo = ?""", (correo, datos.nombre_cultivo))
        if not cursor.fetchone():
            conexion.close()
            return {"error": "Cultivo no encontrado para este usuario"}

        # Convertir modelo a dict excluyendo nulos
        datos_dict = datos.model_dump(exclude_unset=True)
        # Removemos nombre_cultivo del dict de update porque es parte del WHERE
        if "nombre_cultivo" in datos_dict:
            del datos_dict["nombre_cultivo"]

        if not datos_dict:
            conexion.close()
            return {"error": "No hay campos válidos para actualizar"}

        campos_update = []
        valores = []
        for campo, valor in datos_dict.items():
            campos_update.append(f"{campo} = ?")
            valores.append(valor)

        cursor.execute(f"""
            UPDATE cultivos
            SET {', '.join(campos_update)}
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (*valores, correo, datos.nombre_cultivo))

        conexion.commit()
        conexion.close()
        return {"mensaje": f"Cultivo {datos.nombre_cultivo} modificado exitosamente"}

    except Exception as e:
        return {"error": str(e)}

def modificar_area_cultivo(correo: str, datos: AreaCultivoDatos) -> Dict[str, Any]:
    try:
        if not usuario_existe(correo):
            return {"error": "Usuario no existe"}
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT id FROM cultivos
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (correo, datos.cultivo))
        
        if not cursor.fetchone():
            conexion.close()
            return {"error": "Cultivo no encontrado para este usuario"}

        # Serializar puntos a JSON
        puntos_json = json.dumps([p.model_dump() for p in datos.puntos])

        cursor.execute("""
            UPDATE cultivos
            SET hectareas = ?, puntos = ?
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (datos.area, puntos_json, correo, datos.cultivo))

        conexion.commit()
        conexion.close()
        return {"mensaje": f"Área del cultivo {datos.cultivo} modificada exitosamente"}

    except Exception as e:
        return {"error": str(e)}

def eliminar_cultivo(correo: str, nombre_cultivo: str) -> Dict[str, Any]:
    try:
        if not usuario_existe(correo):
            return {"error": "Usuario no existe"}
            
        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id FROM cultivos
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (correo, nombre_cultivo))

        if not cursor.fetchone():
            conexion.close()
            return {"error": "Cultivo no encontrado"}

        cursor.execute("""
            DELETE FROM cultivos
            WHERE usuario_correo = ? AND nombre_cultivo = ?
        """, (correo, nombre_cultivo))

        conexion.commit()
        conexion.close()

        return {"mensaje": f"Cultivo {nombre_cultivo} eliminado"}

    except Exception as e:
        return {"error": str(e)}

def obtener_todos_cultivos_usuario(correo: str) -> List[Dict[str, Any]] | Dict[str, str]:
    """
    Obtiene TODOS los cultivos de un usuario SIN paginación.
    """
    try:
        if not usuario_existe(correo):
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
            return [] # Retornar lista vacía en lugar de error para consistencia

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

def obtener_detalle_cultivo(correo: str, nombre_cultivo: str) -> Dict[str, Any]:
    try:
        if not usuario_existe(correo):
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

        cultivo_info = {
            "id": cultivo_row[0],
            "usuario_correo": cultivo_row[1],
            "nombre_cultivo": cultivo_row[2],
            "hectareas": cultivo_row[3],
            "fecha_siembra": cultivo_row[4],
            "notas": cultivo_row[5],
            "puntos": json.loads(cultivo_row[6]) if cultivo_row[6] else [],
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
        return {"error": str(e)}

def filtrar_cultivos(
    correo: Optional[str] = None,
    buscar: Optional[str] = None,
    etapa_planta: Optional[str] = None,
    fecha_siembra_desde: Optional[str] = None,
    fecha_siembra_hasta: Optional[str] = None,
    estado_planta: Optional[str] = None,
    tipo_riego: Optional[str] = None,
    ordenar_por: str = "nombre_cultivo",
    orden: str = "ASC",
    pagina: int = 1,
    limite: int = 20
) -> Dict[str, Any]:
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()

        condiciones = []
        parametros = []

        if correo:
            condiciones.append("usuario_correo = ?")
            parametros.append(correo)

        if buscar:
            condiciones.append("nombre_cultivo LIKE ?")
            parametros.append(f"%{buscar}%")

        if etapa_planta:
            condiciones.append("Etapa_planta = ?")
            parametros.append(etapa_planta)

        if estado_planta:
            condiciones.append("Estado_Planta = ?")
            parametros.append(estado_planta)

        if tipo_riego:
            condiciones.append("Tipo_riego = ?")
            parametros.append(tipo_riego)

        if fecha_siembra_desde:
            condiciones.append("fecha_siembra >= ?")
            parametros.append(fecha_siembra_desde)

        if fecha_siembra_hasta:
            condiciones.append("fecha_siembra <= ?")
            parametros.append(fecha_siembra_hasta)

        where_clause = "WHERE " + " AND ".join(condiciones) if condiciones else ""
        
        # Count total
        cursor.execute(f"SELECT COUNT(*) FROM cultivos {where_clause}", parametros)
        total = cursor.fetchone()[0]

        # Pagination
        offset = (pagina - 1) * limite
        
        query = f"""
            SELECT id, nombre_cultivo, hectareas, fecha_siembra, notas,
                puntos, Etapa_planta, Tipo_riego, Ultimo_riego,
                Frecuencia_Riego, Humedad_Suelo, Textura_suelo,
                Variedad_planta, Estado_Planta, Estres_Hidrico,
                Profundidad_radical, Densidad_plantacion, Tipo_Sensor,
                Eficiencia_riego, Caudal, pH_agua, acolchado,
                consejos_ia, created_at
            FROM cultivos
            {where_clause}
            ORDER BY {ordenar_por} {orden}
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, (*parametros, limite, offset))
        
        cultivos_rows = cursor.fetchall()
        conexion.close()

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
