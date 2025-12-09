# Guía de Instalación Local - AtmosphericLettuce

Este documento detalla los pasos necesarios para configurar y ejecutar el proyecto **AtmosphericLettuce** en un entorno local.

## 📋 Prerrequisitos

Asegúrate de tener instalado lo siguiente antes de comenzar:

- **Python 3.10** o superior.
- **Git** (para clonar el repositorio).
- **SQLite** (generalmente incluido con Python).

## 🚀 Pasos de Instalación

### 1. Clonar el Repositorio

Abre tu terminal y clona el proyecto:

```bash
git clone <URL_DEL_REPOSITORIO>
cd AtmosphericLettuce
```

### 2. Configurar Entorno Virtual (Recomendado)

Es altamente recomendable usar un entorno virtual para aislar las dependencias del proyecto.

**En Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**En Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r src/requirements.txt
```
**Configuración de PIP en el PATH**
Si el comando `pip` no es reconocido directamente, puede deberse a que la carpeta `Scripts` de tu instalación de Python no está en las variables de entorno (PATH) del sistema.
1. Localiza la carpeta donde se instaló Python (ej. `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python314`).
2. Busca la subcarpeta `Scripts` dentro de ella (ej. `...\Python314\Scripts`). Aquí es donde se encuentra el ejecutable `pip.exe`.
3. Copia la ruta completa de esa carpeta `Scripts`.
4. En Windows, busca "Editar las variables de entorno del sistema", ve a "Variables de entorno", busca la variable `Path` en "Variables de usuario" o "Variables del sistema", selecciona "Editar" y agrega una "Nueva" entrada pegando la ruta copiada.
5. Reinicia tu terminal. Ahora podrás usar `pip install` directamente sin necesitar `python -m pip`.


### 4. Configurar Variables de Entorno

El proyecto requiere ciertas credenciales para conectar con servicios externos (Clima, IA, Correo). Crea un archivo llamado `.env` en la raíz del proyecto (al mismo nivel que `src/`) y usa el archivo `.env.example` como plantilla.

### 5. Configurar Base de Datos

El sistema utiliza SQLite. Sigue estos pasos para inicializar la base de datos con la estructura correcta:

1.  **Ejecutar script de migración:**
    Este script crea las tablas necesarias (`usuarios`, `cultivos`, etc.) con la estructura más reciente.

    ```bash
    python scripts/migracion_sqlite.py
    ```

    *El script generará un archivo llamado `usuarios_nueva.db` dentro de `src/data/`.*

2.  **Activar la Base de Datos:**
    Para que la aplicación use esta nueva base de datos:
    - Ve a la carpeta `src/data/`.
    - Renombra el archivo `usuarios_nueva.db` a `DataBase.db`.
    - *(Si ya tenías una `DataBase.db` y quieres conservarla, haz una copia de seguridad antes).*

### 6. Ejecutar el Servidor

Una vez configurado todo, inicia el servidor de desarrollo `uvicorn`. Asegúrate de estar dentro de la carpeta `src`:

```bash
cd src
python -m uvicorn app:app --reload
```

Verás una salida indicando que el servidor está corriendo, generalmente en `http://127.0.0.1:8000`.

## ✅ Verificación

Para confirmar que la instalación fue exitosa:

1.  **Backend Docs:** Navega a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver la documentación interactiva de la API.
2.  **Frontend:** Accede a la aplicación web ingresando a [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## 🛠️ Solución de Problemas

- **ModuleNotFoundError:** Si obtienes errores de importación, asegúrate de:
    1. Tener activado el entorno virtual (`venv`).
    2. Haber ejecutado el comando de instalación de `requirements.txt`.
    3. Estar ejecutando `python -m uvicorn` desde la carpeta `src`.

- **Errores de Base de Datos:** Si la aplicación falla al leer datos, verifica que `src/data/DataBase.db` existe. Si no, repite el paso 5.
