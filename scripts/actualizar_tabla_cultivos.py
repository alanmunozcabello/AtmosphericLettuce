#!/usr/bin/env python3
"""
Script para actualizar la tabla cultivos con los nuevos campos
AtmosphericLettuce - Actualización de estructura
"""

import sqlite3
import os

DB_PATH = "src/data/usuarios.db"

def main():
    print("🥬 ATMOSPHERIC LETTUCE - Actualizar Tabla Cultivos")
    print("=" * 70)
    
    if not os.path.exists(DB_PATH):
        print(f"❌ No se encontró la base de datos: {DB_PATH}")
        return False
    
    print(f"✅ Base de datos encontrada: {DB_PATH}\n")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Ver columnas actuales
        print("📋 Columnas actuales en la tabla cultivos:")
        cursor.execute("PRAGMA table_info(cultivos)")
        columnas_actuales = [col[1] for col in cursor.fetchall()]
        for col in columnas_actuales:
            print(f"  - {col}")
        
        print(f"\n🔧 Agregando nuevas columnas...")
        
        # Lista de columnas a agregar
        columnas_nuevas = [
            ("etapa_planta", "TEXT"),
            ("tipo_riego", "TEXT"),
            ("ultimo_riego", "DATETIME"),
            ("frecuencia_riego", "TEXT"),
            ("humedad_suelo", "TEXT"),
            ("textura_suelo", "TEXT"),
            ("variedad_planta", "TEXT"),
            ("estado_planta", "TEXT"),
            ("estres_hidrico", "INTEGER", "0"),
            ("profundidad_radical", "INTEGER"),
            ("densidad_plantacion", "INTEGER"),
            ("tipo_sensor", "TEXT"),
            ("eficiencia_riego", "REAL"),
            ("caudal", "REAL"),
            ("pH_agua", "REAL"),
            ("acolchado", "INTEGER", "0"),
        ]
        
        agregadas = 0
        for columna_info in columnas_nuevas:
            nombre = columna_info[0]
            tipo = columna_info[1]
            default = columna_info[2] if len(columna_info) > 2 else None
            
            if nombre not in columnas_actuales:
                try:
                    if default:
                        query = f"ALTER TABLE cultivos ADD COLUMN {nombre} {tipo} DEFAULT {default}"
                    else:
                        query = f"ALTER TABLE cultivos ADD COLUMN {nombre} {tipo}"
                    
                    cursor.execute(query)
                    print(f"  ✅ Agregada: {nombre} ({tipo})")
                    agregadas += 1
                except Exception as e:
                    print(f"  ❌ Error con {nombre}: {str(e)}")
            else:
                print(f"  ⏭️  Ya existe: {nombre}")
        
        conn.commit()
        
        # Verificar estructura final
        cursor.execute("PRAGMA table_info(cultivos)")
        columnas_finales = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) FROM cultivos")
        total = cursor.fetchone()[0]
        
        print(f"\n📊 RESUMEN:")
        print(f"  - Columnas agregadas: {agregadas}")
        print(f"  - Total de columnas: {len(columnas_finales)}")
        print(f"  - Total de registros: {total}")
        
        conn.close()
        
        print(f"\n🎉 ¡Actualización completada!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    main()
