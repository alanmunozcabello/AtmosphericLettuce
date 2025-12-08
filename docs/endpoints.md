# 🌾 Endpoints de Usuarios y APIs Externas

## 📘 Endpoints Básicos

### 🏠 Página Inicial
- **URL**: `/`
- **Método**: GET
- **Descripción**: Landing page

### 🔄 Test de Conexión
- **URL**: `/ping`
- **Método**: GET
- **Descripción**: Test simple de conectividad
- **Respuesta**: `{"mensaje": "pong"}`

## 🔐 Autenticación

### 🔑 Validar Token
- **URL**: `/api/validar-token`
- **Método**: GET
- **Descripción**: Valida si un token JWT es válido
- **Headers**:
  - `Authorization`: `Bearer <token>`
- **Respuesta**:
  ```json
  {
    "valido": true,
    "correo": "usuario@ejemplo.com"
  }
  ```

## 👤 Gestión de Usuarios

### 📋 Obtener Todos los Usuarios
- **URL**: `/usuarios`
- **Método**: GET
- **Descripción**: Obtiene la lista de todos los usuarios registrados

### 🔍 Obtener Usuario Específico
- **URL**: `/usuarios/{correo}`
- **Método**: GET
- **Descripción**: Obtiene la información de un usuario específico
- **Parámetros**:
  - `correo`: Email del usuario

### 🔓 Iniciar Sesión (GET - Actualmente utilizado)
- **URL**: `/usuarios/iniciar_sesion/{correo}/{contrasena}`
- **Método**: GET
- **Descripción**: Valida las credenciales de inicio de sesión
- **Parámetros**:
  - `correo`: Email del usuario
  - `contrasena`: Contraseña del usuario

### 🔐 Iniciar Sesión (POST - Recomendado)
- **URL**: `/usuarios/login`
- **Método**: POST
- **Descripción**: Valida las credenciales de inicio de sesión de forma segura
- **Body**:
  ```json
  {
    "correo": "usuario@ejemplo.com",
    "contrasena": "string"
  }
  ```

### 🧾 Registrar Usuario
- **URL**: `/usuarios/registrar`
- **Método**: POST
- **Descripción**: Registra un nuevo usuario
- **Body**:
  ```json
  {
    "correo": "string",
    "nombre": "string",
    "contrasena": "string"
  }
  ```

### ✏️ Modificar Usuario
- **URL**: `/usuarios/{correo}/modificar`
- **Método**: PUT
- **Descripción**: Modifica los datos de un usuario
- **Parámetros**:
  - `correo`: Email del usuario
- **Body**:
  ```json
  {
    "nombre": "string",
    "ciudad": "string",
    "region": "string",
    "foto_perfil": "string"
  }
  ```

### 🔔 Modificar Preferencias de Notificaciones
- **URL**: `/usuarios/{correo}/modificar_notificaciones/{notificaciones}`
- **Método**: PATCH
- **Descripción**: Activa o desactiva las notificaciones por correo
- **Parámetros**:
  - `correo`: Email del usuario
  - `notificaciones`: Booleano (`true` o `false`)

### 🗑️ Eliminar Usuario
- **URL**: `/usuarios/{correo}`
- **Método**: DELETE
- **Descripción**: Elimina un usuario
- **Parámetros**:
  - `correo`: Email del usuario

## 🔄 Recuperación de Contraseña

### 📧 Solicitar Código
- **URL**: `/api/recuperacion/solicitar`
- **Método**: POST
- **Descripción**: Envía un código de recuperación al correo del usuario
- **Body**:
  ```json
  {
    "correo": "usuario@ejemplo.com"
  }
  ```

### ✅ Verificar Código
- **URL**: `/api/recuperacion/verificar`
- **Método**: POST
- **Descripción**: Verifica si el código ingresado es válido
- **Body**:
  ```json
  {
    "correo": "usuario@ejemplo.com",
    "codigo": "123456"
  }
  ```

### 🔑 Cambiar Contraseña
- **URL**: `/api/recuperacion/cambiar`
- **Método**: POST
- **Descripción**: Cambia la contraseña del usuario usando un código válido
- **Body**:
  ```json
  {
    "correo": "usuario@ejemplo.com",
    "codigo": "123456",
    "nueva_contrasena": "NuevaPassword123!"
  }
  ```

## 📍 Gestión de Ubicación

### 📡 Modificar Ubicación (Latitud / Longitud)
- **URL**: `/usuarios/{correo}/ubicacion/{lat}/{lon}/modificar`
- **Método**: PATCH
- **Descripción**: Actualiza las coordenadas de ubicación del usuario
- **Parámetros**:
  - `correo`: Email del usuario
  - `lat`: Latitud
  - `lon`: Longitud

### 🌎 Modificar Región y Ciudad
- **URL**: `/usuarios/{correo}/ubicacion/region/{region}/{ciudad}/modificar`
- **Método**: PATCH
- **Descripción**: Actualiza la región y ciudad del usuario
- **Parámetros**:
  - `correo`: Email del usuario
  - `region`: Nombre de la región
  - `ciudad`: Nombre de la ciudad

## 🌱 Gestión de Cultivos

### 🌾 Obtener Cultivos del Usuario
- **URL**: `/usuarios/{correo}/cultivos`
- **Método**: GET
- **Descripción**: Obtiene los cultivos de un usuario con paginación
- **Parámetros**:
  - `correo`: Email del usuario
  - `pagina`: Número de página (Opcional, default: 1)
  - `limite`: Cantidad por página (Opcional, default: 20)

