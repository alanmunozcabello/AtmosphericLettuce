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
- Imprementacion del sistema de notificaciones
  - `Se creo en la rama main un sistema de notificaciones que enviara archivos pdf con un infrome detallado de la informacion que este disponible para el usuario y otro donde se enviara cada cierto tiempo un html al correo del usuario con el clima de la semana y otros datos relevantes que le puedan servir al usuario`

- Implementaciones Backend   
  - `El nuevo formato permite un acceso más rápido a la información, ya que para obtener un usuario no es necesario recorrer todo el arreglo; ahora la búsqueda se realiza directamente por la clave correspondiente al correo o ID del usuario, optimizando la velocidad de los procesos.`
  - `Al tratarse de una base de datos en formato JSON, esta se carga en tiempo de ejecución. Aunque esto no es adecuado para bases de datos con miles de usuarios, resulta suficiente para nuestro caso.`
  - `La implementación se ha diseñado de manera que, al migrar a SQLite, solo será necesario modificar unas pocas funciones en el backend, mientras que el resto del código permanecerá prácticamente igual. Las partes donde se realiza un cambio directo en el JSON cargado deberán reemplazarse por llamadas a funciones con instrucciones SQL.`
  - `Se han añadido nuevos comentarios que describen la nueva implementación, así como comentarios adicionales que indican cómo se realizaría la migración a SQLite.`
  - `Se implementaron nuevos campos de informacion en los usuarios ciudad y ubicacion y metodos con los que se puede modificar estos parametros`
  - `Se modificaron los métodos HTTP de las rutas (.post .get .delete .patch .put) para que la informacion se manejara mejor y mas segura `
  - `Cambios estéticos en el chatbot, incluyendo mejoras en el feedback hacia el usuario al momento de seleccionar archivos.` 
  - `Mejoras en la selección de archivos: anteriormente, al seleccionar archivos nuevos, se eliminaban los ya seleccionados; ahora, los archivos se añaden a la lista existente, y los no deseados pueden eliminarse mediante un botón “X”.` 
  - `La burbuja del chat ahora es completamente responsiva, adaptándose a distintos tamaños de pantalla.`
  - `Se implemento el archvio security que contiene dos funciones una permite resivir una contraseña y devolverla hasheada con Argon2 y la otra permite verificar si la contraseña es igual a la hasheada que esta en la base de datos`

- Implementacion rama Frontend   
    **Integración entre el backend y el frontend**
  - `Los usuarios que se registren ahora se guardan en el archivo JSON a través de la ruta registrar usuario.`
  - `El login se conectó a la ruta iniciar sesión, permitiendo que únicamente los usuarios registrados en nuestra base de datos puedan acceder a la página.`
  - `En la pantalla Home, dentro de la sección de cultivos, se implementó la funcionalidad de agregar y eliminar cultivos, los cuales se cargan también en la base de datos (JSON).`
  - `En la sección Perfil, se muestran los datos del usuario que haya iniciado sesión, incluyendo nombre, correo, ciudad y región.`
  - `Todos estos cambios se realizaron utilizando fetch, reemplazando el uso anterior de localStorage, lo que mejora la comunicación con la base de datos y la persistencia de la información.`
  