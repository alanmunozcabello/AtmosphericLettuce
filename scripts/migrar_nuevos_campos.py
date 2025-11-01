"""
Script para agregar campos 'notificaciones' a usuarios y 'consejos_ia' a cultivos
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "src" / "data" / "DataBase.db"

def migrar_campos_nuevos():
    print("=" * 60)
    print("🔄 MIGRACIÓN: Agregar campos nuevos")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Agregar campo 'notificaciones' a usuarios
        print("\n1️⃣ Agregando campo 'notificaciones' a usuarios...")
        try:
            cursor.execute("""
                ALTER TABLE usuarios 
                ADD COLUMN notificaciones INTEGER DEFAULT 1
            """)
            print("   ✅ Campo 'notificaciones' agregado")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("   ⚠️ Campo 'notificaciones' ya existe")
            else:
                raise e
        
        # 2. Agregar campo 'consejos_ia' a cultivos
        print("\n2️⃣ Agregando campo 'consejos_ia' a cultivos...")
        try:
            cursor.execute("""
                ALTER TABLE cultivos 
                ADD COLUMN consejos_ia TEXT DEFAULT 'Aquí están los consejos de la IA'
            """)
            print("   ✅ Campo 'consejos_ia' agregado")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("   ⚠️ Campo 'consejos_ia' ya existe")
            else:
                raise e
        
        # 3. Actualizar usuarios existentes con notificaciones = True
        print("\n3️⃣ Actualizando usuarios existentes...")
        cursor.execute("""
            UPDATE usuarios 
            SET notificaciones = 1 
            WHERE notificaciones IS NULL
        """)
        usuarios_actualizados = cursor.rowcount
        print(f"   ✅ {usuarios_actualizados} usuarios actualizados")
        
        # 4. Actualizar cultivos existentes con mensaje por defecto
        print("\n4️⃣ Actualizando cultivos existentes...")
        cursor.execute("""
            UPDATE cultivos 
            SET consejos_ia = 'Aquí están los consejos de la IA' 
            WHERE consejos_ia IS NULL
        """)
        cultivos_actualizados = cursor.rowcount
        print(f"   ✅ {cultivos_actualizados} cultivos actualizados")
        
        # Guardar cambios
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\n📋 Resumen:")
        print(f"   • Campo 'notificaciones' agregado a tabla usuarios")
        print(f"   • Campo 'consejos_ia' agregado a tabla cultivos")
        print(f"   • {usuarios_actualizados} usuarios actualizados")
        print(f"   • {cultivos_actualizados} cultivos actualizados")
        print("\n🚀 Ya puedes reiniciar tu servidor FastAPI")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    migrar_campos_nuevos()
