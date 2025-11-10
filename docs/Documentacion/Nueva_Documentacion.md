# 🌿 AtmosphericLettuce — Documentación Técnica

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
- FastAPI y Uvicorn para el servidor web
- SQLite para la base de datos
- Python-dotenv para variables de entorno
- Requests para llamadas HTTP
- Google API Client para servicios de Google
- Argon2 para encriptación de contraseñas
- Apscheduler para el automata
- Pytest pytest-asyncio httpx para las pruebas unitarias

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
├── app.py              # Punto de entrada de la aplicación FastAPI
├── requirements.txt    # Lista de dependencias del proyecto
├── .env               # Variables de entorno (crear desde .env.example)
│
├── controllers/        # Controladores de la aplicación
│   ├── usuarios_controller.py     # Gestión de usuarios
│   ├── chat_controllers.py        # Lógica del chatbot
│   ├── clima_controller.py        # Control del clima
│   ├── modificadora_notificaciones.py
│   └── notificaciones_controller.py
│
├── routes/            # Rutas y endpoints de la API
│   ├── usuarios_routes.py
│   ├── chat_routes.py
│   ├── clima_routes.py
│   └── notificaciones_routes.py
│
├── services/          # Servicios y lógica de negocio
│   ├── usuarios_service.py
│   ├── chat_service.py
│   ├── clima_service.py
│   ├── plant_service.py
│   ├── ai_services.py
│   ├── modificadora_service.py
│   ├── notificaciones_service.py
│   └── security.py
│
├── data/             # Archivos de datos
│   └── database.db   # Base de datos SQLite
│
├── tasks/            # Tareas programadas
│   ├── enviar_correos_tasks.py   # Tareas de envío de correos
│   └── scheduler.py              # Programador de tareas
│
└── static/           # Frontend
    └── web/
        ├── css/      # Hojas de estilo
        ├── js/       # Scripts organizados por funcionalidad
        │   ├── chatbot/
        │   ├── clima/
        │   ├── cultivos/
        │   ├── mapa/
        │   ├── usuario/
        │   └── utilidades/
        ├── img/      # Recursos visuales
        └── *.html    # Páginas de la aplicación
```

### 📚 Descripción de Carpetas

#### Backend
- **controllers/**: Maneja la lógica de control y procesamiento de datos
- **routes/**: Define los endpoints de la API REST
- **services/**: Implementa la lógica de negocio principal

#### Frontend
- **static/web/**: Interfaz de usuario completa
  - **css/**: Estilos de la aplicación
  - **js/**: Scripts organizados por módulos
  - **img/**: Recursos visuales
  - **html**: Páginas y vistas

## 🚀 Iniciar el Servidor

Para iniciar el servidor de desarrollo, ejecuta el siguiente comando desde la carpeta `src/`:

```bash
python -m uvicorn app:app --reload
```

El servidor se iniciará en `http://localhost:8000` con recarga automática activada para desarrollo.

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