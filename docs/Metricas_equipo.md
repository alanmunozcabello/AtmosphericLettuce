# 📊 Métricas de Rendimiento - Equipo Lechuga

**Fecha de Corte:** 10/12/2025
**Sprint/Fase Evaluada:** Fase Final

---

## 👥 Resumen General del Equipo

| Métrica | Total Equipo | Promedio por Integrante |
|:---|:---:|:---:|
| **Total Commits** | 382 | 95.5 |
| **Total Pull Requests (PRs)** | 16 | 4 |
| **Lead Time Promedio** | 8.2 días | - |
| **Tareas Completadas (Trello)** | 74 + 11 | 21.25 |

> **Definiciones:**
> * **Lead Time:** Tiempo transcurrido desde que una tarea se mueve a "En Progreso" hasta que llega a "Terminado" (Done).
> * **PRs:** Pull Requests creados y mergeados.

---

## 👤 Desglose Individual

### 1. Alan Muñoz
* **Rol Principal:** Backend / Frontend / QA
* **Commits:** 145
* **Pull Requests (PRs):** 4
* **Tareas Completadas (Trello):** 40 + 7
* **Lead Time Promedio:** 7.1 días
* **Áreas de Impacto:**
    * **Lógica de Negocio y Backend:** Implementación del núcleo funcional (manejo de ubicación, persistencia de cultivos).
    * **Integración de IA:** Implementación de Deepseek y funcionalidad del chatbot (mensajes, imágenes, PDFs).
    * **Integración Temprana de APIs Externas:** Implementación inicial de APIs OpenWeatherMap y Crop.health con bibliotecas GIS OpenLayers y Nominatim.
    * **Manejo de Datos:** Transición de datos de prueba a datos reales de API y persistencia inicial.

### 2. Cristian Aliaga
* **Rol Principal:** Líder Técnico / Backend / Frontend
* **Commits:** 70
* **Pull Requests (PRs):** 0
* **Tareas Completadas (Trello):** 23 + 6
* **Lead Time Promedio:** 7.0 días
* **Áreas de Impacto:**
    * **Arquitectura de Base de Datos:** Migración a SQLite, CRUD y persistencia de datos complejos.
    * **Integración de Sistemas Externos:** Conexión con APIs externas, manejo de errores robustos y timeouts.
    * **Seguridad:** Sistema de seguridad (hashing) y autenticación.

### 3. John Rojas
* **Rol Principal:** Frontend / QA / Líder Técnico
* **Commits:** 54
* **Pull Requests (PRs):** 0
* **Tareas Completadas (Trello):** 27 + 3
* **Lead Time Promedio:** 8.7 días
* **Áreas de Impacto:**
    * **Frontend y UI/UX:** Creación de la interfaz navegable HTML/CSS base.
    * **Validación de Cliente:** Implementación de reglas de validación en el frontend.
    * **Integración:** Conexión inicial entre las vistas y los servicios del backend.

### 4. Nicolás Urbina
* **Rol Principal:** QA / Líder Técnico / Backend
* **Commits:** 113
* **Pull Requests (PRs):** 12
* **Tareas Completadas (Trello):** 39 + 7
* **Lead Time Promedio:** 8.3 días
* **Áreas de Impacto:**
    * **Desarrollo Full Stack:** Puente entre lógica de backend y visualización en frontend (integración, formularios, notificaciones).
    * **Calidad de Código y Automatización:** Configuración de Linter, tareas automáticas y optimización de performance.
    * **Refactorización:** Separación de validaciones de la lógica de negocio y limpieza de arquitectura.

---

## 📈 Análisis de Lead Time (Trello)

*Esta sección analiza cuánto tiempo tardamos en cerrar las tareas más críticas.*

