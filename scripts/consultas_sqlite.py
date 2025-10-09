#!/usr/bin/env python3
"""
Consultas SQL para la base de datos de usuarios
Permite hacer consultas interactivas
"""

import sqlite3
import json
import sys

def ejecutar_consulta(query, db_path="src/data/usuarios.db"):
    """Ejecutar una consulta SQL"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            # Es una consulta de selección
            resultados = cursor.fetchall()
            columnas = [description[0] for description in cursor.description]
            
            print(f"📊 Resultados ({len(resultados)} filas):")
            print("-" * 50)
            
            # Mostrar encabezados
            print(" | ".join(f"{col:15}" for col in columnas))
            print("-" * (17 * len(columnas)))
            
            # Mostrar datos
            for fila in resultados:
                valores = []
                for valor in fila:
                    if valor is None:
                        valores.append("NULL")
                    elif isinstance(valor, str) and len(valor) > 15:
                        valores.append(valor[:12] + "...")
                    else:
                        valores.append(str(valor))
                
                print(" | ".join(f"{val:15}" for val in valores))
        
        else:
            # Es una consulta de modificación
            conn.commit()
            print(f"✅ Consulta ejecutada. Filas afectadas: {cursor.rowcount}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Error SQL: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def consultas_predefinidas(db_path="src/data/usuarios.db"):
    """Mostrar menú de consultas predefinidas"""
    
    consultas = {
        "1": ("Todos los usuarios", "SELECT correo, nombre, ciudad, region FROM usuarios"),
        "2": ("Usuarios con cultivos", "SELECT correo, nombre FROM usuarios WHERE cultivos != '{}'"),
        "3": ("Usuarios por región", "SELECT region, COUNT(*) as cantidad FROM usuarios WHERE region IS NOT NULL GROUP BY region"),
        "4": ("Usuarios sin ubicación", "SELECT correo, nombre FROM usuarios WHERE ciudad IS NULL OR ciudad = ''"),
        "5": ("Cultivos más comunes", """
            SELECT 
                json_extract(value, '$') as cultivo,
                COUNT(*) as usuarios
            FROM usuarios, json_each(usuarios.cultivos) 
            WHERE json_valid(usuarios.cultivos)
            GROUP BY json_extract(value, '$')
            ORDER BY usuarios DESC
        """),
        "6": ("Estadísticas generales", """
            SELECT 
                'Total usuarios' as metrica, COUNT(*) as valor FROM usuarios
            UNION ALL
            SELECT 'Con ciudad', COUNT(*) FROM usuarios WHERE ciudad IS NOT NULL AND ciudad != ''
            UNION ALL
            SELECT 'Con coordenadas', COUNT(*) FROM usuarios WHERE latitud IS NOT NULL
            UNION ALL
            SELECT 'Con cultivos', COUNT(*) FROM usuarios WHERE cultivos != '{}'
        """)
    }
    
    print("🔍 CONSULTAS PREDEFINIDAS")
    print("=" * 25)
    
    for key, (descripcion, _) in consultas.items():
        print(f"{key}. {descripcion}")
    
    print("0. Salir")
    print("c. Consulta personalizada")
    
    while True:
        opcion = input(f"\n🔧 Selecciona una opción: ").strip()
        
        if opcion == "0":
            break
        elif opcion == "c":
            query = input("📝 Ingresa tu consulta SQL: ")
            if query.strip():
                ejecutar_consulta(query, db_path)
        elif opcion in consultas:
            descripcion, query = consultas[opcion]
            print(f"\n🔍 {descripcion}")
            ejecutar_consulta(query, db_path)
        else:
            print("❌ Opción inválida")

def main():
    """Función principal"""
    db_path = "src/data/usuarios.db"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--query" and len(sys.argv) > 2:
            # Ejecutar consulta directa
            query = " ".join(sys.argv[2:])
            ejecutar_consulta(query, db_path)
        else:
            # Usar ruta personalizada
            db_path = sys.argv[1]
            consultas_predefinidas(db_path)
    else:
        # Menú interactivo
        consultas_predefinidas(db_path)

if __name__ == "__main__":
    main()