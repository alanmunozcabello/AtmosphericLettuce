# Avances del Proyecto

## 📌 Semana 1
- Creación del tablero Kanban con tarjetas **To Do, In Progress, Review, Testing y Done**.
- Creación del repositorio en **GitHub** con el archivo `README.md` y la carpeta **DOCS** (acta_equipo, preguntas_generales, requisitos y documentación).
- Creación de la carpeta **Wireframes**.
- Asignación de roles y planificación de la futura distribución de responsabilidades.
- Redacción de la **descripción del proyecto**.

---

## 📌 Semana 2
- Elaboración del archivo **PDF Semana 2**.

---

## 📌 Semana 3
- Creación de la carpeta **Arquitectura**.

---

## 📌 Semana 4
- Implementación de la **estructura en capas**:  
  `Routes / Controllers / Services / Data`
- Implementación de la **persistencia de datos con información real** (registro y lectura de usuarios) en:  
  `Services/usuarios_service.py`
- Implementación de un **manejo básico de errores en diferentes niveles**:  
  - **Control de calidad de los datos de un nuevo usuario** en:  
    `Controllers/usuarios_controllers.py`  
  - **Manejo de respuestas de la API y errores generales** (archivos `.json`, errores de conexión, etc.) con `try/except` en:  
    - `Services/ai_service.py`  
    - `Services/clima_service.py`  
    - `Services/planta_service.py`

## 📌 Semana 5
- Implementación de la interfaz navegable HTML y CSS (Home, Formularios, log, Perfeil)
  - `Perfil: permite modificar imformacion registrada previamente`
  - `Home: permite eliminar y agregar cultivos`
  - `Formulario: permite interactuar y verificar los datos proporcionados por el usuarios`
  - `log: Permite validar los datos del usuarios (correo valido)`
- Implementación de validación
  - `Campos obligatorios: log -> correo, nombre, contraseña, verificacion de datos en el perfil`
- Implementación de errores y campos vacíos 
  - `manejo de campos vacíos log, Perfil`
  - `home permite no repetir los cultivos ya ingresados`

## 📌 Semana 6


