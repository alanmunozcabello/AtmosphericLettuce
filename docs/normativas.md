#  Normativas, Reglamentos y Estándares - AtmosphericLettuce

Este documento detalla el marco legal, normativo y los estándares comerciales aplicables al proyecto **AtmosphericLettuce**, considerando su naturaleza como plataforma de software agrícola ('AgroTech') que opera en Chile y procesa datos personales.

## 1.  Protección de Datos y Privacidad (Chile)

Dado que la plataforma gestiona perfiles de usuarios y datos personales, el cumplimiento de la legislación chilena sobre privacidad es mandatorio.

*   **Ley N° 21.719 (Nueva Ley de Protección de Datos Personales):**
    *   **Estado:** Publicada en diciembre de 2024 (en vacancia legal hasta 2026).
    *   **Impacto:** Alinea a Chile con estándares internacionales como el GDPR.
    *   **Requisitos Clave:**
        *   **Consentimiento:** Debe ser explícito para el tratamiento de datos.
        *   **Derechos ARCO:** Garantizar derechos de Acceso, Rectificación, Cancelación y Oposición a los usuarios.
        *   **Seguridad:** Obligación de reportar brechas de seguridad.
        *   **Principio de Responsabilidad (Accountability):** Demostrar activamente el cumplimiento.

*   **Ley N° 19.628 (Sobre la Protección de la Vida Privada):**
    *   **Estado:** Vigente (marco base actual).
    *   **Relevancia:** Regula el tratamiento de datos de carácter personal en registros o bancos de datos.

## 2.  Normativas Agrícolas y Buenas Prácticas (Chile)

Al entregar recomendaciones agrícolas y gestionar información de cultivos, es crucial alinearse con las directrices de organismos oficiales.

*   **Servicio Agrícola y Ganadero (SAG):**
    *   Normativas sobre **sanidad vegetal** y control de plagas que deben considerarse al dar recomendaciones fitosanitarias.
    *   Regulaciones sobre **semillas y plantas frutales**.
*   **Buenas Prácticas Agrícolas (BPA):**
    *   Estándares voluntarios pero altamente valorados comercialmente (como GlobalG.A.P. o normas nacionales de AChipia).
    *   El software debe fomentar el registro de datos que faciliten la **trazabilidad**, un pilar fundamental de las BPA.

## 3.  Calidad de Software y Seguridad

Estándares internacionales para asegurar la calidad del producto tecnológico.

*   **ISO/IEC 25000 (SQuaRE):**
    *   Familia de normas para la evaluación de la calidad del producto de software (Funcionalidad, Rendimiento, Usabilidad, Seguridad, Mantenibilidad).
*   **ISO 27001 (Seguridad de la Información):**
    *   Estándar de oro para la gestión de la seguridad de la información. Relevante para asegurar la confidencialidad de los datos de los agricultores.
*   **OWASP Top 10:**
    *   Estándar de facto para la seguridad de aplicaciones web. El desarrollo debe mitigar riesgos comunes como inyecciones SQL, XSS y fallos de autenticación.

## 4.  Uso de Drones (Procesamiento de Imágenes)

Si bien el proyecto procesa imágenes, el origen de estas puede ser mediante drones, lo que implica regulaciones específicas.

*   **Normas Aeronáuticas (DGAC):**
    *   **DAN 151:** Operaciones de aeronaves pilotadas a distancia (RPAS) en asuntos de interés público.
    *   **DAN 91:** Reglas del aire generales.
    *   **Relevancia:** Si AtmosphericLettuce integra captura directa o alianzas con operadores de drones, estos deben contar con licencia, registro ante la DGAC y seguros correspondientes.

## 5.  Inteligencia Artificial y Ética

Para el uso del Chatbot (DeepSeek AI) y algoritmos de recomendación.

*   **Transparencia Algorítmica:** Los usuarios deben saber cuando interactúan con una IA.
*   **Explicabilidad:** Las recomendaciones críticas para el cultivo deben tener una base lógica rastreable, no ser "cajas negras", para evitar pérdidas económicas al agricultor por malas decisiones automatizadas.
