# 🌱 AtmosphericLettuce — Documentación Técnica

## 📦 Configuración del Entorno

### 🧩 Requisitos Previos
- Python 3.8 o superior
- SQLite
- DB Browser para SQLite (para visualización de la base de datos)

### ⚙️ Instalación de Dependencias

El proyecto utiliza varias librerías de Python que se encuentran listadas en el archivo `requirements.txt`. Para instalarlas, ejecuta el siguiente comando en la terminal desde la carpeta raíz del proyecto:

```bash
pip install -r src/requirements.txt
```

Las principales dependencias incluyen:

- **FastAPI** y **Uvicorn**: Servidor web asíncrono
- **SQLite3**: Base de datos
- **Python-dotenv**: Manejo de variables de entorno
- **Requests**: Llamadas HTTP a APIs externas
- **Google API Client**: Integración con servicios de Google
- **Argon2**: Encriptación segura de contraseñas
- **APScheduler**: Sistema de tareas programadas
- **Anthropic/OpenAI**: APIs de IA para el chatbot

**Testing:**
- **Pytest**: Framework de pruebas
- **Pytest-asyncio**: Soporte para tests asíncronos
- **HTTPX**: Cliente HTTP para tests

### 🔐 Configuración del Archivo .env

El proyecto requiere un archivo `.env` en la carpeta `src/`. Para facilitar la configuración, se proporciona un archivo `.env.example` con la siguiente estructura:

```plaintext
# Configuración de la Base de Datos
DATABASE_PATH="data/database.db"

# Clave Secreta para JWT
SECRET_KEY="tu_clave_secreta_aqui"

# Configuración de Email
GMAIL_USERNAME="tu_correo@gmail.com"
GMAIL_PASSWORD="tu_contraseña_de_aplicacion"

# Configuración de OpenAI (para el chatbot)
OPENAI_API_KEY="tu_clave_api_de_openai"

# Configuración de APIs de Clima
WEATHER_API_KEY="tu_clave_api_del_clima"
```

Para configurar el proyecto:
1. Copia el archivo `.env.example` a `.env`
2. Reemplaza los valores de ejemplo con tus propias credenciales
3. Asegúrate de no compartir el archivo `.env` con las credenciales reales

## 🧱 Estructura del Proyecto

La carpeta `src/` contiene el código principal del proyecto. A continuación se detalla su estructura:

```
src/
├── app.py                    # Punto de entrada de la aplicación FastAPI
├── requirements.txt          # Lista de dependencias del proyecto
├── .env                     # Variables de entorno (crear desde .env.example)
├── .env.example             # Plantilla de configuración
│
├── controllers/             # Controladores de la aplicación
│   ├── __init__.py
│   ├── usuarios_controller.py          # Gestión de usuarios
│   ├── chat_controllers.py             # Lógica del chatbot
│   ├── clima_controller.py             # Control del clima
│   ├── modificadora_notificaciones.py  # Modificación de notificaciones
│   └── notificaciones_controller.py    # Control de notificaciones
│
├── routes/                  # Rutas y endpoints de la API
│   ├── __init__.py
│   ├── usuarios_routes.py   # Endpoints de usuarios
│   ├── chat_routes.py       # Endpoints del chat
│   ├── clima_routes.py      # Endpoints de clima
│   └── notificaciones_routes.py  # Endpoints de notificaciones
│
├── services/                # Servicios y lógica de negocio
│   ├── __init__.py
│   ├── usuarios_service.py          # Lógica de usuarios
│   ├── chat_service.py              # Servicio del chat
│   ├── clima_service.py             # Servicio de clima
│   ├── plant_service.py             # Servicio de plantas
│   ├── ai_services.py               # Integración con IAs (Claude/OpenAI)
│   ├── modificadora_service.py      # Modificación de datos
│   ├── notificaciones_service.py    # Envío de notificaciones
│   └── security.py                  # Autenticación y seguridad
│
├── data/                    # Archivos de datos
│   └── DataBase.db          # Base de datos SQLite (NO incluir en git)
│
├── tasks/                   # Tareas programadas (cron jobs)
│   ├── __init__.py
│   ├── enviar_correos_tasks.py   # Tareas de envío de correos
│   ├── scheduler.py              # Programador de tareas (APScheduler)
│   └── sistema_de_alertas.py     # Sistema de alertas automáticas
│
├── utils/                   # Utilidades (si existen)
│
└── static/                  # Frontend de la aplicación
    └── web/
        ├── index.html       # Página de inicio/login
        ├── landing.html     # Landing page
        ├── registro.html    # Registro de usuarios
        ├── home.html        # Dashboard principal
        ├── dias.html        # Pronóstico semanal
        ├── perfil.html      # Perfil de usuario
        ├── gestor_cultivos.html       # Gestión de cultivos
        ├── formulario_plantas.html    # Formulario de plantas
        │
        ├── css/             # Hojas de estilo
        │   ├── chat_bot.css
        │   ├── dias.css
        │   ├── formulario_plantas.css
        │   ├── gestor_cultivos.css
        │   ├── homes.css
        │   ├── landing.css
        │   ├── perfil.css
        │   ├── redireccion.css
        │   └── style.css
        │
        ├── js/              # Scripts organizados por funcionalidad
        │   ├── chatbot/
        │   │   └── chat_controller.js      # Control del chat con IA
        │   ├── clima/
        │   │   ├── cache_clima.js          # Sistema de caché de clima
        │   │   ├── clima_dias.js           # Clima semanal
        │   │   └── clima_home.js           # Clima en dashboard
        │   ├── cultivos/
        │   │   ├── crud_cultivos.js        # CRUD de cultivos
        │   │   ├── cultivos.js             # Gestión de cultivos
        │   │   ├── formulario_plantas.js   # Formulario de plantas
        │   │   └── ui_cultivos.js          # Interfaz de cultivos
        │   ├── mapa/
        │   │   ├── mapa_marcar_area.js     # Marcado de áreas
        │   │   ├── mapa_principal.js       # Mapa principal
        │   │   ├── obtener_ubicacion.js    # Geolocalización
        │   │   └── ubicacion.js            # Gestión de ubicación
        │   ├── usuario/
        │   │   ├── borrar_cuenta.js        # Eliminación de cuenta
        │   │   ├── login.js                # Autenticación
        │   │   ├── nav_correo.js           # Navegación
        │   │   ├── perfil.js               # Gestión de perfil
        │   │   └── registro.js             # Registro de usuarios
        │   └── utilidades/
        │       ├── redireccion.js          # Redirecciones
        │       └── utils.js                # Utilidades generales
        │
        ├── img/             # Recursos visuales
        │
        └── prueba_mapa/     # Tests del mapa
            └── idea.txt
```

