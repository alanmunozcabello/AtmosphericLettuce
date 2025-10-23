# AtmosphericLettuce — Documentación técnica (Backend `src`)

Esta guía explica cómo instalar, configurar, ejecutar y usar el backend construido con FastAPI. Se enfoca en la carpeta `src` y sus archivos. Incluye comandos listos para Windows PowerShell.

## Requisitos

- Python 3.11 o superior (recomendado)
- Windows PowerShell (esta guía usa comandos para PowerShell)
- Acceso a Internet para consumir APIs externas (OpenWeather, OpenRouter, CropKindwise)

Dependencias principales del proyecto:
- fastapi, uvicorn
- python-dotenv
- requests
- argon2-cffi (hash de contraseñas)
- PyMuPDF (módulo `fitz`, para leer PDF)
- reportlab PyPDF2
- --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
- Jinja2

## Instalación rápida (Windows)

1) Crear y activar entorno virtual:

```powershell
# Desde la carpeta del repositorio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

2) Instalar dependencias:

```powershell
pip install fastapi "uvicorn[standard]" python-dotenv requests argon2-cffi PyMuPDF
```

3) Crear el archivo `.env` con tus llaves (ver sección Variables de entorno). Importante: colócalo dentro de `src/` porque el código carga variables desde el directorio de ejecución.

## Variables de entorno (.env)

Crea un archivo llamado `.env` en la carpeta raiz del proyecto con el siguiente contenido y reemplaza los valores:

```
# Clave de OpenWeather (pronóstico del tiempo)
OPENWEATHER_API_KEY=tu_api_key_de_openweather

# Clave para OpenRouter (modelo Mistral). Requiere cuenta y API key.
OPENROUTER_MISTRAL_API_KEY=tu_api_key_de_openrouter

