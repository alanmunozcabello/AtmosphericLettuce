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

## 📌 Semana 7
- Corregion de errores y termino de tareas pendientes 
  - `Se implemto la opcion de eliminar usuario (Backend/ frontend) utilizando los metodos del backend y fetch en el frontend`
  - `Se implemento la opcion de cerrar sesión con persistencia de datos `
  - `Se implmento la opcion de modficar datos del usuario (todos los datos menos el correo) con persistencia de datos`
  - `Se implemento la opcion de verificar si un cultivo ya esta ingresado en la base de datos y no permite agregarlo denuevo`
  - `Se implemento la opcion validaciones en la contraseña al momento de registrar usuarios [ahora se requiere una mayuscula, un caracter especial y un numero más las restricciones que estaban antes], tambien se quitó la limitación de nombres distintos entre usuarios [ahora se permite que dos usuarios tengan el mismo nombre pero obviamente distinto correo!!!]`
  - `Se actualizo la base de datos con nuevos usuarios con los nuevos datos ciudad y region`
  - `Se aplicaron las mismas validaciones que tiene el correo al nombre para tener validaciones en ese apatado tambien`
  - `Se aplicaron validaciones a los campos de ciudad y region`
  - `Comienzo de la implementacion del sistema de notificaciones fuera de la carpeta src, por el momento podemos enviar correos con emisario de atmosphericlettuce hacia otros destinatarios (planilla html, planilla pdf y correo de texto)`

## 📌 Semana 8  
- Correcion de errores del hito 1  
  - ` `
## 📌 Semana 9
- Migracion a SQL Lite con el CRUD completo
- `Solo pueden ingresar usuarios que se encuentren dentro de la base de datos.`
- `Se pueden registar usuarios y estos de guardan dentro de la base de datos.`
- `Se pueden agregar y eliminar cultivos con la cantidad de hectareas que el usuario le defina. `
- `El usuario puede editar su informacion(nombre,cuidad,region) y estos datos se actualizan dentro de la base de datos.`
- `El usuario puede cerrar seson siendo redirigido al login. `
- `El usuario puede eliminar su cuenta y esta tambien se borra de forma permanete dentro de la base de datos.` 

## 📌 Semana 10
- Exponer API Rest 
- `Se documentaron los endpoints de tanto de la API interna como los de las API externas.`
- `Se demostro que todos nuestros endpoints de las API internas funcionaban correctamente.`
- `La documentacion de los endpoints se realizo en el archivo endpoints.md donde se encuentra detallado cada uno.`

## 📌 Semana 11
- Integracion de API externas con el backend 
- `Es funcional el chatbot al cual se le puede enviar mensajes,fotos,archivos pdf, el chatbot se demora alrededor de 3 a 5 segundos en dar una respuesta en base a la pregunta del usuario.`
- `Se configuro el tema de las notificaciones las cuales le llegan semanalmente a los usuarios, en donde pueden encontran informacion del clima de los 7 dias de la semana.`
- `La API del clima muestra la informacion real del clima basado en la ubicacion del usuario.`
- `El usuario a traves de la barra de busqueda puede ingresar la ubicacion que el quiera ver.`
- `Se implemento el manejo de el manejo de errores de las API externas.`

## 📌 Semana 12
- Implementacion de las pruebas unitarias
- `Se aplico linter al proyecto tanto al backend como al frontend.`
- `Se corrigieron todos los errores que arrojo el linter.`
- `Los endpoints estan completos tanto los endpoints de las API internas como los de las API externas.`
- `Se hicieron pruebas unitarias a las carpetas de controllers, services y routes.`
- `Se aplico la libreria Pytest para las pruebas unitarias.`

## 📌 Semana 13
- Correccion de errores para presentacion del hito 2
- `Se creo documento de retroalimentacion donde se explica la metodologia aplicada hasta ahora.`
- `Se aplicaron validaciones a controllers.`
- `Se cambio el diseño al formulario.`
- `Implementacion de display de datos metereologicos.`
- `Creacion de landing page.`
- `Implementacion de selector de cultivo en el chatbot.`
- `Conexion realizada al backend en consultas al chatbot.`
- `Creacion de plantilla de warning.`
- `Modificacion de la planilla informe.`
- `Creacion de los metodos para pasarse la info del cultivo y clima de cada cultivo al chatbot.`
- `Implementacion de la logica de los warning.`
- `Creacion otra tabla con el clima de cultivos.`

