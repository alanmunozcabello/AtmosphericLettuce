#!/usr/bin/env python3
"""
Script para crear tabla de clima guardado
AtmosphericLettuce - Sistema de Alertas
"""

import sqlite3
import os

# Detectar la ruta correcta de la base de datos
if os.path.exists("src/data/DataBase.db"):
    DB_PATH = "src/data/DataBase.db"
elif os.path.exists("data/DataBase.db"):
    DB_PATH = "data/DataBase.db"
elif os.path.exists("../src/data/DataBase.db"):
    DB_PATH = "../src/data/DataBase.db"
else:
    DB_PATH = None


def main():
    print("🥬 ATMOSPHERIC LETTUCE - Crear Tabla de Clima")
    print("=" * 70)
    
    if DB_PATH is None:
        print("❌ No se encontró la base de datos DataBase.db")
        print("💡 Rutas buscadas:")
        print("  - src/data/DataBase.db")
        print("  - data/DataBase.db")
        print("  - ../src/data/DataBase.db")
        print("\n🔧 Solución: Ejecuta desde la raíz del proyecto o desde src/")
        return False
    
    print(f"✅ Base de datos encontrada: {DB_PATH}\n")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("📊 Creando tabla: clima_guardado")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clima_guardado (
                correo TEXT NOT NULL,
                cultivo_nombre TEXT NOT NULL,
                fecha_guardado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                latitud REAL NOT NULL,
                longitud REAL NOT NULL,
                clima_json TEXT NOT NULL,
                PRIMARY KEY (correo, cultivo_nombre),
                FOREIGN KEY (correo) REFERENCES usuarios(correo) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        
        print("  ✅ Tabla clima_guardado creada")
        print("  ✅ Clave primaria: (correo, cultivo_nombre)\n")
        
        # Verificación
        print("🔍 Verificando estructura...")
        cursor.execute("PRAGMA table_info(clima_guardado)")
        columnas = cursor.fetchall()
        
        print(f"\n📋 Estructura de clima_guardado ({len(columnas)} columnas):")
        for col in columnas:
            pk = " [PK]" if col[5] else ""
            print(f"  - {col[1]} ({col[2]}){pk}")
        
        conn.close()
        
        print(f"\n🎉 ¡Tabla creada exitosamente!")
        print("\n💡 Uso:")
        print("  - Cada usuario puede tener múltiples cultivos")
        print("  - Cada combinación correo+cultivo guarda UN clima")
        print("  - Si guardas de nuevo, ACTUALIZA el registro existente")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