### 🔍 Filtrar Cultivos
- **URL**: `/cultivos/filtrar`
- **Método**: GET
- **Descripción**: Busca y filtra cultivos con múltiples criterios
- **Parámetros (Query Params)**:
  - `correo`: Email del usuario (Opcional)
  - `buscar`: Texto a buscar en nombre del cultivo (Opcional)
  - `etapa_planta`: Etapa de crecimiento (Opcional)
  - `fecha_siembra_desde`: Fecha inicio (YYYY-MM-DD)
  - `fecha_siembra_hasta`: Fecha fin (YYYY-MM-DD)
  - `estado_planta`: Estado de salud
  - `tipo_riego`: Tipo de riego
  - `tiene_area`: Booleano
  - `ordenar_por`: Campo para ordenar (default: nombre_cultivo)
  - `orden`: ASC o DESC
  - `pagina`: Número de página
  - `limite`: Resultados por página

### ➕ Agregar Cultivo
- **URL**: `/usuarios/{correo}/agregar_cultivo`
- **Método**: POST
- **Descripción**: Agrega un nuevo cultivo al usuario
- **Parámetros**:
  - `correo`: Email del usuario
- **Body**:
  ```json
  {
    "nombre_cultivo": "string",
    "hectareas": 0
  }
  ```

### 🧾 Modificar Formulario de Cultivo
- **URL**: `/usuarios/{correo}/cultivos/modificar_formulario_cultivo`
- **Método**: PATCH
- **Descripción**: Modifica los datos del formulario de un cultivo
- **Parámetros**:
  - `correo`: Email del usuario
- **Body**:
  ```json
  {
    "nombre_cultivo": "string",
    "hectareas": 0,
    "fecha_siembra": "string",
    "notas": "string",
    "etapa_planta": "string",
    "tipo_riego": "string",
    "ultimo_riego": "string",
    "frecuencia_riego": "string",
    "humedad_suelo": "string",
    "textura_suelo": "string",
    "variedad_planta": "string",
    "estado_planta": "string",
    "estres_hidrico": 0,
    "profundidad_radical": 0,
    "densidad_plantacion": 0,
    "tipo_sensor": "string",
    "eficiencia_riego": 0,
    "caudal": 0,
    "ph_agua": 0,
    "acolchado": 0
  }
  ```

### 📏 Modificar Área de Cultivo
- **URL**: `/usuarios/{correo}/cultivo/modificar_area_cultivo`
- **Método**: PATCH
- **Descripción**: Modifica el área y coordenadas de un cultivo
- **Parámetros**:
  - `correo`: Email del usuario
- **Body**:
  ```json
  {
    "cultivo": "string",
    "area": 0,
    "puntos": [
      {
        "latitud": 0,
        "longitud": 0
      }
    ]
  }
  ```

### ❌ Eliminar Cultivo
- **URL**: `/usuarios/{correo}/{cultivo}/eliminar`
- **Método**: DELETE
- **Descripción**: Elimina un cultivo específico del usuario
- **Parámetros**:
  - `correo`: Email del usuario
  - `cultivo`: Nombre del cultivo

## 🤖 Endpoints de Chat (API Externa)

### 💬 Realizar Consulta al Chat
- **URL**: `/chat/consulta`
- **Método**: POST
- **Descripción**: Realiza una consulta al chatbot
- **Body**:
  ```json
  {
    "payload": "object"
  }
  ```
- **Respuesta**: Retorna un objeto con la respuesta del chatbot

## ☀️ Endpoints de Clima (API Externa)

### 🕐 Clima por Hora
- **URL**: `/clima/hora/{lat}/{lon}`
- **Método**: GET
- **Descripción**: Obtiene el pronóstico del clima por hora
- **Parámetros**:
  - `lat`: Latitud de la ubicación
  - `lon`: Longitud de la ubicación

### 🌤️ Clima del Día
- **URL**: `/clima/hoy/{lat}/{lon}`
- **Método**: GET
- **Descripción**: Obtiene el pronóstico del clima para el día actual
- **Parámetros**:
  - `lat`: Latitud de la ubicación
  - `lon`: Longitud de la ubicación

### 📅 Clima de la Semana
- **URL**: `/clima/semana/{lat}/{lon}`
- **Método**: GET
- **Descripción**: Obtiene el pronóstico del clima para la semana
- **Parámetros**:
  - `lat`: Latitud de la ubicación
  - `lon`: Longitud de la ubicación

## 📧 Endpoints de Notificaciones (API Externa)

### 🔍 Verificar Conexión con Gmail
- **URL**: `/notificaciones/verificar_gmail`
- **Método**: GET
- **Descripción**: Verifica que la conexión con la API de Gmail funciona correctamente

### ✉️ Enviar HTML
- **URL**: `/notificaciones/enviar_html`
- **Método**: POST
- **Descripción**: Envía un correo electrónico en formato HTML
- **Parámetros**:
  - `correo`: Email del destinatario

### 🔢 Enviar Código de Verificación
- **URL**: `/notificaciones/enviar_codigo`
- **Método**: POST
- **Descripción**: Envía un código de verificación por correo electrónico
- **Parámetros**:
  - `correo`: Email del destinatario