# Clave para CropKindwise (detección de enfermedades en plantas)
CROPHEALTH_API_KEY=tu_api_key_de_crop_kindwise
```


Notas:
- Si ejecutas el servidor desde `src/`, `.env` debe estar en la carpeta raiz del proyecto.
- Si cambias el directorio de trabajo, asegúrate de que `.env` esté donde se lance el proceso (o ajusta el código para cargar una ruta específica).

## Estructura de `src/`

- `app.py`: punto de entrada de FastAPI. Define CORS, monta estáticos y agrega routers.
- `controllers/`: capa intermedia que valida/transforma datos y llama a `services/`.
  - `usuarios_controller.py`, `clima_controller.py`, `chat_controllers.py`.
- `routes/`: define endpoints HTTP (APIRouter) y los vincula a controllers.
  - `usuarios_routes.py`, `clima_routes.py`, `chat_routes.py`.
- `services/`: lógica de negocio e integración con APIs/DB/seguridad.
  - `usuarios_service.py`: CRUD de usuarios sobre JSON local, login, cultivos, ubicación.
  - `clima_service.py`: consumo de OpenWeather y filtrado de respuestas.
  - `chat_service.py`: orquesta texto/imagen/pdf y consulta a IA (Mistral vía OpenRouter) y CropKindwise para imágenes.
  - `ai_services.py`: cliente de OpenRouter (Mistral) y prompt del sistema.
  - `plant_service.py`: cliente de CropKindwise y filtrado de resultados.
  - `security.py`: hashing/verificación de contraseñas con Argon2.
  - `user_db_services.py`: carga/guarda `data/usuarios.json`.
- `data/`
  - `usuarios.json`: base de datos local en formato JSON.
- `static/`
  - `web/*.html`, `web/css`, `web/js`, `web/img`: frontend estático servido bajo `/static`.

## Cómo ejecutar el servidor

El servidor está pensado para ejecutarse desde la carpeta `src/` (por la ruta de estáticos y `.env`).

```powershell
# Estando en la raíz del repo
Set-Location src
python -m uvicorn app:app --reload
```

Opcional (exponer en la red local / cambiar host/puerto):

```powershell
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

- Documentación interactiva (Swagger): http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
- Archivos estáticos (frontend): se sirven bajo `/static`. Por ejemplo:
  - http://127.0.0.1:8000/static/web/index.html
  - http://127.0.0.1:8000/static/web/home.html

Nota: en `app.py` se monta `StaticFiles(directory="static")`. Por eso, si ejecutas desde otra carpeta (no `src/`), es probable que no encuentre la carpeta `static`. Corre el servidor desde `src/` o ajusta la ruta según tu estructura.

## Endpoints principales

A continuación, un resumen de los endpoints y ejemplos con PowerShell usando `Invoke-RestMethod`.

### Salud y raíz
- `GET /` → { mensaje: "Bienvenido a la API" }
- `GET /ping` → { mensaje: "pong" }

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/ -Method Get
Invoke-RestMethod -Uri http://127.0.0.1:8000/ping -Method Get
```

### Usuarios
- `GET /usuarios` → lista completa (diccionario) de usuarios.
- `GET /usuarios/{correo}` → datos del usuario formateados para frontend.
- `GET /usuarios/iniciar_sesion/{correo}/{contrasena}` → login. Devuelve datos del usuario sin el hash.
- `POST /usuarios/registrar` → registrar nuevo usuario; body JSON:
  - { correo: string, nombre: string, contrasena: string }
- `GET /usuarios/{correo}/cultivos` → cultivos del usuario.
- `PATCH /usuarios/{correo}/{cultivo}/{hectareas}/agregar_modificar` → crea/modifica cultivo (hectáreas enteras).
- `DELETE /usuarios/{correo}/{cultivo}/eliminar` → elimina cultivo.
- `PUT /usuarios/{correo}/modificar` → reemplaza usuario (nota: función marcada para refactor en comentarios del código).
- `PATCH /usuarios/{correo}/ubicacion/{lat}/{lon}/modificar` → actualiza ubicación numérica.
- `PATCH /usuarios/{correo}/ubicacion/region/{region}/{ciudad}/modificar` → actualiza ciudad/región.

Ejemplos:

Registrar un usuario
```powershell
$body = @{ correo = "user@example.com"; nombre = "User"; contrasena = "Secreta123" } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/usuarios/registrar -Method Post -Body $body -ContentType 'application/json'
```

Obtener usuario
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/usuarios/user@example.com -Method Get
```

Agregar/modificar cultivo
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/usuarios/user@example.com/Maiz/10/agregar_modificar -Method Patch
```

Actualizar ubicación (lat/lon)
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/usuarios/user@example.com/ubicacion/-35.1/-71.2/modificar -Method Patch
```

Login
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/usuarios/iniciar_sesion/user@example.com/Secreta123 -Method Get
```
## Endpoints API externas

OpenWeatherMap
- `GET /clima/hoy/{lat}/{lon}` → estado del día actual.
- `GET /clima/semana/{lat}/{lon}` → resumen diario de 7 días.

crop.health de KindWise
- URL: https://crop.kindwise.com/api/v1/identification
- Método: POST

Google Gmail
- `POST/notificaciones/enviar_html` → se manda un archivo html en el cual aparece el clima de los dias ademas de los consejos que ofrece la ia para los cutivos, etc.

OpenLayers
- Esta es una libreria de javascript la cual lo que hace es es cargar datos de mapas desde fuentes externas.
- URL: https://cdn.jsdelivr.net/npm/ol@latest/dist/ol.js
- URL Hoja de estilos: https://cdn.jsdelivr.net/npm/ol@latest/ol.css


Nominatim
- URL: https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10&addressdetails=1
- Metodo: GET

DeepSeek
- `POST/chat/consulta` → para poder realizar la pregunta al chat bot 


### Clima (requiere `OPENWEATHER_API_KEY`)
- `GET /clima/hora/{lat}/{lon}` → pronóstico hora a hora para 4 días, agrupado por día.
- `GET /clima/hoy/{lat}/{lon}` → estado del día actual.
- `GET /clima/semana/{lat}/{lon}` → resumen diario de 7 días.

Ejemplos:
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/clima/hoy/-35.0/-71.0 -Method Get
Invoke-RestMethod -Uri http://127.0.0.1:8000/clima/hora/-35.0/-71.0 -Method Get
Invoke-RestMethod -Uri http://127.0.0.1:8000/clima/semana/-35.0/-71.0 -Method Get
```

### Chat IA
- `POST /chat/consulta` → acepta un JSON con cualquiera de las claves:
  - `texto`: string (consulta del usuario)
  - `imagen`: lista de strings Base64 (ej. fotografías de plantas)
  - `pdf`: lista de strings Base64 (documentos a analizar)

El backend:
- Para imágenes usa CropKindwise (`plant_service.py`) y resume resultados.
- Para texto y contexto (incluido texto extraído de PDF vía PyMuPDF) usa OpenRouter/Mistral (`ai_services.py`).

Ejemplo mínimo (solo texto):
```powershell
$payload = @{ texto = "¿Cómo prevenir mildiu en lechuga?" } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/chat/consulta -Method Post -Body $payload -ContentType 'application/json'
```

Ejemplo con una imagen en Base64 (esquema):
```powershell
# Supón que tienes una cadena Base64 en $img64
$payload = @{ texto = "¿Qué enfermedad es?"; imagen = @($img64) } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/chat/consulta -Method Post -Body $payload -ContentType 'application/json'
```

## Datos locales (`src/data/usuarios.json`)

- Se usa como “base de datos” simple. El servicio `user_db_services.py` carga/guarda este JSON.
- El servicio de usuarios mantiene un diccionario en memoria y escribe cambios con `guardar_db`.
- Consideraciones:
  - No es transaccional ni seguro para escrituras concurrentes.
  - Haz copias de seguridad periódicas del archivo.
  - Las contraseñas se guardan hasheadas con Argon2 (ver `security.py`).

## Archivos estáticos (frontend)

- Bajo `src/static/web/` hay páginas como `index.html`, `home.html`, `perfil.html`, etc.
- Se sirven en `/static/web/...`. Por ejemplo:
  - http://127.0.0.1:8000/static/web/index.html

Si cambias la estructura de carpetas, ajusta en `app.py`:
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

## Migracion a SQL lite
- Ahora los datos en vez de estar guardados en un archivo .json se encuentra dentro de SQL lite
- Se actualizo `usuarios_services.py` para que ahora funcione en base a SQL lite
Las herramientas utilizadas son:
- SQLite como motor de base de datos embebido.
- DB Browser for SQLite para la inspección y validación de la base de datos.
- Enlace de descarga: https://sqlitebrowser.org/

Los resultados obtenidos son:
- Una base de datos funcional y portable archivo(.db).
- Confirmación de la persistencia de datos tras reiniciar la aplicación.
- Adaptación del código de conexión y consultas SQL al nuevo entorno.

 Pruebas realizadas:
- Agregar, Edicion y eliminación de registros en tablas principales.
- Visualización de los datos en DB Browser para verificar consistencia.

## Configuración y notas

- CORS: está abierto a `*` para pruebas locales en `app.py`. En producción restringe `allow_origins`.
- Directorio de trabajo: ejecuta desde `src/` para que `static/` y `.env` se resuelvan correctamente.
- Cambiar puerto/host: usa flags de `uvicorn` (`--host`, `--port`).
- Logs/Errores: revisa la consola donde corre Uvicorn.

## Problemas comunes y soluciones

- «No se encuentran archivos estáticos»: ejecuta desde `src/` o ajusta `StaticFiles(directory=...)` a la ruta correcta.
- 401/403 en APIs externas: revisa tus API keys en `.env`. Verifica que no tengan espacios extras.
- Error instalando PyMuPDF o argon2-cffi en Windows:
  - Actualiza pip: `python -m pip install --upgrade pip`.
  - En la mayoría de los casos hay wheel precompilado y se instala sin compilación.
  - Si hubiera errores de compilación, instala Microsoft C++ Build Tools y vuelve a intentar.

## Apéndice: contratos breves por servicio

- `usuarios_service`:
  - Entrada típica: correo (clave), nombres de cultivo, hectáreas (int), lat/lon (float), región/ciudad (str).
  - Salidas: objetos JSON; en login/consulta de usuario se omite el campo `contrasena`.
  - Errores: {"error": <mensaje>} para archivo no encontrado, JSON corrupto, usuario inexistente, duplicados.
- `clima_service`:
  - Requiere `OPENWEATHER_API_KEY` válido.
  - Devuelve estructuras ya filtradas y listas para frontend.
- `chat_service`/`ai_services`/`plant_service`:
  - Requieren `OPENROUTER_MISTRAL_API_KEY` y/o `CROPHEALTH_API_KEY`.
  - PDF: se extrae texto con PyMuPDF; imágenes: se mandan en Base64.

---


