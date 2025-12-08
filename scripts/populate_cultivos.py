import requests
import sys

# Configuración
BASE_URL = "http://localhost:8000"
CORREO = "diego@pjd.cl"

def populate():
    print(f"🚀 Iniciando carga masiva de cultivos para: {CORREO}")
    print(f"🎯 Objetivo: 100 cultivos (A, AA, AAA, ...)")

    # Verificar que el servidor esté arriba
    try:
        requests.get(f"{BASE_URL}/ping")
    except requests.exceptions.ConnectionError:
        print("❌ Error: El servidor no parece estar corriendo en http://localhost:8000")
        print("Ejecuta 'python -m uvicorn app:app' en otra terminal.")
        return

    exitos = 0
    errores = 0

    for i in range(1, 101):
        nombre = "A" * i
        
        payload = {
            "nombre_cultivo": nombre,
            "hectareas": 5
        }
        
        try:
            url = f"{BASE_URL}/usuarios/{CORREO}/agregar_cultivo"
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    print(f"⚠️ [{i}/100] Rechazado por API: {data['error']} (Nombre: {nombre[:10]}...)")
                    errores += 1
                else:
                    print(f"✅ [{i}/100] Creado: {len(nombre)} chars")
                    exitos += 1
            else:
                print(f"❌ [{i}/100] Error HTTP {response.status_code}: {response.text}")
                errores += 1
                
        except Exception as e:
            print(f"💥 Error crítico: {e}")
            break
            
    print("-" * 30)
    print(f"🏁 Finalizado. Éxitos: {exitos}, Errores: {errores}")

if __name__ == "__main__":
    populate()
