# Arquitectura del Proyecto

La carpeta `src` está organizada siguiendo una arquitectura por capas, facilitando la separación de responsabilidades y el mantenimiento del código. A continuación se describe el propósito de cada carpeta:

## Estructura de Carpetas

- **routes/**
  - Define los endpoints o rutas de la API. Cada archivo en esta carpeta expone las rutas accesibles para los clientes y delega la lógica a los controladores.
  -

- **controllers/**
  - Contiene la lógica de negocio principal. Los controladores reciben las peticiones desde las rutas, procesan los datos y llaman a los servicios necesarios.

- **services/**
  - Encapsula la lógica de acceso a datos y operaciones complejas. Los servicios interactúan con los archivos de datos (`.json`) o bases de datos y devuelven la información procesada a los controladores.

- **data/**
  - Almacena los archivos de datos, como archivos `.json`, que contienen la información persistente utilizada por la aplicación.

## Ejemplo de Flujo de una Petición

1. El usuario realiza una petición a una ruta definida en `routes/`.
2. La ruta llama a una función del controlador correspondiente en `controllers/`.
3. El controlador procesa la petición y utiliza uno o varios servicios de `services/` para obtener o modificar datos.
4. Los servicios acceden a los archivos en `data/` para leer o escribir información.
5. La respuesta se construye y se envía de vuelta al usuario.

---

Esta arquitectura permite un desarrollo más ordenado, facilita las pruebas y el escalado del proyecto.
