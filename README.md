# 🌱 AtmosphericLettuce – Proyecto de Programación  

## 📌 Información General  

**Equipo:** *Lechuga* 🥬  
**Integrantes:**  
- 👨‍💻 John Rojas - Líder Técnico
- 🛠️ Nicolas Urbina - Backend
- 🎨 Cristian Aliaga - Frontend
- 📑 Alan Muñoz - QA & Documentación

**Universidad de Talca – Proyecto de Programación 2025**  

---

## 📝 Descripción del Proyecto  

**AtmosphericLettuce** es una plataforma web enfocada en la **meteorología aplicada a la agricultura** 🌦️🌾.  
Nuestro objetivo es entregar a agricultores y usuarios en general información climática **precisa y personalizada**, acompañada de **recomendaciones inteligentes basadas en IA** y herramientas de apoyo en el cuidado de cultivos.  

---

## 🚀 Funcionalidades Principales  

### Autenticación y Usuarios
- 🔐 **Sistema de autenticación JWT** con tokens de acceso
- 👤 **Gestión de perfiles** con información personal (foto, nombre, ubicación, preferencias)
- 🔑 **Recuperación de contraseña** mediante códigos de verificación por email
- 📧 **Notificaciones por Gmail** para alertas y recordatorios

### Gestión de Cultivos
- 🌱 **CRUD completo de cultivos** con información detallada
- 📍 **Áreas de cultivo georeferenciadas** con coordenadas GPS
- 📊 **Formularios extensivos** (fecha siembra, tipo riego, etapa, humedad suelo, etc.)
- 🔍 **Filtrado y búsqueda avanzada** de cultivos con paginación

### Información Climática
- ☀️ **Clima del día y semana** mediante integración con APIs externas
- 🌡️ **Datos detallados**: temperatura, humedad, viento, descripción
- 📌 **Clima por coordenadas GPS** para ubicaciones específicas

### Inteligencia Artificial
- 🤖 **Chatbot conversacional** integrado con DeepSeek AI
- 📷 **Procesamiento de imágenes** para análisis de cultivos
- 💡 **Consejos agrícolas personalizados** basados en clima y cultivos
- 📄 **Análisis de documentos** para contexto enriquecido

### Notificaciones y Alertas
- 🔔 **Sistema de alertas programadas** con APScheduler
- 📨 **Dashboards HTML enviados por email** con información del cultivo
- ⚠️ **Alertas meteorológicas** para condiciones adversas
- 📬 **Verificación de estado de notificaciones**

---

## 🛠️ Stack Tecnológico

### Backend
- **Framework:** FastAPI (Python 3.13.1)
- **Base de datos:** SQLite
- **Autenticación:** JWT (PyJWT)
- **Validación:** Pydantic
- **Testing:** pytest (59 tests unitarios)
- **Scheduler:** APScheduler
- **Email:** Gmail API

### Frontend
- **HTML5, CSS3, JavaScript**
- **Diseño responsive** con grid y flexbox
- **Integración con APIs** mediante fetch

### APIs Externas
- **DeepSeek AI:** Procesamiento de lenguaje natural
- **OpenWeatherMap:** Datos meteorológicos
- **Crop.health:** Identificación de enfermedades
- **Gmail API:** Envío de notificaciones

---

## 📦 Instalación y Configuración

### Inicio Rápido

```bash
# 1. Clonar el repositorio
git clone https://github.com/alanmunozcabello/AtmosphericLettuce.git
cd AtmosphericLettuce

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r src/requirements.txt

# 4. Configurar base de datos
python scripts/migracion_sqlite.py

# 5. Configurar gmail
python scripts/setup_gmail.py

# 6. Iniciar servidor
cd src
uvicorn app:app --reload
```

La aplicación estará disponible en `http://localhost:8000`

### 📖 Guía Completa de Instalación

Para instrucciones detalladas sobre:
- Configuración de variables de entorno (API Keys)
- Setup de Gmail para notificaciones
- Solución de problemas comunes
- Configuración de base de datos

**👉 Consulta la [Guía de Instalación Completa](docs/instalacion.md)**

---

## 🧪 Testing

El proyecto cuenta con **59 tests unitarios** que cubren todas las rutas principales:

### Ejecutar tests
```bash
cd src
python -m pytest ../tests/routes/ --tb=short -v
```

### Ejecutar con cobertura
```bash
python -m pytest ../tests/routes/ --cov=. --cov-report=html
```

### Distribución de tests
- ✅ `test_auth_routes.py`: 5 tests (validación JWT)
- ✅ `test_chat_routes.py`: 6 tests (chatbot con IA)
- ✅ `test_clima_routes.py`: 11 tests (servicios climáticos)
- ✅ `test_notificaciones_routes.py`: 7 tests (Gmail y notificaciones)
- ✅ `test_recuperacion_routes.py`: 10 tests (recuperación de contraseña)
- ✅ `test_usuarios_routes.py`: 20 tests (CRUD usuarios y cultivos)

---

## 📁 Estructura del Proyecto

```
AtmosphericLettuce/
├── src/
│   ├── app.py                 # Aplicación principal FastAPI
│   ├── requirements.txt       # Dependencias Python
│   ├── models/               # Modelos Pydantic
│   │   ├── usuario.py
│   │   ├── cultivo.py
│   │   ├── clima.py
│   │   ├── chat.py
│   │   └── recuperacion.py
│   ├── routes/               # Endpoints de la API
│   │   ├── auth_routes.py
│   │   ├── usuarios_routes.py
│   │   ├── clima_routes.py
│   │   ├── chat_routes.py
│   │   ├── notificaciones_routes.py
│   │   └── recuperacion_routes.py
│   ├── services/             # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── cultivo_service.py
│   │   ├── clima_service.py
│   │   ├── ai_integration_service.py
│   │   └── notification_service.py
│   ├── middleware/           # Autenticación y permisos
│   │   ├── autenticacion_mw.py
│   │   └── permisos_mw.py
│   ├── tasks/                # Tareas programadas
│   │   ├── scheduler.py
│   │   ├── enviar_correos_tasks.py
│   │   └── sistema_de_alertas.py
│   └── static/               # Archivos frontend
│       └── web/
│           ├── *.html
│           ├── css/
│           ├── js/
│           └── img/
├── tests/                    # Suite de testing
│   ├── conftest.py          # Configuración pytest
│   └── routes/              # Tests de endpoints
├── scripts/                  # Scripts de utilidad
│   ├── populate_cultivos.py
│   ├── migracion_sqlite.py
│   └── setup_gmail.py
└── docs/                     # Documentación
    ├── endpoints.md
    ├── instalacion.md
    └── Arquitectura/
```

---

## 🎯 Objetivo Académico  

Este proyecto es desarrollado con fines académicos dentro del **Ramo de Proyecto de Programación – Universidad de Talca (2025)**.  
Más allá de mostrar el clima, busca ser una **herramienta innovadora para la agricultura**, integrando tecnología de **IA y visión por computadora** al servicio de la toma de decisiones en el campo.  

---