### 📚 Descripción de Carpetas

#### Backend (Python)
- **controllers/**: Maneja la lógica de control y procesamiento de requests
- **routes/**: Define los endpoints de la API REST
- **services/**: Implementa la lógica de negocio principal
- **tasks/**: Tareas automáticas programadas (envío de correos, alertas)
- **data/**: Almacenamiento de la base de datos SQLite

#### Frontend (HTML/CSS/JavaScript)
- **static/web/**: Aplicación web completa
  - **css/**: Estilos modulares por página
  - **js/**: Scripts organizados por funcionalidad
    - `chatbot/`: Chat con IA y previews de archivos
    - `clima/`: Sistema de clima con caché
    - `cultivos/`: CRUD completo de cultivos
    - `mapa/`: Integración con OpenLayers
    - `usuario/`: Autenticación y perfil
    - `utilidades/`: Funciones compartidas
  - **img/**: Recursos visuales
  - **html**: Páginas y vistas de la aplicación


## 🚀 Iniciar el Servidor

### Desarrollo Local
Para iniciar el servidor de desarrollo, ejecuta el siguiente comando desde la carpeta `src/`:

```bash
python -m uvicorn app:app --reload
```

El servidor se iniciará en `http://localhost:8000` con recarga automática activada para desarrollo.

### Desarrollo en Red Local (LAN)
Para que otros dispositivos en tu red puedan acceder:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Accede desde otros dispositivos usando `http://TU_IP_LOCAL:8000`


## 🗃️ Base de Datos

El proyecto utiliza SQLite3 como sistema de gestión de base de datos. El archivo de la base de datos se encuentra en `src/data/database.db`. 

### Visualización de la Base de Datos
Para ver y administrar la base de datos:
1. Descarga e instala DB Browser for SQLite desde su [sitio oficial](https://sqlitebrowser.org/)
2. Abre el archivo database.db con DB Browser
3. Podrás ver todas las tablas, realizar consultas y modificar datos directamente

La base de datos contiene las siguientes tablas:
- **usuarios**: Almacena la información de los usuarios registrados
- **cultivos**: Información sobre los cultivos y plantas
- **area_cultivo**: Información geográfica de las áreas de cultivo

### Scripts de Base de Datos

En la carpeta `scripts/` encontrarás:

```bash
# Migrar base de datos
python scripts/migracion_sqlite.py
```

## 🧪 Pruebas Unitarias

El proyecto incluye un conjunto completo de pruebas unitarias usando **pytest**.

### Ejecutar Tests

```bash
# Opción 1: Usando script Python
python run_tests.py

# Opción 2: Usando pytest directo
cd src
pytest ../tests/ -v

# Con prints visibles
pytest ../tests/ -v -s

# Con coverage
pytest ../tests/ -v --cov=. --cov-report=html

# Solo tests de routes
pytest ../tests/routes/ -v

# Solo tests de controllers
pytest ../tests/controllers/ -v

# Solo tests de services
pytest ../tests/services/ -v

# Test específico
pytest ../tests/routes/test_usuarios_routes.py::test_registrar_usuario -v
```

### Estructura de Tests

```
tests/
├── routes/
│   ├── test_usuarios_routes.py
│   ├── test_chat_routes.py
│   ├── test_clima_routes.py
│   └── test_notificaciones_routes.py
├── controllers/
│   └── ...
└── services/
    └── ...
```

## 🧭 Documentación de API

La documentación detallada de todos los endpoints de la API se encuentra en el archivo `docs/Documentacion/endpoints.md`. Este documento contiene:
- Lista completa de endpoints disponibles
- Parámetros requeridos y opcionales
- Ejemplos de respuestas

## 🌤️ Características Principales

- Sistema de autenticación de usuarios
- Chat bot con IA para consultas sobre cultivos
- Sistema de notificaciones por correo electrónico
- Monitoreo del clima en tiempo real
- Gestión de cultivos
- Interfaz web interactiva
- Sistema de geolocalización para cultivos

## 🧰 Scripts de Utilidad

En la carpeta `scripts/` encontrarás varios scripts útiles para:
- Migración de la base de datos
- Actualización de tabla de cultivos
- Configuración de Gmail
- Verificación de migraciones