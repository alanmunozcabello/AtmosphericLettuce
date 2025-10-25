#!/usr/bin/env python3
"""
Script de Verificación de Migración
AtmosphericLettuce - Verifica la integridad de la base de datos migrada

Verifica:
- Estructura de tablas
- Integridad de datos
- Relaciones entre tablas
- Consistencia de datos
"""

import sqlite3
import json
import sys
from datetime import datetime
from pathlib import Path

class VerificadorMigracion:
    def __init__(self, db_antigua="src/data/DataBase.db", db_nueva="src/data/usuarios_nueva.db", db_respaldo="src/data/DataBaseCopy.db"):
        self.db_antigua = db_antigua
        self.db_nueva = db_nueva
        self.db_respaldo = db_respaldo
        self.errores = []
        self.advertencias = []
    
    def verificar_existencia_bd(self):
        """Verificar que existen las bases de datos necesarias"""
        print("🔍 Verificando existencia de bases de datos...")
        
        bd_antigua_existe = Path(self.db_antigua).exists()
        bd_respaldo_existe = Path(self.db_respaldo).exists()
        bd_nueva_existe = Path(self.db_nueva).exists()
        
        # Determinar qué BD antigua usar
        if bd_antigua_existe:
            self.db_fuente = self.db_antigua
            print(f"   ✅ BD principal: {self.db_antigua}")
        elif bd_respaldo_existe:
            self.db_fuente = self.db_respaldo
            print(f"   ⚠️  BD principal no encontrada: {self.db_antigua}")
            print(f"   ✅ Usando BD respaldo: {self.db_respaldo}")
        else:
            self.errores.append(f"❌ No se encontró BD principal ({self.db_antigua}) ni respaldo ({self.db_respaldo})")
            return False
        
        if not bd_nueva_existe:
            self.errores.append(f"❌ BD nueva no encontrada: {self.db_nueva}")
            return False
        
        print(f"   ✅ BD nueva: {self.db_nueva}")
        return True
    
    def verificar_estructura_tablas(self, conn):
        """Verificar que las tablas necesarias existen con la estructura correcta"""
        print("\n🏗️  Verificando estructura de tablas...")
        cursor = conn.cursor()
        
        # Verificar tabla usuarios
        cursor.execute("PRAGMA table_info(usuarios)")
        columnas_usuarios = {col[1]: col[2] for col in cursor.fetchall()}
        
        columnas_esperadas_usuarios = {
            'correo': 'TEXT',
            'nombre': 'TEXT',
            'contrasena': 'TEXT',
            'latitud': 'REAL',
            'longitud': 'REAL',
            'ciudad': 'TEXT',
            'region': 'TEXT',
            'foto_perfil': 'TEXT',
            'created_at': 'DATETIME',
            'updated_at': 'DATETIME'
        }
        
        print("   📋 Tabla usuarios:")
        for col, tipo in columnas_esperadas_usuarios.items():
            if col in columnas_usuarios:
                print(f"      ✅ {col} ({tipo})")
            else:
                error = f"Columna faltante en usuarios: {col}"
                self.errores.append(error)
                print(f"      ❌ {error}")
        
        # Verificar tabla cultivos
        cursor.execute("PRAGMA table_info(cultivos)")
        columnas_cultivos = {col[1]: col[2] for col in cursor.fetchall()}
        
        columnas_esperadas_cultivos = {
            'id': 'INTEGER',
            'usuario_correo': 'TEXT',
            'nombre_cultivo': 'TEXT',
            'hectareas': 'REAL',
            'fecha_siembra': 'DATE',
            'notas': 'TEXT',
            'puntos': 'TEXT',
            'etapa_planta': 'TEXT',
            'tipo_riego': 'TEXT',
            'ultimo_riego': 'DATETIME',
            'frecuencia_riego': 'TEXT',
            'humedad_suelo': 'TEXT',
            'textura_suelo': 'TEXT',
            'variedad_planta': 'TEXT',
            'estado_planta': 'TEXT',
            'estres_hidrico': 'INTEGER',
            'profundidad_radical': 'INTEGER',
            'densidad_plantacion': 'INTEGER',
            'tipo_sensor': 'TEXT',
            'eficiencia_riego': 'REAL',
            'caudal': 'REAL',
            'pH_agua': 'REAL',
            'acolchado': 'INTEGER',
            'created_at': 'DATETIME'
        }
        
        print("\n   📋 Tabla cultivos:")
        for col, tipo in columnas_esperadas_cultivos.items():
            if col in columnas_cultivos:
                print(f"      ✅ {col} ({tipo})")
            else:
                error = f"Columna faltante en cultivos: {col}"
                self.errores.append(error)
                print(f"      ❌ {error}")
        
        # Verificar índices
        print("\n   📋 Índices:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
        indices = [row[0] for row in cursor.fetchall()]
        
        indices_esperados = [
            'idx_usuarios_nombre',
            'idx_usuarios_ciudad',
            'idx_usuarios_region',
            'idx_cultivos_usuario',
            'idx_cultivos_nombre'
        ]
        
        for indice in indices_esperados:
            if indice in indices:
                print(f"      ✅ {indice}")
            else:
                advertencia = f"Índice faltante: {indice}"
                self.advertencias.append(advertencia)
                print(f"      ⚠️  {advertencia}")
        
        return len(self.errores) == 0
    
    def verificar_conteo_registros(self, conn_antigua, conn_nueva):
        """Verificar que el número de registros coincide"""
        print("\n📊 Verificando conteo de registros...")
        
        cursor_antigua = conn_antigua.cursor()
        cursor_nueva = conn_nueva.cursor()
        
        # Contar usuarios
        cursor_antigua.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_antiguos = cursor_antigua.fetchone()[0]
        
        cursor_nueva.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_nuevos = cursor_nueva.fetchone()[0]
        
        print(f"\n   👥 Usuarios:")
        print(f"      BD antigua: {usuarios_antiguos}")
        print(f"      BD nueva:   {usuarios_nuevos}")
        
        if usuarios_antiguos == usuarios_nuevos:
            print(f"      ✅ Coinciden")
        else:
            error = f"Diferencia en usuarios: {usuarios_antiguos} vs {usuarios_nuevos}"
            self.errores.append(error)
            print(f"      ❌ {error}")
        
        # Verificar si existe tabla cultivos en BD antigua
        cursor_antigua.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cultivos'")
        tabla_cultivos_existe = cursor_antigua.fetchone() is not None
        
        if tabla_cultivos_existe:
            # Contar cultivos desde tabla
            cursor_antigua.execute("SELECT COUNT(*) FROM cultivos")
            total_cultivos_antiguos = cursor_antigua.fetchone()[0]
            print(f"\n   🌾 Cultivos (desde tabla 'cultivos'):")
        else:
            # Contar cultivos desde JSON en usuarios
            cursor_antigua.execute("PRAGMA table_info(usuarios)")
            columnas = [col[1] for col in cursor_antigua.fetchall()]
            
            if 'cultivos' in columnas:
                cursor_antigua.execute("SELECT cultivos FROM usuarios WHERE cultivos IS NOT NULL AND cultivos != '{}'")
                total_cultivos_antiguos = 0
                for (cultivos_json,) in cursor_antigua.fetchall():
                    try:
                        cultivos = json.loads(cultivos_json)
                        total_cultivos_antiguos += len(cultivos)
                    except:
                        pass
                print(f"\n   🌾 Cultivos (desde columna JSON en usuarios):")
            else:
                total_cultivos_antiguos = 0
                print(f"\n   🌾 Cultivos (no encontrados en BD antigua):")
        
        cursor_nueva.execute("SELECT COUNT(*) FROM cultivos")
        cultivos_nuevos = cursor_nueva.fetchone()[0]
        
        print(f"      BD antigua: {total_cultivos_antiguos}")
        print(f"      BD nueva:   {cultivos_nuevos}")
        
        if total_cultivos_antiguos == cultivos_nuevos:
            print(f"      ✅ Coinciden")
        else:
            if total_cultivos_antiguos == 0:
                advertencia = f"BD antigua sin cultivos, BD nueva tiene {cultivos_nuevos}"
                self.advertencias.append(advertencia)
                print(f"      ⚠️  {advertencia}")
            else:
                error = f"Diferencia en cultivos: {total_cultivos_antiguos} vs {cultivos_nuevos}"
                self.errores.append(error)
                print(f"      ❌ {error}")
        
        return usuarios_antiguos, usuarios_nuevos, total_cultivos_antiguos, cultivos_nuevos
    
    def verificar_integridad_referencial(self, conn_nueva):
        """Verificar que todas las foreign keys son válidas"""
        print("\n🔗 Verificando integridad referencial...")
        cursor = conn_nueva.cursor()
        
        # Verificar que todos los cultivos tienen un usuario válido
        cursor.execute("""
            SELECT COUNT(*) 
            FROM cultivos c
            LEFT JOIN usuarios u ON c.usuario_correo = u.correo
            WHERE u.correo IS NULL
        """)
        cultivos_huerfanos = cursor.fetchone()[0]
        
        if cultivos_huerfanos == 0:
            print("   ✅ Todos los cultivos tienen un usuario válido")
        else:
            error = f"Cultivos sin usuario válido: {cultivos_huerfanos}"
            self.errores.append(error)
            print(f"   ❌ {error}")
        
        return cultivos_huerfanos == 0
    
    def verificar_datos_usuarios(self, conn_antigua, conn_nueva):
        """Verificar que los datos de usuarios coinciden"""
        print("\n👤 Verificando datos de usuarios...")
        
        cursor_antigua = conn_antigua.cursor()
        cursor_nueva = conn_nueva.cursor()
        
        cursor_antigua.execute("SELECT correo, nombre, contrasena FROM usuarios ORDER BY correo")
        usuarios_antiguos = cursor_antigua.fetchall()
        
        errores_datos = 0
        for correo, nombre, contrasena in usuarios_antiguos:
            cursor_nueva.execute(
                "SELECT nombre, contrasena FROM usuarios WHERE correo = ?",
                (correo,)
            )
            resultado = cursor_nueva.fetchone()
            
            if resultado is None:
                error = f"Usuario no encontrado en BD nueva: {correo}"
                self.errores.append(error)
                print(f"   ❌ {error}")
                errores_datos += 1
            else:
                nombre_nuevo, contrasena_nueva = resultado
                if nombre != nombre_nuevo or contrasena != contrasena_nueva:
                    error = f"Datos diferentes para usuario {correo}"
                    self.errores.append(error)
                    print(f"   ❌ {error}")
                    errores_datos += 1
        
        if errores_datos == 0:
            print(f"   ✅ Datos de {len(usuarios_antiguos)} usuarios verificados correctamente")
        else:
            print(f"   ❌ Errores en {errores_datos} usuarios")
        
        return errores_datos == 0
    
    def verificar_datos_cultivos(self, conn_antigua, conn_nueva):
        """Verificar que los datos de cultivos coinciden"""
        print("\n🌱 Verificando datos de cultivos...")
        
        cursor_antigua = conn_antigua.cursor()
        cursor_nueva = conn_nueva.cursor()
        
        # Verificar si existe tabla cultivos en BD antigua
        cursor_antigua.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cultivos'")
        tabla_cultivos_existe = cursor_antigua.fetchone() is not None
        
        errores_cultivos = 0
        cultivos_verificados = 0
        
        if tabla_cultivos_existe:
            # Verificar desde tabla cultivos
            print("   📋 Verificando desde tabla 'cultivos'...")
            cursor_antigua.execute("SELECT usuario_correo, nombre_cultivo, hectareas FROM cultivos")
            
            for correo, nombre_cultivo, hectareas in cursor_antigua.fetchall():
                cursor_nueva.execute(
                    "SELECT hectareas FROM cultivos WHERE usuario_correo = ? AND nombre_cultivo = ?",
                    (correo, nombre_cultivo)
                )
                resultado = cursor_nueva.fetchone()
                
                if resultado is None:
                    error = f"Cultivo no encontrado: {correo} - {nombre_cultivo}"
                    self.errores.append(error)
                    print(f"   ❌ {error}")
                    errores_cultivos += 1
                else:
                    hectareas_nueva = resultado[0]
                    hectareas_antigua = float(hectareas) if hectareas else 0.0
                    
                    if abs(hectareas_antigua - hectareas_nueva) > 0.001:
                        error = f"Hectáreas diferentes para {correo} - {nombre_cultivo}: {hectareas_antigua} vs {hectareas_nueva}"
                        self.errores.append(error)
                        print(f"   ❌ {error}")
                        errores_cultivos += 1
                    else:
                        cultivos_verificados += 1
        else:
            # Verificar desde columna JSON en usuarios
            cursor_antigua.execute("PRAGMA table_info(usuarios)")
            columnas = [col[1] for col in cursor_antigua.fetchall()]
            
            if 'cultivos' not in columnas:
                print("   ⚠️  No se encontró columna 'cultivos' ni tabla 'cultivos' en BD antigua")
                print("   ⏭️  Omitiendo verificación de datos de cultivos")
                return True
            
            print("   📋 Verificando desde columna JSON en usuarios...")
            cursor_antigua.execute("SELECT correo, cultivos FROM usuarios WHERE cultivos IS NOT NULL")
            
            for correo, cultivos_json in cursor_antigua.fetchall():
                try:
                    if not cultivos_json or cultivos_json == '{}':
                        continue
                    
                    cultivos = json.loads(cultivos_json)
                    
                    for nombre_cultivo, hectareas in cultivos.items():
                        cursor_nueva.execute(
                            "SELECT hectareas FROM cultivos WHERE usuario_correo = ? AND nombre_cultivo = ?",
                            (correo, nombre_cultivo)
                        )
                        resultado = cursor_nueva.fetchone()
                        
                        if resultado is None:
                            error = f"Cultivo no encontrado: {correo} - {nombre_cultivo}"
                            self.errores.append(error)
                            print(f"   ❌ {error}")
                            errores_cultivos += 1
                        else:
                            hectareas_nueva = resultado[0]
                            hectareas_antigua = float(hectareas) if hectareas else 0.0
                            
                            if abs(hectareas_antigua - hectareas_nueva) > 0.001:
                                error = f"Hectáreas diferentes para {correo} - {nombre_cultivo}: {hectareas_antigua} vs {hectareas_nueva}"
                                self.errores.append(error)
                                print(f"   ❌ {error}")
                                errores_cultivos += 1
                            else:
                                cultivos_verificados += 1
                
                except json.JSONDecodeError:
                    error = f"JSON inválido en cultivos de {correo}"
                    self.errores.append(error)
                    print(f"   ❌ {error}")
                    errores_cultivos += 1
        
        if errores_cultivos == 0:
            print(f"   ✅ {cultivos_verificados} cultivos verificados correctamente")
        else:
            print(f"   ❌ Errores en {errores_cultivos} cultivos")
        
        return errores_cultivos == 0
    
    def verificar_campo_puntos(self, conn_nueva):
        """Verificar que el campo puntos existe y es accesible"""
        print("\n📍 Verificando campo 'puntos' en cultivos...")
        cursor = conn_nueva.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM cultivos WHERE puntos IS NOT NULL")
            cultivos_con_puntos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM cultivos")
            total_cultivos = cursor.fetchone()[0]
            
            print(f"   ✅ Campo 'puntos' existe y es accesible")
            print(f"   📊 Cultivos con puntos: {cultivos_con_puntos}/{total_cultivos}")
            
            if cultivos_con_puntos > 0:
                # Mostrar ejemplo de puntos
                cursor.execute("SELECT nombre_cultivo, puntos FROM cultivos WHERE puntos IS NOT NULL LIMIT 1")
                resultado = cursor.fetchone()
                if resultado:
                    print(f"   📝 Ejemplo: {resultado[0]} -> {resultado[1][:100]}...")
            
            return True
        except Exception as e:
            error = f"Error al verificar campo puntos: {str(e)}"
            self.errores.append(error)
            print(f"   ❌ {error}")
            return False
    
    def generar_reporte_detallado(self, conn_nueva):
        """Generar reporte detallado de la BD nueva"""
        print("\n📈 Reporte detallado de BD nueva:")
        cursor = conn_nueva.cursor()
        
        # Usuarios por región
        cursor.execute("""
            SELECT region, COUNT(*) as total
            FROM usuarios
            WHERE region IS NOT NULL
            GROUP BY region
            ORDER BY total DESC
            LIMIT 5
        """)
        print("\n   🗺️  Top 5 regiones con más usuarios:")
        for region, total in cursor.fetchall():
            print(f"      - {region}: {total} usuarios")
        
        # Cultivos más comunes
        cursor.execute("""
            SELECT nombre_cultivo, COUNT(*) as total, SUM(hectareas) as total_hectareas
            FROM cultivos
            GROUP BY nombre_cultivo
            ORDER BY total DESC
            LIMIT 5
        """)
        print("\n   🌾 Top 5 cultivos más comunes:")
        for cultivo, total, hectareas in cursor.fetchall():
            print(f"      - {cultivo}: {total} cultivos, {hectareas:.2f} ha")
        
        # Usuarios con más cultivos
        cursor.execute("""
            SELECT usuario_correo, COUNT(*) as total_cultivos
            FROM cultivos
            GROUP BY usuario_correo
            ORDER BY total_cultivos DESC
            LIMIT 3
        """)
        print("\n   👨‍🌾 Top 3 usuarios con más cultivos:")
        for correo, total in cursor.fetchall():
            print(f"      - {correo}: {total} cultivos")
    
    def ejecutar_verificacion(self):
        """Ejecutar el proceso completo de verificación"""
        print("🔍 ATMOSPHERIC LETTUCE - Verificación de Migración")
        print("=" * 60)
        
        try:
            # 1. Verificar existencia
            if not self.verificar_existencia_bd():
                self.mostrar_resumen_final()
                return False
            
            # 2. Abrir conexiones
            print("\n📂 Abriendo bases de datos...")
            conn_antigua = sqlite3.connect(self.db_fuente)  # Usar db_fuente en vez de db_antigua
            conn_nueva = sqlite3.connect(self.db_nueva)
            
            # 3. Verificar estructura
            estructura_ok = self.verificar_estructura_tablas(conn_nueva)
            
            # 4. Verificar campo puntos
            puntos_ok = self.verificar_campo_puntos(conn_nueva)
            
            # 5. Verificar conteo
            stats = self.verificar_conteo_registros(conn_antigua, conn_nueva)
            
            # 6. Verificar integridad referencial
            integridad_ok = self.verificar_integridad_referencial(conn_nueva)
            
            # 7. Verificar datos de usuarios
            usuarios_ok = self.verificar_datos_usuarios(conn_antigua, conn_nueva)
            
            # 8. Verificar datos de cultivos
            cultivos_ok = self.verificar_datos_cultivos(conn_antigua, conn_nueva)
            
            # 9. Generar reporte detallado
            self.generar_reporte_detallado(conn_nueva)
            
            # Cerrar conexiones
            conn_antigua.close()
            conn_nueva.close()
            
            # 10. Mostrar resumen final
            self.mostrar_resumen_final()
            
            return len(self.errores) == 0
            
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def mostrar_resumen_final(self):
        """Mostrar resumen final de la verificación"""
        print("\n" + "=" * 60)
        print("📋 RESUMEN DE VERIFICACIÓN")
        print("=" * 60)
        
        if len(self.errores) == 0:
            print("✅ ¡VERIFICACIÓN EXITOSA!")
            print("   Todos los datos se migraron correctamente")
        else:
            print(f"❌ VERIFICACIÓN FALLÓ - {len(self.errores)} errores encontrados")
            print("\n🔴 Errores críticos:")
            for i, error in enumerate(self.errores, 1):
                print(f"   {i}. {error}")
        
        if self.advertencias:
            print(f"\n⚠️  {len(self.advertencias)} advertencias:")
            for i, advertencia in enumerate(self.advertencias, 1):
                print(f"   {i}. {advertencia}")
        
        print("\n" + "=" * 60)
        
        if len(self.errores) == 0:
            print("✨ La base de datos nueva está lista para ser usada")
            print("📝 Recuerda actualizar las rutas en tu aplicación")
        else:
            print("⚠️  NO uses la base de datos nueva hasta resolver los errores")
            print("🔧 Revisa el proceso de migración y vuelve a ejecutarlo")

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
    
    # Ejecutar verificación
    verificador = VerificadorMigracion(db_antigua, db_nueva, db_respaldo)
    exito = verificador.ejecutar_verificacion()
    
    if exito:
        print("\n✅ Verificación completada exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Verificación falló - revisa los errores")
        sys.exit(1)

if __name__ == "__main__":
    main()
