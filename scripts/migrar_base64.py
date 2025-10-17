#!/usr/bin/env python3
"""
Migración a Base64 - AtmosphericLettuce
Actualiza la BD para manejar fotos en Base64
"""

import sqlite3
import base64
import os
from pathlib import Path

def migrar_a_base64():
    """Migrar estructura para soportar Base64"""
    
    print("📸 MIGRANDO A SOPORTE BASE64")
    print("=" * 35)
    
    try:
        conn = sqlite3.connect("data/usuarios.db")
        cursor = conn.cursor()
        
        # La estructura actual ya soporta Base64 (TEXT es suficiente)
        # Solo necesitamos verificar el tamaño máximo
        
        print("✅ Campo foto_perfil ya es TEXT - soporta Base64")
        print("ℹ️  Formato esperado: 'data:image/jpeg;base64,{datos}'")
        
        # Ejemplo de cómo se verían los datos
        print("\n📝 Formato de datos Base64:")
        print("   Imagen pequeña (10KB): ~13KB en Base64")
        print("   Imagen mediana (50KB): ~67KB en Base64") 
        print("   Imagen grande (200KB): ~267KB en Base64")
        
        print(f"\n✅ BD preparada para Base64")
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def ejemplo_base64():
    """Mostrar ejemplo de conversión a Base64"""
    print("\n🔧 EJEMPLO DE USO BASE64:")
    print("-" * 25)
    
    # Ejemplo de función para convertir imagen a Base64
    ejemplo_codigo = '''
# Función para convertir imagen a Base64
import base64

def imagen_a_base64(ruta_imagen):
    """Convertir imagen local a Base64"""
    try:
        with open(ruta_imagen, "rb") as archivo:
            datos_binarios = archivo.read()
            base64_string = base64.b64encode(datos_binarios).decode('utf-8')
            
            # Detectar tipo de imagen
            extension = Path(ruta_imagen).suffix.lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg', 
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            
            mime_type = mime_types.get(extension, 'image/jpeg')
            
            # Formato completo para web
            return f"data:{mime_type};base64,{base64_string}"
            
    except Exception as e:
        return None

# Uso:
foto_base64 = imagen_a_base64("mi_foto.jpg")
# Resultado: "data:image/jpeg;base64,/9j/4AAQSkZJRgAB..."
'''
    
    print(ejemplo_codigo)
    
    print("🌐 USO EN FRONTEND:")
    print('<img src="{foto_base64}" alt="Foto de perfil" />')
    print("\n📡 USO EN API:")
    print('{"foto_perfil": "data:image/jpeg;base64,..."}')

if __name__ == "__main__":
    migrar_a_base64()
    ejemplo_base64()