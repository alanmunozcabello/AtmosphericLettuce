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
    def __init__(self, db_antigua="src/data/DataBase.db", db_nueva="src/data/usuarios_nueva.db", db_respaldo="src/data/DataBaseCopy.db"):
        self.db_antigua = db_antigua
        self.db_nueva = db_nueva
        self.db_respaldo = db_respaldo
        self.usuarios_migrados = 0
        self.cultivos_migrados = 0
        self.errores = []
    
    def verificar_archivos(self):
        """Verificar que existe la BD antigua, respaldo o preparar para crear nueva vacía"""
        bd_antigua_existe = os.path.exists(self.db_antigua)
        bd_respaldo_existe = os.path.exists(self.db_respaldo)
        
        # Crear directorio para la nueva BD si no existe
        db_dir = os.path.dirname(self.db_nueva)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        
        if bd_antigua_existe:
            print(f"✅ BD principal encontrada: {self.db_antigua}")
            print(f"📁 BD nueva se creará con datos migrados en: {self.db_nueva}")
            return self.db_antigua
        elif bd_respaldo_existe:
            print(f"⚠️  BD principal NO encontrada: {self.db_antigua}")
            print(f"✅ Usando BD de respaldo: {self.db_respaldo}")
            print(f"📁 BD nueva se creará con datos del respaldo en: {self.db_nueva}")
            return self.db_respaldo
        else:
            print(f"⚠️  BD principal NO encontrada: {self.db_antigua}")
            print(f"⚠️  BD respaldo NO encontrada: {self.db_respaldo}")
            print(f"📁 Se creará BD nueva VACÍA con estructura completa en: {self.db_nueva}")
            return None
    
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
                puntos TEXT,
                
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
    
    def obtener_estructura_bd_antigua(self, conn_antigua):
        """Detectar la estructura de la BD antigua"""
        cursor = conn_antigua.cursor()
        cursor.execute("PRAGMA table_info(usuarios)")
        columnas = cursor.fetchall()
        
        columnas_dict = {col[1]: col[0] for col in columnas}  # nombre: índice
        print(f"\n📋 Estructura de BD antigua detectada:")
        print(f"   Columnas encontradas: {', '.join(columnas_dict.keys())}")
        
        return columnas_dict
    
    def migrar_usuarios(self, conn_antigua, conn_nueva):
        """Migrar usuarios desde BD antigua (sin cultivos)"""
        cursor_antigua = conn_antigua.cursor()
        cursor_nueva = conn_nueva.cursor()
        
        # Detectar estructura
        columnas = self.obtener_estructura_bd_antigua(conn_antigua)
        
        # Leer usuarios de BD antigua
        cursor_antigua.execute("SELECT * FROM usuarios")
        usuarios_antiguos = cursor_antigua.fetchall()
        
        print(f"\n📄 Usuarios encontrados en BD antigua: {len(usuarios_antiguos)}")
        
        for usuario in usuarios_antiguos:
            try:
                # Extraer datos según columnas disponibles
                correo = usuario[columnas['correo']]
                nombre = usuario[columnas['nombre']]
                contrasena = usuario[columnas['contrasena']]
                latitud = usuario[columnas['latitud']] if 'latitud' in columnas else None
                longitud = usuario[columnas['longitud']] if 'longitud' in columnas else None
                ciudad = usuario[columnas['ciudad']] if 'ciudad' in columnas else None
                region = usuario[columnas['region']] if 'region' in columnas else None
                # cultivos se migran por separado
                created_at = usuario[columnas['created_at']] if 'created_at' in columnas else datetime.now().isoformat()
                updated_at = usuario[columnas['updated_at']] if 'updated_at' in columnas else datetime.now().isoformat()
                
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
        
        # Verificar si existe la columna cultivos en usuarios
        cursor_antigua.execute("PRAGMA table_info(usuarios)")
        columnas = [col[1] for col in cursor_antigua.fetchall()]
        
        # Verificar si existe tabla cultivos
        cursor_antigua.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cultivos'")
        tabla_cultivos_existe = cursor_antigua.fetchone() is not None
        
        if tabla_cultivos_existe:
            # Migrar desde tabla cultivos existente
            print(f"\n🌾 Tabla 'cultivos' encontrada en BD antigua")
            self.migrar_desde_tabla_cultivos(cursor_antigua, cursor_nueva, conn_nueva)
        elif 'cultivos' in columnas:
            # Migrar desde columna JSON en usuarios
            print(f"\n🌾 Migrando cultivos desde columna JSON en usuarios")
            self.migrar_desde_json_cultivos(cursor_antigua, cursor_nueva, conn_antigua, conn_nueva)
        else:
            print(f"\n⚠️  No se encontraron cultivos para migrar")
            print(f"   - No existe tabla 'cultivos'")
            print(f"   - No existe columna 'cultivos' en usuarios")
            print(f"   Columnas en usuarios: {', '.join(columnas)}")
    
    def migrar_desde_tabla_cultivos(self, cursor_antigua, cursor_nueva, conn_nueva):
        """Migrar cultivos desde tabla cultivos existente"""
        cursor_antigua.execute("SELECT * FROM cultivos")
        cultivos_antiguos = cursor_antigua.fetchall()
        
        # Obtener nombres de columnas
        cursor_antigua.execute("PRAGMA table_info(cultivos)")
        columnas_info = cursor_antigua.fetchall()
        columnas = {col[1]: col[0] for col in columnas_info}
        
        print(f"   Cultivos encontrados: {len(cultivos_antiguos)}")
        print(f"   Columnas: {', '.join(columnas.keys())}")
        
        for cultivo in cultivos_antiguos:
            try:
                # Extraer datos según estructura existente
                datos = {
                    'usuario_correo': cultivo[columnas['usuario_correo']] if 'usuario_correo' in columnas else None,
                    'nombre_cultivo': cultivo[columnas['nombre_cultivo']] if 'nombre_cultivo' in columnas else None,
                    'hectareas': cultivo[columnas['hectareas']] if 'hectareas' in columnas else 0.0,
                    'fecha_siembra': cultivo[columnas['fecha_siembra']] if 'fecha_siembra' in columnas else None,
                    'notas': cultivo[columnas['notas']] if 'notas' in columnas else None,
                    'puntos': cultivo[columnas['puntos']] if 'puntos' in columnas else None,
                    'etapa_planta': cultivo[columnas['etapa_planta']] if 'etapa_planta' in columnas else None,
                    'tipo_riego': cultivo[columnas['tipo_riego']] if 'tipo_riego' in columnas else None,
                    'ultimo_riego': cultivo[columnas['ultimo_riego']] if 'ultimo_riego' in columnas else None,
                    'frecuencia_riego': cultivo[columnas['frecuencia_riego']] if 'frecuencia_riego' in columnas else None,
                    'humedad_suelo': cultivo[columnas['humedad_suelo']] if 'humedad_suelo' in columnas else None,
                    'textura_suelo': cultivo[columnas['textura_suelo']] if 'textura_suelo' in columnas else None,
                    'variedad_planta': cultivo[columnas['variedad_planta']] if 'variedad_planta' in columnas else None,
                    'estado_planta': cultivo[columnas['estado_planta']] if 'estado_planta' in columnas else None,
                    'estres_hidrico': cultivo[columnas['estres_hidrico']] if 'estres_hidrico' in columnas else 0,
                    'profundidad_radical': cultivo[columnas['profundidad_radical']] if 'profundidad_radical' in columnas else None,
                    'densidad_plantacion': cultivo[columnas['densidad_plantacion']] if 'densidad_plantacion' in columnas else None,
                    'tipo_sensor': cultivo[columnas['tipo_sensor']] if 'tipo_sensor' in columnas else None,
                    'eficiencia_riego': cultivo[columnas['eficiencia_riego']] if 'eficiencia_riego' in columnas else None,
                    'caudal': cultivo[columnas['caudal']] if 'caudal' in columnas else None,
                    'pH_agua': cultivo[columnas['pH_agua']] if 'pH_agua' in columnas else None,
                    'acolchado': cultivo[columnas['acolchado']] if 'acolchado' in columnas else 0,
                    'created_at': cultivo[columnas['created_at']] if 'created_at' in columnas else datetime.now().isoformat()
                }
                
                cursor_nueva.execute('''
                    INSERT INTO cultivos 
                    (usuario_correo, nombre_cultivo, hectareas, fecha_siembra, notas, puntos,
                     etapa_planta, tipo_riego, ultimo_riego, frecuencia_riego, humedad_suelo,
                     textura_suelo, variedad_planta, estado_planta, estres_hidrico, 
                     profundidad_radical, densidad_plantacion, tipo_sensor, eficiencia_riego,
                     caudal, pH_agua, acolchado, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    datos['usuario_correo'], datos['nombre_cultivo'], datos['hectareas'],
                    datos['fecha_siembra'], datos['notas'], datos['puntos'],
                    datos['etapa_planta'], datos['tipo_riego'], datos['ultimo_riego'],
                    datos['frecuencia_riego'], datos['humedad_suelo'], datos['textura_suelo'],
                    datos['variedad_planta'], datos['estado_planta'], datos['estres_hidrico'],
                    datos['profundidad_radical'], datos['densidad_plantacion'], datos['tipo_sensor'],
                    datos['eficiencia_riego'], datos['caudal'], datos['pH_agua'],
                    datos['acolchado'], datos['created_at']
                ))
                
                self.cultivos_migrados += 1
                print(f"  ✅ Cultivo: {datos['usuario_correo']} → {datos['nombre_cultivo']} ({datos['hectareas']} ha)")
                
            except Exception as e:
                error_msg = f"Error migrando cultivo: {str(e)}"
                self.errores.append(error_msg)
                print(f"  ❌ {error_msg}")
        
        conn_nueva.commit()
    
    def migrar_desde_json_cultivos(self, cursor_antigua, cursor_nueva, conn_antigua, conn_nueva):
        """Migrar cultivos desde columna JSON en tabla usuarios"""
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
                            (usuario_correo, nombre_cultivo, hectareas, puntos, created_at)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            correo,
                            nombre_cultivo,
                            float(hectareas) if hectareas else 0.0,
                            None,  # puntos inicialmente NULL
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
            db_a_usar = self.verificar_archivos()
            
            # 2. Abrir conexiones
            print("\n2️⃣ Conectando a bases de datos...")
            conn_nueva = sqlite3.connect(self.db_nueva)
            
            # 3. Crear nueva estructura
            print("\n3️⃣ Creando nueva estructura...")
            cursor_nueva = conn_nueva.cursor()
            self.crear_nueva_estructura(cursor_nueva)
            
            if db_a_usar:
                # Solo migrar si existe BD antigua o respaldo
                conn_antigua = sqlite3.connect(db_a_usar)
                
                # 4. Migrar usuarios
                print("\n4️⃣ Migrando usuarios...")
                self.migrar_usuarios(conn_antigua, conn_nueva)
                
                # 5. Migrar cultivos
                print("\n5️⃣ Migrando cultivos...")
                self.migrar_cultivos(conn_antigua, conn_nueva)
                
                # Cerrar conexión antigua
                conn_antigua.close()
            else:
                print("\n4️⃣ Omitiendo migración de datos (ninguna BD fuente encontrada)")
                print("   ✅ BD nueva creada con estructura vacía")
            
            # 6. Verificar migración
            print("\n5️⃣ Verificando estructura...")
            total_usuarios, total_cultivos, usuarios_con_cultivos = self.verificar_migracion(conn_nueva)
            
            # Cerrar conexión nueva
            conn_nueva.close()
            
            # 7. Resumen final
            self.mostrar_resumen(total_usuarios, total_cultivos, db_a_usar)
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def mostrar_resumen(self, total_usuarios, total_cultivos, db_a_usar):
        """Mostrar resumen de la migración"""
        if db_a_usar:
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
            
            print(f"\n📁 BD fuente: {db_a_usar}")
            print(f"📁 Nueva base de datos: {self.db_nueva}")
            print("🔧 Próximos pasos:")
            print("   1. Verificar nueva estructura con script verificar_migracion.py")
            print("   2. Actualizar código de la aplicación")
            print("   3. Probar funcionalidades")
            print("   4. Reemplazar BD antigua con nueva")
        else:
            print("\n🎉 BASE DE DATOS NUEVA CREADA")
            print("=" * 40)
            print(f"✅ Estructura completa creada")
            print(f"📊 Estado:")
            print(f"   - Usuarios: 0 (vacía)")
            print(f"   - Cultivos: 0 (vacía)")
            print(f"   - Tablas: ✅ usuarios, cultivos")
            print(f"   - Índices: ✅ 5 índices creados")
            print(f"   - Foreign Keys: ✅ Configuradas")
            print(f"\n📁 Base de datos creada en: {self.db_nueva}")
            print("🔧 Próximos pasos:")
            print("   1. Renombrar a 'DataBase.db' o usar como nueva BD")
            print("   2. Comenzar a agregar usuarios y cultivos")
            print("   3. ¡Listo para usar!")

def main():
    """Función principal"""
    # Rutas por defecto
    db_antigua = "src/data/DataBase.db"
    db_nueva = "src/data/usuarios_nueva.db"
    db_respaldo = "src/data/DataBaseCopy.db"
    
    # Permitir argumentos personalizados
    if len(sys.argv) > 1:
        db_antigua = sys.argv[1]
    if len(sys.argv) > 2:
        db_nueva = sys.argv[2]
    if len(sys.argv) > 3:
        db_respaldo = sys.argv[3]
    
    # Ejecutar migración
    migrador = Migrador(db_antigua, db_nueva, db_respaldo)
    exito = migrador.ejecutar_migracion()
    
    if exito:
        print("\n✨ ¡Migración exitosa!")
        sys.exit(0)
    else:
        print("\n💥 Migración falló")
        sys.exit(1)

if __name__ == "__main__":
    main()