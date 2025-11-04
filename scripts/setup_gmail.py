"""
🔐 Script para configurar Gmail API - AtmosphericLettuce
Ejecuta este script una sola vez para obtener los tokens de acceso.
"""

import sys
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("❌ ERROR: Falta instalar las librerías de Google")
    print("\n📦 Ejecuta este comando:")
    print("   pip install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Ruta al archivo de credenciales descargado (nueva versión)
CREDENTIALS_FILE = Path.home() / "Downloads" / "client_secret_2_157306603315-dpegd30un454t8h04aodjk93erlgrt7b.apps.googleusercontent.com.json"

def actualizar_env(key, value):
    """Actualiza una variable en el archivo .env"""
    env_path = Path(__file__).parent.parent / '.env'
    
    lines = []
    encontrado = False
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    # Buscar y actualizar
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f'{key}="{value}"\n'
            encontrado = True
            break
    
    # Agregar si no existe
    if not encontrado:
        lines.append(f'{key}="{value}"\n')
    
    # Guardar
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    print("=" * 70)
    print("🔐 CONFIGURACIÓN DE GMAIL API - AtmosphericLettuce")
    print("=" * 70)
    print()
    
    # Verificar que existe el archivo de credenciales
    if not CREDENTIALS_FILE.exists():
        print(f"❌ ERROR: No se encontró el archivo de credenciales")
        print(f"   Buscado en: {CREDENTIALS_FILE}")
        print()
        print("💡 SOLUCIÓN:")
        print("   1. Descarga el archivo JSON de Google Cloud Console")
        print("   2. Guárdalo en tu carpeta de Descargas")
        print("   3. Vuelve a ejecutar este script")
        return False
    
    print(f"✅ Archivo de credenciales encontrado: {CREDENTIALS_FILE.name}")
    print()
    print("🌐 Iniciando autenticación...")
    print()
    print("📌 INSTRUCCIONES:")
    print("   1. Se abrirá tu navegador automáticamente")
    print("   2. Inicia sesión con tu cuenta de Gmail")
    print("   3. Acepta los permisos solicitados")
    print("   4. Espera a que se complete el proceso")
    print()
    input("Presiona ENTER para continuar...")
    print()
    
    try:
        # Crear flow desde el archivo de credenciales
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE),
            SCOPES
        )
        
        # Ejecutar flujo de autenticación
        creds = flow.run_local_server(
            port=0,
            access_type='offline',
            prompt='consent'
        )
        
        # Guardar tokens en .env
        print("💾 Guardando tokens en .env...")
        actualizar_env("GMAIL_ACCESS_TOKEN", creds.token)
        actualizar_env("GMAIL_REFRESH_TOKEN", creds.refresh_token)
        
        if creds.expiry:
            actualizar_env("GMAIL_EXPIRY", creds.expiry.isoformat())
        
        print()
        print("=" * 70)
        print("✅ ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
        print("=" * 70)
        print()
        print("📋 Tokens guardados:")
        print(f"   ✓ Access Token: {creds.token[:50]}...")
        print(f"   ✓ Refresh Token: {creds.refresh_token[:50]}...")
        if creds.expiry:
            print(f"   ✓ Expira: {creds.expiry}")
        print()
        print("🎉 Ya puedes usar las notificaciones por correo en tu aplicación")
        print("🔄 Reinicia tu servidor FastAPI para aplicar los cambios")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR EN LA AUTENTICACIÓN")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        print("💡 POSIBLES SOLUCIONES:")
        print("   1. Verifica que Gmail API esté habilitada en Google Cloud Console")
        print("   2. Asegúrate de usar la cuenta de Gmail correcta")
        print("   3. Revisa que las credenciales sean las más recientes")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
