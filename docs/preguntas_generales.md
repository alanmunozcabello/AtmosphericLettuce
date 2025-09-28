# 📋 Cuestionario – Proyecto Meteorológico (Equipo Lechuga)

## 1️⃣ Visión General del Proyecto

1. **Objetivo y alcance**
   - ¿Qué problema exacto queremos resolver con esta web de meteorología? 
        Ayudar a los usuarios a saber el estado meteorológico de una ubicación concreta.
   - ¿Cuál es el flujo principal que seguirá un usuario desde que entra hasta que obtiene la información?
   - ¿Mostraremos solo pronóstico actual o también histórico y a futuro?

2. **Usuarios y roles**
   - ¿Habrá un único tipo de usuario o varios (ej. visitante, usuario registrado, admin)?
        invitado, usuario registrado, extra: usuario premium con cosas extras.
   - ¿Qué acciones podrá hacer un usuario no registrado?
        invitado solo puede ver el dia actual con su ubicación.
   - ¿Qué beneficios tendrá un usuario registrado?
        podrá ver la semana entera con su ubicación.

3. **Datos climáticos**
   - ¿Qué información específica vamos a mostrar además de temperatura, humedad y sensación térmica?
        temperatura, humedad, sensación termica, precipitación.
   - ¿Queremos incluir imágenes o iconos representando el clima (ej. nublado, soleado, etc.)?
        si.
   - ¿Mostraremos datos horarios o solo un resumen diario?
        datos por hora.

4. **Autenticación y seguridad**
   - ¿Cómo será el registro e inicio de sesión (email, usuario, redes sociales)?
        usuario y contraseña.
   - ¿Se requerirá autenticación para ver datos climáticos o solo para guardar preferencias?
        se guardarán preferencias.

5. **Integración con API externa**
   - ¿Qué API meteorológica vamos a usar (OpenWeatherMap, WeatherAPI, etc.)?
        por saber.
   - ¿Con qué frecuencia se actualizarán los datos?
        cada vez que se haga la consulta.
   - ¿Qué datos mínimos necesitamos de esa API?
        los que se mostrarán mas que nada.

---

## 2️⃣ Backend (Enfoque Técnico)

1. **Datos y almacenamiento**
   - ¿Qué entidades principales tendremos en la base de datos (Usuarios, Ubicaciones, Preferencias, Registros climáticos)?
        Usuarios, Ubicaciones, Preferencias de los usuarios.
   - ¿Guardaremos datos históricos del clima o solo lo traeremos en tiempo real desde la API externa?
        No.
   - ¿Cómo se relacionan las entidades (ej. un usuario puede tener varias ubicaciones guardadas)?
        Usuariotiene preferencias asi como un nombre y contraseña.

2. **Estructura de API interna**
   - ¿Qué endpoints iniciales necesitamos para el Hito 1 (sin REST completo todavía)?
        Por ver.
   - ¿Qué validaciones serán necesarias en el backend (ej. formato de dirección, ubicación existente)?
        Por ver.
   - ¿Queremos implementar paginación o filtrado desde el inicio o dejarlo para el avanzado?
        Por ver.

3. **Persistencia progresiva**
   - ¿Qué datos vamos a guardar en JSON/CSV para el primer hito?
        Usuarios, Ubicaciones, Preferencias de los usuarios.
   - ¿Cómo haremos la migración a SQLite sin perder datos?
        Buena pregunta.
4. **Seguridad y control**
   - ¿Vamos a usar JWT o sesiones para autenticación?
        Usaremos autenticacion de contraseña por medio de hash comun y corriente.
   - ¿Guardaremos contraseñas con hash desde el inicio o recién en Hito 2?
        Por verse.

---

## 3️⃣ Semana 2 (S2) – Documento de Requisitos y Diseño

1. **Requisitos funcionales (RF)**
   - ¿Qué funciones sí o sí debe cumplir el sistema desde la versión inicial?
   - ¿Qué funciones avanzadas queremos incluir en la versión final?
   - ¿Qué casos de uso tiene que cubrir la web?  
     *(Ejemplo: “Usuario busca clima por dirección”, “Usuario guarda ubicación favorita”, etc.)*

2. **Requisitos no funcionales (RNF)**
   - ¿Velocidad de respuesta máxima que debería tener la API?
   - ¿Disponibilidad mínima esperada (ej. 99%)?
   - ¿Qué navegadores y dispositivos queremos soportar?
   - ¿Seguridad mínima (HTTPS, hash de contraseñas, etc.)?

3. **Wireframes**
   - ¿Cuáles serán las 3 pantallas clave? (Home, resultado de búsqueda, perfil/configuración)
        Inicio de seción, Home, Perfil de usuario... por verse realmente.
   - ¿Qué elementos obligatorios debe tener cada pantalla (campos, botones, mensajes)?

4. **Selección de API externa**
   - ¿Cuál ofrece la mejor relación entre datos, facilidad de uso y límite gratuito?
   - ¿Qué formato de respuesta entrega (JSON, XML)?
   - ¿Qué datos mínimos debemos extraer para cumplir nuestro objetivo?
        temperatura, humedad, sensación termica, precipitación.
