# 🌾 Endpoints de Usuarios y APIs Externas

## 📘 Endpoints Básicos

### 🏠 Página Inicial
- **URL**: `/`
- **Método**: GET
- **Descripción**: Retorna un mensaje de bienvenida a la API
- **Respuesta**: `{"mensaje": "Bienvenido a la API"}`

### 🔄 Test de Conexión
- **URL**: `/ping`
- **Método**: GET
- **Descripción**: Test simple de conectividad
- **Respuesta**: `{"mensaje": "pong"}`

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

### 🔐 Iniciar Sesión
- **URL**: `/usuarios/iniciar_sesion/{correo}/{contrasena}`
- **Método**: GET
- **Descripción**: Valida las credenciales de inicio de sesión
- **Parámetros**:
  - `correo`: Email del usuario
  - `contrasena`: Contraseña del usuario

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

### 🗑️ Eliminar Usuario
- **URL**: `/usuarios/{correo}`
- **Método**: DELETE
- **Descripción**: Elimina un usuario
- **Parámetros**:
  - `correo`: Email del usuario

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
- **Descripción**: Obtiene todos los cultivos de un usuario
- **Parámetros**:
  - `correo`: Email del usuario

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



