import json
import sqlite3
from services.security import hash_password_simple, verify_password
        
def formatear_usuario_para_frontend(correo):# retorna  el usuario en el formato que espera el frontend, incluyendo 'id' dentro del diccionario.
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        conexion.close()
        if(not usuario):
            return  {"error": "Usuario no encontrado"}
        usuario_dict = {
            "nombre": usuario[1],
            "ubicacion": {
                "latitud": usuario[3] if usuario[3] else 0,
                "longitud": usuario[4] if usuario[4] else 0,
                "ciudad": usuario[5] if usuario[5] else "",
                "region": usuario[6] if usuario[6] else ""
            },
            "cultivos": json.loads(usuario[7]) if usuario[7] else {}
        }
        return {"id": correo, **usuario_dict}
    
    except Exception as e:
        return {"error": str(e)}

#Útil para pruebas en FASTAPI
def service_leer_usuarios(): #leer el json y retornar todos los usuarios en un diccionario
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios")
        filas = cursor.fetchall()
        conexion.close()

        usuarios_db = {}
        for fila in filas:
            correo = fila[0]
            usuario_dict = {
                "nombre": fila[1],
                "ubicacion": {
                    "latitud": fila[3] if fila[3] else 0,
                    "longitud": fila[4] if fila[4] else 0,
                    "ciudad": fila[5] if fila[5] else "",
                    "region": fila[6] if fila[6] else ""
                },
                "cultivos": json.loads(fila[7]) if fila[7] else {}
            }
            usuarios_db[correo] = usuario_dict

        return usuarios_db

    except Exception as e:
        return {"error": str(e)}

