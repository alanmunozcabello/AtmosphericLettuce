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
        
        # Tabla cultivos (relacionada con nuevos atributos)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cultivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_correo TEXT NOT NULL,
                nombre_cultivo TEXT NOT NULL,
                hectareas REAL NOT NULL,
                fecha_siembra DATE,
                notas TEXT,
                
                -- Nuevos atributos para manejo avanzado de cultivos
                etapa_planta TEXT,
                tipo_riego TEXT,
                ultimo_riego DATETIME,
                frecuencia_riego TEXT,
                humedad_suelo TEXT,
                textura_suelo TEXT,
                variedad_planta TEXT,
                estado_planta TEXT,
                estres_hidrico TEXT,
                profundidad_radical INTEGER,
                densidad_plantacion INTEGER,
                tipo_sensor TEXT,
                eficiencia_riego INTEGER,
                caudal INTEGER,
                ph_agua INTEGER,
                acolchado TEXT,
                
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
        """Migrar usuarios desde BD antigua"""
        cursor_antigua = conn_antigua.cursor()
        cursor_nueva = conn_nueva.cursor()
        
        # Obtener información de columnas de la tabla usuarios antigua
        cursor_antigua.execute("PRAGMA table_info(usuarios)")
        columnas_antiguas = cursor_antigua.fetchall()
        columnas_dict = {col[1]: col[0] for col in columnas_antiguas}  # {nombre: índice}
        
        print(f"📋 Columnas en tabla usuarios antigua: {', '.join(columnas_dict.keys())}")
        
        # Leer usuarios de BD antigua
        cursor_antigua.execute("SELECT * FROM usuarios")
        usuarios_antiguos = cursor_antigua.fetchall()
        
        print(f"\n📄 Usuarios encontrados en BD antigua: {len(usuarios_antiguos)}")
        
        for usuario in usuarios_antiguos:
            try:
                # Extraer datos usando índices seguros
                correo = usuario[columnas_dict.get('correo', 0)]
                nombre = usuario[columnas_dict.get('nombre', 1)]
                contrasena = usuario[columnas_dict.get('contrasena', 2)]
                latitud = usuario[columnas_dict.get('latitud', 3)] if 'latitud' in columnas_dict else None
                longitud = usuario[columnas_dict.get('longitud', 4)] if 'longitud' in columnas_dict else None
                ciudad = usuario[columnas_dict.get('ciudad', 5)] if 'ciudad' in columnas_dict else None
                region = usuario[columnas_dict.get('region', 6)] if 'region' in columnas_dict else None
                
                # foto_perfil de BD antigua si existe
                foto_perfil = usuario[columnas_dict['foto_perfil']] if 'foto_perfil' in columnas_dict else None
                
                # Timestamps
                created_at = usuario[columnas_dict['created_at']] if 'created_at' in columnas_dict else datetime.now().isoformat()
                updated_at = usuario[columnas_dict['updated_at']] if 'updated_at' in columnas_dict else datetime.now().isoformat()
                
                # Insertar usuario en nueva tabla
                cursor_nueva.execute('''
                    INSERT OR REPLACE INTO usuarios 
                    (correo, nombre, contrasena, latitud, longitud, ciudad, region, foto_perfil, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    correo, nombre, contrasena, latitud, longitud, 
                    ciudad, region, foto_perfil, created_at, updated_at
                ))
                
                self.usuarios_migrados += 1
                print(f"  ✅ Usuario: {correo} ({nombre})")
                
            except Exception as e:
                error_msg = f"Error migrando usuario: {str(e)}"
                self.errores.append(error_msg)
                print(f"  ❌ {error_msg}")
        
        conn_nueva.commit()
    
    def migrar_cultivos(self, conn_antigua, conn_nueva):
        """Migrar cultivos desde tabla antigua a nueva estructura con campos adicionales"""
        cursor_antigua = conn_antigua.cursor()
        cursor_nueva = conn_nueva.cursor()
        
        # Verificar si existe tabla cultivos en BD antigua
        cursor_antigua.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cultivos'")
        if not cursor_antigua.fetchone():
            print(f"\n🌾 No se encontró tabla 'cultivos' en BD antigua - omitiendo migración de cultivos")
            return
        
        # Leer cultivos desde tabla antigua
        cursor_antigua.execute("SELECT * FROM cultivos")
        cultivos_antiguos = cursor_antigua.fetchall()
        
        print(f"\n🌾 Migrando {len(cultivos_antiguos)} cultivos...")
        
        # Obtener nombres de columnas de la tabla antigua
        cursor_antigua.execute("PRAGMA table_info(cultivos)")
        columnas_antigas = [col[1] for col in cursor_antigua.fetchall()]
        print(f"  📋 Columnas en BD antigua: {', '.join(columnas_antigas)}")
        
        for cultivo_antiguo in cultivos_antiguos:
            try:
                # Mapear datos antiguos (asumiendo estructura básica)
                if len(cultivo_antiguo) >= 6:  # Mínimo: id, usuario_correo, nombre_cultivo, hectareas, fecha_siembra, notas
                    id_antiguo = cultivo_antiguo[0]
                    usuario_correo = cultivo_antiguo[1] 
                    nombre_cultivo = cultivo_antiguo[2]
                    hectareas = cultivo_antiguo[3]
                    fecha_siembra = cultivo_antiguo[4] if len(cultivo_antiguo) > 4 else None
                    notas = cultivo_antiguo[5] if len(cultivo_antiguo) > 5 else None
                    created_at = cultivo_antiguo[6] if len(cultivo_antiguo) > 6 else datetime.now().isoformat()
                    
                    # Insertar en nueva estructura con campos adicionales
                    cursor_nueva.execute('''
                        INSERT INTO cultivos 
                        (usuario_correo, nombre_cultivo, hectareas, fecha_siembra, notas,
                         etapa_planta, tipo_riego, ultimo_riego, frecuencia_riego, humedad_suelo, 
                         textura_suelo, variedad_planta, estado_planta, estres_hidrico, 
                         profundidad_radical, densidad_plantacion, tipo_sensor, eficiencia_riego, 
                         caudal, ph_agua, acolchado, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        usuario_correo,
                        nombre_cultivo,
                        float(hectareas) if hectareas else 0.0,
                        fecha_siembra,
                        notas,
                        # Valores por defecto para nuevos campos
                        'No especificada',  # etapa_planta
                        'No especificado',  # tipo_riego
                        None,               # ultimo_riego
                        'No especificada',  # frecuencia_riego
                        'No medida',        # humedad_suelo
                        'No analizada',     # textura_suelo
                        'No especificada',  # variedad_planta
                        'Activo',           # estado_planta
                        'Normal',           # estres_hidrico
                        0,                  # profundidad_radical
                        0,                  # densidad_plantacion
                        'No instalado',     # tipo_sensor
                        0,                  # eficiencia_riego
                        0,                  # caudal
                        7,                  # ph_agua (neutro por defecto)
                        'Sin acolchado',    # acolchado
                        created_at
                    ))
                    
                    self.cultivos_migrados += 1
                    print(f"  ✅ Cultivo migrado: {nombre_cultivo} ({hectareas} ha) - Usuario: {usuario_correo}")
                
            except Exception as e:
                error_msg = f"Error migrando cultivo ID {id_antiguo}: {str(e)}"
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