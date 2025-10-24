#!/usr/bin/env python3
"""
Script de Migración: Nueva Estructura con Tablas Relacionadas
AtmosphericLettuce - Usuarios y Cultivos separados

Migra de estructura antigua a:
- Tabla usuarios (sin cultivos, con foto_perfil)
- Tabla cultivos (relacionada por foreign key)
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

class Migrador:
    def __init__(self, db_antigua="src/data/usuarios.db", db_nueva="src/data/usuarios_nueva.db"):
        self.db_antigua = db_antigua
        self.db_nueva = db_nueva
        self.usuarios_migrados = 0
        self.cultivos_migrados = 0
        self.errores = []
    
    def verificar_archivos(self):
        """Verificar que existe la BD antigua"""
        if not os.path.exists(self.db_antigua):
            raise FileNotFoundError(f"❌ No se encontró BD antigua: {self.db_antigua}")
        
        # Crear directorio para la nueva BD si no existe
        db_dir = os.path.dirname(self.db_nueva)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        
        print(f"✅ BD antigua encontrada: {self.db_antigua}")
        print(f"📁 BD nueva se creará en: {self.db_nueva}")
    
    def crear_nueva_estructura(self, cursor):
        """Crear las nuevas tablas con estructura mejorada"""
        
        # Tabla usuarios (sin cultivos, con foto_perfil)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                correo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                contrasena TEXT NOT NULL,
                latitud REAL,
                longitud REAL,
                ciudad TEXT,
                region TEXT,
                foto_perfil TEXT DEFAULT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla cultivos (relacionada)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cultivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_correo TEXT NOT NULL,
                nombre_cultivo TEXT NOT NULL,
                hectareas REAL NOT NULL,
                fecha_siembra DATE,
                notas TEXT,
                
                
                etapa_planta TEXT,
                tipo_riego TEXT,
                ultimo_riego DATETIME,
                frecuencia_riego TEXT,
                humedad_suelo TEXT,
                textura_suelo TEXT,
                variedad_planta TEXT,
                estado_planta TEXT,
                estres_hidrico INTEGER DEFAULT 0,
                profundidad_radical INTEGER,
                densidad_plantacion INTEGER,
                tipo_sensor TEXT,
                eficiencia_riego REAL,
                caudal REAL,
                pH_agua REAL,
                acolchado INTEGER DEFAULT 0,
                
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (usuario_correo) REFERENCES usuarios(correo) 
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
            )
        ''')
        
        # Índices para rendimiento
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_nombre ON usuarios(nombre)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_ciudad ON usuarios(ciudad)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_region ON usuarios(region)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cultivos_usuario ON cultivos(usuario_correo)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cultivos_nombre ON cultivos(nombre_cultivo)')
        
        print("✅ Nueva estructura creada: usuarios + cultivos + índices")
    
    def migrar_usuarios(self, conn_antigua, conn_nueva):
        """Migrar usuarios desde BD antigua (sin cultivos)"""
        cursor_antigua = conn_antigua.cursor()
        cursor_nueva = conn_nueva.cursor()
        
        # Leer usuarios de BD antigua
        cursor_antigua.execute("SELECT * FROM usuarios")
        usuarios_antiguos = cursor_antigua.fetchall()
        
        print(f"\n📄 Usuarios encontrados en BD antigua: {len(usuarios_antiguos)}")
        
        for usuario in usuarios_antiguos:
            try:
                # usuario = (correo, nombre, contrasena, lat, lon, ciudad, region, cultivos_json, created, updated)
                correo = usuario[0]
                nombre = usuario[1]
                contrasena = usuario[2]
                latitud = usuario[3]
                longitud = usuario[4]
                ciudad = usuario[5]
                region = usuario[6]
                # cultivos se migran por separado
                created_at = usuario[8] if len(usuario) > 8 else datetime.now().isoformat()
                updated_at = usuario[9] if len(usuario) > 9 else datetime.now().isoformat()
                
                # Insertar usuario en nueva tabla (sin cultivos)
                cursor_nueva.execute('''
                    INSERT OR REPLACE INTO usuarios 
                    (correo, nombre, contrasena, latitud, longitud, ciudad, region, foto_perfil, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    correo, nombre, contrasena, latitud, longitud, 
                    ciudad, region, None, created_at, updated_at
                ))
                
                self.usuarios_migrados += 1
                print(f"  ✅ Usuario: {correo} ({nombre})")
                
            except Exception as e:
                error_msg = f"Error migrando usuario {correo}: {str(e)}"
                self.errores.append(error_msg)
                print(f"  ❌ {error_msg}")
        
        conn_nueva.commit()
    
    # modificar funcion para migrar cultivos
    def migrar_cultivos(self, conn_antigua, conn_nueva):
        """Migrar cultivos desde JSON a tabla separada"""
        cursor_antigua = conn_antigua.cursor()
        cursor_nueva = conn_nueva.cursor()
        
        # Leer cultivos desde BD antigua
        cursor_antigua.execute("SELECT correo, cultivos FROM usuarios")
        usuarios_con_cultivos = cursor_antigua.fetchall()
        
        print(f"\n🌾 Procesando cultivos de {len(usuarios_con_cultivos)} usuarios...")
        
        for correo, cultivos_json in usuarios_con_cultivos:
            try:
                if not cultivos_json or cultivos_json == '{}':
                    continue
                
                cultivos = json.loads(cultivos_json)
                
                for nombre_cultivo, hectareas in cultivos.items():
                    try:
                        cursor_nueva.execute('''
                            INSERT INTO cultivos 
                            (usuario_correo, nombre_cultivo, hectareas, created_at)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            correo,
                            nombre_cultivo,
                            float(hectareas) if hectareas else 0.0,
                            datetime.now().isoformat()
                        ))
                        
                        self.cultivos_migrados += 1
                        print(f"  ✅ Cultivo: {correo} → {nombre_cultivo} ({hectareas} ha)")
                        
                    except Exception as e:
                        error_msg = f"Error con cultivo {nombre_cultivo} de {correo}: {str(e)}"
                        self.errores.append(error_msg)
                        print(f"  ❌ {error_msg}")
                
            except json.JSONDecodeError as e:
                error_msg = f"JSON inválido en cultivos de {correo}: {str(e)}"
                self.errores.append(error_msg)
                print(f"  ❌ {error_msg}")
        
        conn_nueva.commit()
    
    def verificar_migracion(self, conn_nueva):
        """Verificar que la migración fue exitosa"""
        cursor = conn_nueva.cursor()
        
        # Contar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        # Contar cultivos
        cursor.execute("SELECT COUNT(*) FROM cultivos")
        total_cultivos = cursor.fetchone()[0]
        
        # Usuarios con cultivos
        cursor.execute("""
            SELECT COUNT(DISTINCT usuario_correo) 
            FROM cultivos
        """)
        usuarios_con_cultivos = cursor.fetchone()[0]
        
        print(f"\n📊 VERIFICACIÓN:")
        print(f"   👥 Usuarios migrados: {total_usuarios}")
        print(f"   🌾 Cultivos migrados: {total_cultivos}")
        print(f"   🔗 Usuarios con cultivos: {usuarios_con_cultivos}")
        
        return total_usuarios, total_cultivos, usuarios_con_cultivos
    
    def ejecutar_migracion(self):
        """Ejecutar el proceso completo de migración"""
        print("🥬 ATMOSFERIC LETTUCE - Migración Nueva Estructura")
        print("=" * 55)
        
        try:
            # 1. Verificaciones
            print("\n1️⃣ Verificando archivos...")
            self.verificar_archivos()
            
            # 2. Abrir conexiones
            print("\n2️⃣ Conectando a bases de datos...")
            conn_antigua = sqlite3.connect(self.db_antigua)
            conn_nueva = sqlite3.connect(self.db_nueva)
            
            # 3. Crear nueva estructura
            print("\n3️⃣ Creando nueva estructura...")
            cursor_nueva = conn_nueva.cursor()
            self.crear_nueva_estructura(cursor_nueva)
            
            # 4. Migrar usuarios
            print("\n4️⃣ Migrando usuarios...")
            self.migrar_usuarios(conn_antigua, conn_nueva)
            
            # 5. Migrar cultivos
            print("\n5️⃣ Migrando cultivos...")
            self.migrar_cultivos(conn_antigua, conn_nueva)
            
            # 6. Verificar migración
            print("\n6️⃣ Verificando migración...")
            total_usuarios, total_cultivos, usuarios_con_cultivos = self.verificar_migracion(conn_nueva)
            
            # Cerrar conexiones
            conn_antigua.close()
            conn_nueva.close()
            
            # 7. Resumen final
            self.mostrar_resumen(total_usuarios, total_cultivos)
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO: {e}")
            return False
    
    def mostrar_resumen(self, total_usuarios, total_cultivos):
        """Mostrar resumen de la migración"""
        print("\n🎉 MIGRACIÓN NUEVA ESTRUCTURA COMPLETADA")
        print("=" * 40)
        print(f"👥 Usuarios migrados:     {self.usuarios_migrados}")
        print(f"🌾 Cultivos migrados:     {self.cultivos_migrados}")
        print(f"❌ Errores:               {len(self.errores)}")
        print(f"📊 Total en nueva BD:")
        print(f"   - Usuarios: {total_usuarios}")
        print(f"   - Cultivos: {total_cultivos}")
        
        if self.errores:
            print(f"\n⚠️ ERRORES ENCONTRADOS:")
            for i, error in enumerate(self.errores[:5], 1):  # Solo primeros 5
                print(f"   {i}. {error}")
            if len(self.errores) > 5:
                print(f"   ... y {len(self.errores) - 5} errores más")
        
        print(f"\n📁 Nueva base de datos: {self.db_nueva}")
        print("🔧 Próximos pasos:")
        print("   1. Verificar nueva estructura con herramientas SQLite")
        print("   2. Actualizar código de la aplicación")
        print("   3. Probar funcionalidades")
        print("   4. Reemplazar BD antigua con nueva")

def main():
    """Función principal"""
    # Rutas por defecto
    db_antigua = "src/data/usuarios.db"
    db_nueva = "src/data/usuarios_nueva.db"
    
    # Permitir argumentos personalizados
    if len(sys.argv) > 1:
        db_antigua = sys.argv[1]
    if len(sys.argv) > 2:
        db_nueva = sys.argv[2]
    
    # Ejecutar migración
    migrador = Migrador(db_antigua, db_nueva)
    exito = migrador.ejecutar_migracion()
    
    if exito:
        print("\n✨ ¡Migración exitosa!")
        sys.exit(0)
    else:
        print("\n💥 Migración falló")
        sys.exit(1)

if __name__ == "__main__":
    main()