def service_registrar_nuevo_usuario(correo, nombre, contrasena): #guardar/registrar un nuevo usuario
    try:
        contrasena_hasheada = hash_password_simple(contrasena)
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT correo FROM usuarios WHERE correo = ?", (correo,))
        if cursor.fetchone():
            return {"error": "Correo ya utilizado"}
        cursor.execute("INSERT INTO usuarios (correo, nombre, contrasena, latitud, longitud, ciudad, region, cultivos) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (correo, nombre, contrasena_hasheada, 0, 0, "", "", json.dumps({})))
        conexion.commit()
        conexion.close()
        return {"mensaje": "Usuario registrado exitosamente"}

    except Exception as e:
        return {"error": str(e)}
    
def service_obtener_usuario_frontend(correo): #retorna toda la informacion de un usuario en concreto
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        conexion.close()
        if usuario is not None:
            return formatear_usuario_para_frontend(correo)
        return {"error": "Usuario no encontrado"}
    except Exception as e:
        return {"error": str(e)}
    
def service_obtener_cultivos_usuario(correo): #se obtienen todos los cultivos de un usuario, puede que posteriormente venga del frontend-----
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT cultivos FROM usuarios WHERE correo = ?", (correo,))
        resultado = cursor.fetchone()
        conexion.close()
        if resultado is not None:
            cultivos_str = resultado[0]
            cultivos = json.loads(cultivos_str) if cultivos_str else {}
            return cultivos
        return {"error": "Usuario no encontrado"}
    except Exception as e:
        return {"error": str(e)}
    
#puede que despues esta funcion desaparezca y quede solo la de service_modificar_usuario()
def service_agregar_o_modificar_cultivo(correo, cultivo, hectareas): #se agrega el cultivo si no está, y si está se modifica -> tal vez ver si es mejor separar las funciones y permitir tener cultivos repetidos (puede que el usuario tenga 2 campos de maiz con distintas hectareas en cada campo)
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT cultivos FROM usuarios WHERE correo = ?", (correo,))
        resultado = cursor.fetchone()
        if resultado is not None:
            cultivos = json.loads(resultado[0]) if resultado[0] else {}
            cultivos[cultivo] = hectareas
            cursor.execute("UPDATE usuarios SET cultivos = ? WHERE correo = ?", (json.dumps(cultivos, ensure_ascii=False), correo))
            conexion.commit()
            conexion.close()
            return {"mensaje": "Cultivo guardado exitosamente"}
        conexion.close()
        return {"error": "Usuario no encontrado"}
    except Exception as e:
        if 'conexion' in locals():
            conexion.close()
        return {"error": str(e)}

def service_eliminar_cultivo(correo, cultivo): #busca un cultivo por el nombre y lo elimina -> tal vez sea util
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT cultivos FROM usuarios WHERE correo = ?", (correo,))
        resultado = cursor.fetchone()
        if resultado is not None:
            cultivos = json.loads(resultado[0]) if resultado[0] else {}
            if cultivo in cultivos:
                cultivos.pop(cultivo)
                cursor.execute("UPDATE usuarios SET cultivos = ? WHERE correo = ?", (json.dumps(cultivos), correo))
                conexion.commit()
                conexion.close()
                return {"mensaje": "Cultivo eliminado exitosamente"}
            else:
                conexion.close()
                return {"error": "Cultivo no encontrado"}
        conexion.close()
        return {"error": "Usuario no encontrado"}
    except Exception as e:
        if 'conexion' in locals():
            conexion.close()
        return {"error": str(e)}

def service_modificar_usuario(correo, usuarioMOD): #modifica el nombre, ciudad o region de un usuario
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        if usuario:
            cursor.execute("UPDATE usuarios SET nombre = ?, ciudad = ?, region = ? WHERE correo = ?",
                           (usuarioMOD.nombre, usuarioMOD.ciudad, usuarioMOD.region, correo))
            conexion.commit()
            conexion.close()
            return {"mensaje": "Usuario modificado exitosamente"}
        conexion.close()
        return {"error": "Usuario no encontrado"}
    except Exception as e:
        if 'conexion' in locals():
            conexion.close()
        return {"error": str(e)}
    
def service_modificar_ubicacion_usuario(correo, lat, lon):
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        if usuario:
            cursor.execute("UPDATE usuarios SET latitud = ?, longitud = ? WHERE correo = ?", (lat, lon, correo))
            conexion.commit()
            conexion.close()
            return {"mensaje": "Usuario modificado correctamente"}
        conexion.close()
        return {"error": "Usuario no encontrado"}
    except Exception as e:
        if 'conexion' in locals():
            conexion.close()
        return {"error": str(e)}
    
def service_iniciar_sesion(correo_entrada, contrasena_entrada):
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo_entrada,))
        usuario = cursor.fetchone()
        conexion.close()
        
        if not usuario:
            return {"error": "Usuario no encontrado"}
        
        if not verify_password(usuario[2], contrasena_entrada):
            return {"error": "Contraseña incorrecta"}
        
        usuario_sanitizado = {
            "id": correo_entrada,
            "nombre": usuario[1],
            "ubicacion": {
                "latitud": usuario[3] if usuario[3] else 0,
                "longitud": usuario[4] if usuario[4] else 0,
                "ciudad": usuario[5] if usuario[5] else "",
                "region": usuario[6] if usuario[6] else ""
            },
            "cultivos": json.loads(usuario[7]) if usuario[7] else {}
        }
        
        return usuario_sanitizado
    
    except Exception as e:
        return {"error": str(e)}

def service_modificar_region_ciudad_usuario(correo, region, ciudad):
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        if not usuario:
            conexion.close()
            return {"error": "Usuario no encontrado"}
        cursor.execute("UPDATE usuarios SET region = ?, ciudad = ? WHERE correo = ?", (region, ciudad, correo))
        conexion.commit()
        conexion.close()
        return {"mensaje": "Ubicación modificada correctamente"}
    except Exception as e:
        return {"error": str(e)}
    
def service_eliminar_usuario(correo):
    try:
        conexion = sqlite3.connect("data/usuarios.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()

        if not usuario:
            conexion.close()
            return {"error": "Usuario no encontrado"}
        cursor.execute("DELETE FROM usuarios WHERE correo = ?", (correo,))
        conexion.commit()
        conexion.close()
        return {"mensaje": "Usuario " + correo + " eliminado"}

    except Exception as e:
        if 'conexion' in locals():
            conexion.close()
        return {"error": str(e)}