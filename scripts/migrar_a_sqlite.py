#!/usr/bin/env python3
"""
Script de Migración: JSON a SQLite
AtmosphericLettuce - Sistema de Usuarios

Migra datos de usuarios.json a usuarios.db
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

class MigradorSQLite:
    def __init__(self, json_path="src/data/usuarios.json", db_path="src/data/usuarios.db"):
        self.json_path = json_path
        self.db_path = db_path
        self.usuarios_migrados = 0
        self.errores = []
    
    def verificar_archivos(self):
        """Verificar que existe el archivo JSON"""
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"❌ No se encontró: {self.json_path}")
        
        # Crear directorio para la BD si no existe
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        
        print(f"✅ JSON encontrado: {self.json_path}")
        print(f"📁 BD se creará en: {self.db_path}")
    
    def crear_tabla_usuarios(self, cursor):
        """Crear tabla usuarios con estructura completa"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                correo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                contrasena TEXT NOT NULL,
                latitud REAL,
                longitud REAL,
                ciudad TEXT,
                region TEXT,
                cultivos TEXT,  -- JSON como texto
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear índices para consultas rápidas
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_nombre ON usuarios(nombre)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ciudad ON usuarios(ciudad)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_region ON usuarios(region)')
        
        print("✅ Tabla 'usuarios' creada con índices")
    
    def leer_json(self):
        """Leer y validar el archivo JSON"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
            
            print(f"📄 JSON cargado: {len(usuarios)} usuarios encontrados")
            return usuarios
        
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ JSON inválido: {e}")
        except Exception as e:
            raise Exception(f"❌ Error leyendo JSON: {e}")
    
    def migrar_usuario(self, cursor, correo, datos):
        """Migrar un usuario individual"""
        try:
            # Extraer ubicación
            ubicacion = datos.get('ubicacion', {})
            
            # Convertir cultivos a JSON string
            cultivos = datos.get('cultivos', {})
            cultivos_json = json.dumps(cultivos, ensure_ascii=False)
            
            # Validar datos básicos
            nombre = datos.get('nombre', '').strip()
            contrasena = datos.get('contrasena', '').strip()
            
            if not nombre:
                raise ValueError("Nombre vacío")
            if not contrasena:
                raise ValueError("Contraseña vacía")
            if not correo or '@' not in correo:
                raise ValueError("Correo inválido")
            
            # Insertar en BD
            cursor.execute('''
                INSERT OR REPLACE INTO usuarios 
                (correo, nombre, contrasena, latitud, longitud, ciudad, region, cultivos)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                correo,
                nombre,
                contrasena,
                ubicacion.get('latitud'),
                ubicacion.get('longitud'),
                ubicacion.get('ciudad'),
                ubicacion.get('region'),
                cultivos_json
            ))
            
            self.usuarios_migrados += 1
            print(f"  ✅ {correo} ({nombre})")
            
        except Exception as e:
            error_msg = f"Error con {correo}: {str(e)}"
            self.errores.append(error_msg)
            print(f"  ❌ {error_msg}")
    
    def ejecutar_migracion(self):
        """Ejecutar el proceso completo de migración"""
        print("🥬 ATMOSFERIC LETTUCE - Migración a SQLite")
        print("=" * 50)
        
        try:
            # 1. Verificaciones
            print("\n1️⃣ Verificando archivos...")
            self.verificar_archivos()
            
            # 2. Leer JSON
            print("\n2️⃣ Leyendo datos JSON...")
            usuarios_json = self.leer_json()
            
            # 3. Crear BD y tabla
            print("\n3️⃣ Creando base de datos...")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            self.crear_tabla_usuarios(cursor)
            
            # 4. Migrar usuarios
            print("\n4️⃣ Migrando usuarios...")
            for correo, datos in usuarios_json.items():
                self.migrar_usuario(cursor, correo, datos)
            
            # 5. Confirmar cambios
            conn.commit()
            
            # 6. Verificar migración
            print("\n5️⃣ Verificando migración...")
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            total_bd = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE ciudad IS NOT NULL AND ciudad != ''")
            con_ciudad = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE cultivos != '{}'")
            con_cultivos = cursor.fetchone()[0]
            
            conn.close()
            
            # 7. Resumen final
            self.mostrar_resumen(len(usuarios_json), total_bd, con_ciudad, con_cultivos)
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO: {e}")
            return False
    
    def mostrar_resumen(self, total_json, total_bd, con_ciudad, con_cultivos):
        """Mostrar resumen de la migración"""
        print("\n🎉 MIGRACIÓN COMPLETADA")
        print("=" * 30)
        print(f"📄 Usuarios en JSON:     {total_json}")
        print(f"💾 Usuarios en SQLite:   {total_bd}")
        print(f"✅ Migrados exitosos:    {self.usuarios_migrados}")
        print(f"❌ Errores:              {len(self.errores)}")
        print(f"📍 Con ubicación:        {con_ciudad}")
        print(f"🌾 Con cultivos:         {con_cultivos}")
        
        if self.errores:
            print(f"\n⚠️ ERRORES ENCONTRADOS:")
            for i, error in enumerate(self.errores, 1):
                print(f"   {i}. {error}")
        
        print(f"\n📁 Base de datos creada en: {self.db_path}")
        print("🔧 Próximos pasos:")
        print("   1. Verificar datos con un visualizador SQLite")
        print("   2. Actualizar tu aplicación para usar SQLite")
        print("   3. Hacer backup del archivo usuarios.db")

def main():
    """Función principal"""
    # Rutas por defecto
    json_path = "src/data/usuarios.json"
    db_path = "src/data/usuarios.db"
    
    # Permitir argumentos personalizados
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    if len(sys.argv) > 2:
        db_path = sys.argv[2]
    
    # Ejecutar migración
    migrador = MigradorSQLite(json_path, db_path)
    exito = migrador.ejecutar_migracion()
    
    if exito:
        print("\n✨ ¡Migración exitosa!")
        sys.exit(0)
    else:
        print("\n💥 Migración falló")
        sys.exit(1)

if __name__ == "__main__":
    main()