#!/usr/bin/env python3
"""
Verificador de Migración SQLite
Verifica que los datos se migraron correctamente
"""

import sqlite3
import json
import sys

def verificar_bd(db_path="src/data/usuarios.db"):
    """Verificar contenido de la base de datos"""
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 VERIFICACIÓN DE BASE DE DATOS")
        print("=" * 35)
        
        # Información general
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        print(f"📊 Total usuarios: {total}")
        
        if total == 0:
            print("⚠️ La base de datos está vacía")
            return
        
        # Estadísticas detalladas
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE ciudad IS NOT NULL AND ciudad != ''")
        con_ciudad = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE region IS NOT NULL AND region != ''")
        con_region = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE latitud IS NOT NULL")
        con_coordenadas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE cultivos != '{}'")
        con_cultivos = cursor.fetchone()[0]
        
        print(f"📍 Con ciudad: {con_ciudad}")
        print(f"🗺️ Con región: {con_region}")
        print(f"🧭 Con coordenadas: {con_coordenadas}")
        print(f"🌾 Con cultivos: {con_cultivos}")
        
        # Mostrar algunos usuarios de ejemplo
        print(f"\n👥 USUARIOS DE EJEMPLO:")
        print("-" * 25)
        
        cursor.execute("SELECT * FROM usuarios LIMIT 5")
        usuarios = cursor.fetchall()
        
        for usuario in usuarios:
            correo, nombre, _, lat, lon, ciudad, region, cultivos_str = usuario[:8]
            
            try:
                cultivos = json.loads(cultivos_str) if cultivos_str else {}
                num_cultivos = len(cultivos)
            except:
                num_cultivos = 0
            
            print(f"📧 {correo}")
            print(f"   👤 {nombre}")
            if ciudad or region:
                print(f"   📍 {ciudad or 'Sin ciudad'}, {region or 'Sin región'}")
            if lat is not None and lon is not None:
                print(f"   🧭 Lat: {lat}, Lon: {lon}")
            if num_cultivos > 0:
                print(f"   🌾 {num_cultivos} cultivos: {list(cultivos.keys())}")
            print()
        
        if total > 5:
            print(f"... y {total - 5} usuarios más")
        
        # Verificar integridad de datos
        print(f"\n🔧 VERIFICACIÓN DE INTEGRIDAD:")
        print("-" * 30)
        
        # Usuarios con JSON de cultivos inválido
        cursor.execute("SELECT correo FROM usuarios")
        todos_correos = cursor.fetchall()
        
        json_invalidos = []
        for (correo,) in todos_correos:
            cursor.execute("SELECT cultivos FROM usuarios WHERE correo = ?", (correo,))
            cultivos_str = cursor.fetchone()[0]
            
            try:
                json.loads(cultivos_str) if cultivos_str else {}
            except:
                json_invalidos.append(correo)
        
        if json_invalidos:
            print(f"❌ JSON inválidos: {len(json_invalidos)} usuarios")
            for correo in json_invalidos[:3]:
                print(f"   - {correo}")
            if len(json_invalidos) > 3:
                print(f"   ... y {len(json_invalidos) - 3} más")
        else:
            print("✅ Todos los JSON de cultivos son válidos")
        
        # Usuarios sin nombre o contraseña
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre = '' OR contrasena = ''")
        sin_datos = cursor.fetchone()[0]
        
        if sin_datos > 0:
            print(f"⚠️ Usuarios con datos faltantes: {sin_datos}")
        else:
            print("✅ Todos los usuarios tienen datos básicos")
        
        conn.close()
        
        print(f"\n✨ Verificación completada")
        print(f"📁 Base de datos: {db_path}")
        
    except sqlite3.Error as e:
        print(f"❌ Error de SQLite: {e}")
    except FileNotFoundError:
        print(f"❌ No se encontró la base de datos: {db_path}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def consultar_usuario(correo, db_path="src/data/usuarios.db"):
    """Consultar un usuario específico"""
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"❌ Usuario no encontrado: {correo}")
            return
        
        correo, nombre, contrasena, lat, lon, ciudad, region, cultivos_str, created, updated = usuario
        cultivos = json.loads(cultivos_str) if cultivos_str else {}
        
        print(f"👤 USUARIO: {correo}")
        print("-" * 30)
        print(f"Nombre: {nombre}")
        print(f"Contraseña: {contrasena[:20]}... (hash)")
        print(f"Ciudad: {ciudad or 'No especificada'}")
        print(f"Región: {region or 'No especificada'}")
        print(f"Latitud: {lat if lat is not None else 'No especificada'}")
        print(f"Longitud: {lon if lon is not None else 'No especificada'}")
        print(f"Cultivos: {len(cultivos)} registrados")
        
        if cultivos:
            for cultivo, hectareas in cultivos.items():
                print(f"  🌾 {cultivo}: {hectareas} hectáreas")
        
        print(f"Creado: {created}")
        print(f"Actualizado: {updated}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error consultando usuario: {e}")

def main():
    """Función principal"""
    db_path = "src/data/usuarios.db"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--usuario" and len(sys.argv) > 2:
            # Consultar usuario específico
            consultar_usuario(sys.argv[2], db_path)
        else:
            # Usar ruta personalizada
            db_path = sys.argv[1]
            verificar_bd(db_path)
    else:
        # Verificación general
        verificar_bd(db_path)

if __name__ == "__main__":
    main()