| Tarea / Funcionalidad (Trello) | Asignado a | Fecha Inicio | Fecha Fin | Lead Time (Días) |
|:---|:---|:---:|:---:|:---:|
| Definir Funcionalidades y requisitos funcionales | Todos | 15/08 | 25/08 | 10 |
| Definir arquitectura por capas y estructura de carpetas en el repositorio | Todos | 20/08 | 31/08 | 11 |
| Implementar capa de persistencia inicial (lectura/escritura en archivos JSON/CSV) | Alan Muñoz | 20/08 | 31/08 | 11 |
| Implementar capa de datos (lectura/escritura JSON/CSV) con datos de prueba reales. | Alan Muñoz, Nicolas Urbina | 31/08 | 08/09 | 8 |
| Asegurar manejo básico de errores (archivo no encontrado, datos inválidos). | Alan Muñoz, Nicolas Urbina | 31/08 | 08/09 | 8 |
| Implementar validaciones básicas en frontend (campos obligatorios, formatos). | John Rojas | 31/08 | 15/09 | 15 |
| Crear interfaz navegable con HTML/CSS/JS (mínimo: home, listado, formulario). | John Rojas | 31/08 | 15/09 | 15 |
| Implementación del chatbot funcional para soportar mensaje + imágenes + pdfs. | Alan Muñoz, Nicolas Urbina | 16/09 | 24/09 | 8 |
| Implementar manejo de la ubicación del usuario con latitud y longitud | Alan Muñoz, Nicolas Urbina | 23/09 | 29/09 | 6 |
| Implementación y persistencia del manejo de los cultivos del usuario. | Alan Muñoz, Nicolas Urbina | 23/09 | 30/09 | 7 |
| Implementar validaciones básicas en frontend (campos obligatorios, formatos). | John Rojas, Nicolas Urbina | 22/09 | 29/09 | 7 |
| Modificar métodos HTTP de las rutas (.post .get .delete .patch .put) a los correctos. | Cristian Aliaga, Alan Muñoz, Nicolas Urbina | 23/09 | 29/09 | 6 |
| Integración entre el backend y el frontend | John Rojas, Nicolas Urbina | 28/09 | 30/09 | 2 |
| Implementación del sistema de seguridad con contraseñas hasheo y comparación entre contraseña y contraseña | Cristian Aliaga, Alan Muñoz, Nicolas Urbina | 28/09 | 30/09 | 2 |
| Implementación de cerrar sesión. | John Rojas, Alan Muñoz | 30/09 | 30/09 | 1 |
| Implementación de borrar usuario | Cristian Aliaga, Alan Muñoz | 30/09 | 30/09 | 1 |
| Migracion a SQL lite | Criastian Aliaga | 08/10 | 08/10 | 1 |
| Lograr CRUD con la base de datos | Criastian Aliaga | 09/10 | 09/10 | 1 |
| Implementacion de Deepseek | Alan Muñoz | 18/10 | 18/10 | 1 |
| Creación de formularios emergentes para la informacion detallada de cada lugar con cultivos | Alan Muñoz, Nicolas Urbina | 06/10 | 19/10 | 13 |
| Implementar persistencia en foto de perfil | Criastian Aliaga | 13/10 | 19/10 | 6 |
| Creacion de HTML,CSS,JS para formulario cultivos | Nicolas Urbina | 10/10 | 26/10 | 16 |
| Integracion de API externa | Cristian Aliaga | 18/10 | 01/11 | 14 |
| Mostrar Datos reales de la API en la interfaz | Alan Muñoz | 18/10 | 01/11 | 14 |
| Manejo de timeouts y errores con las API externa | Cristian Aliaga | 18/10 | 03/11 | 16 |
| Creacion de tareas automaticas | Nicolas Urbina | 01/11 | 03/11 | 2 |
| Configurar y ejecutar linter en el proyecto | Nicolas Urbina | 01/11 | 10/11 | 9 |
| Implementar 4 a 6 pruebas unitarias para las API | Cristian Aliaga | 01/11 | 10/11 | 9 |
| Creación de la planilla HTML para el Sistema de notificaciones | Nicolas Urbina | 23/10 | 10/11 | 18 |
| Implementar sistema de recuperación de cuentas. | Alan Muñoz | 05/12 | 08/12 | 3 |
| Autenticación y Seguridad | Crisitan Aliaga, Nicolas Urbina | 20/11 | 09/12 | 19 |
| Implementación de Búsqueda y Paginación | Cristian Aliaga, Nicolas Urbina | 27/11 | 09/12 | 12 |
| Separar validaciones de la lógica de negocio | Nicolas Urbina | 27/11 | 09/12 | 12 |
| Optimización de Performance | Cristian Aliaga, Nicolas Urbina | 27/11 | 09/12 | 12 |
| Cierre de Issues y Merge Final | Todos | 09/12 | 09/12 | 1 |
| Finalizar proyecto | Todos | 09/12 | 09/12 | 1 |


---

## 🔄 Ciclo de Pull Requests

*Eficiencia en la revisión y fusión de código.*

* **PRs Mergeados sin cambios:** 1 (Aprobación directa)
* **PRs con cambios solicitados:** 7 (Requirieron correcciones)
* **PRs cancelados o rechazados:** 8
* **Tiempo promedio de aprobación:** 1 Hora

---

## 📝 Conclusiones del Análisis

1. **Velocidad:** El equipo mantiene un Lead Time promedio de **8.2 días**, lo cual es consistente con la complejidad de las tareas abordadas.
2. **Calidad:** Se observa un alto número de commits (382) en relación a los PRs (16), indicando un trabajo iterativo y de refinamiento constante.
3. **Distribución:** La carga de trabajo está distribuida, con Alan y Nicolás liderando en cantidad de commits y tareas transversales, mientras que Cristian y John aportan en áreas críticas de arquitectura y frontend.
4. **Evolución Tecnológica:** El proyecto muestra una clara maduración técnica, migrando de una persistencia básica en archivos JSON hacia una base de datos relacional (SQLite) y escalando hacia la integración de IA (Deepseek) y APIs externas.
5. **Foco Actual:** El equipo se encuentra en una etapa de **estabilización y optimización**, priorizando actualmente la seguridad (autenticación), el rendimiento (paginación, timeouts) y la calidad del código (linter, pruebas unitarias) para el cierre del proyecto.

---