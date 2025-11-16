from jinja2 import Environment, FileSystemLoader


# cambiar rutas----------------------
def modificar_html(correo, usuariop1, clima_, consejos):
    # ---------------------------------------------------
    # Configurar Jinja2 para que busque la carpeta plantilla_html
    env = Environment(loader=FileSystemLoader("services/Archivos_HTML"))

    # Cargar la plantilla
    template = env.get_template("index.html")

    # Renderizar el HTML con datos
    html_renderizado = template.render(
        usuario=usuariop1,
        usuario_correo=correo,
        clima=clima_,
        consejos=consejos
    )

    # Guardar el HTML resultante
    with open("services/Archivos_HTML/salida.html", "w",
              encoding="utf-8") as f:
        f.write(html_renderizado)

    print("✅ HTML generado en salida.html")
# ---------------------------------------------------


def modificar_warning_html(
        correo,
        usuariop1,
        cultivos_alertas,
        condiciones_iniciales,
        condiciones_actuales,
        consejos):
    """
    Genera HTML de advertencia con alertas climáticas.

    Args:
        correo: Email del usuario
        usuariop1: Datos del usuario
        cultivos_alertas: Lista de cultivos con alertas
                          [{nombre, tipo_alerta, severidad}]
        condiciones_iniciales: Lista de condiciones climáticas iniciales
        condiciones_actuales: Lista de condiciones climáticas actuales
        consejos: Lista de consejos [{cultivo, consejo, alerta}]
    """
    env = Environment(loader=FileSystemLoader("services/Archivos_HTML"))
    template = env.get_template("warning.html")

    # Agrupar alertas por cultivo
    cultivos_dict = {}

    for i, cultivo_alerta in enumerate(cultivos_alertas):
        nombre_cultivo = cultivo_alerta["nombre"]

        if nombre_cultivo not in cultivos_dict:
            cultivos_dict[nombre_cultivo] = {
                "nombre": nombre_cultivo,
                "alertas": [],
                "severidad_maxima": "media"
            }

        # Agregar alerta al cultivo
        cultivos_dict[nombre_cultivo]["alertas"].append({
            "tipo_alerta": cultivo_alerta["tipo_alerta"],
            "severidad": cultivo_alerta["severidad"],
            "condicion_inicial": (
                condiciones_iniciales[i]
                if i < len(condiciones_iniciales) else {}
            ),
            "condicion_actual": (
                condiciones_actuales[i]
                if i < len(condiciones_actuales) else {}
            )
        })

        # Actualizar severidad máxima
        if cultivo_alerta["severidad"] == "alta":
            cultivos_dict[nombre_cultivo]["severidad_maxima"] = "alta"

    # Agregar consejos
    for consejo_item in consejos:
        nombre_cultivo = consejo_item.get("cultivo")
        if nombre_cultivo in cultivos_dict:
            cultivos_dict[nombre_cultivo]["consejo"] = (
                consejo_item.get(
                    "consejo",
                    "Se recomienda monitorear de cerca."
                )
            )

    # Convertir a lista
    cultivos_agrupados = list(cultivos_dict.values())

    html_renderizado = template.render(
        usuario=usuariop1,
        usuario_correo=correo,
        cultivos=cultivos_agrupados,
        total_alertas=len(cultivos_alertas),
        total_cultivos=len(cultivos_agrupados)
    )

    with open("services/Archivos_HTML/warning_salida.html", "w",
              encoding="utf-8") as f:
        f.write(html_renderizado)

    print(f"✅ HTML de advertencia generado: "
          f"{len(cultivos_agrupados)} cultivo(s), "
          f"{len(cultivos_alertas)} alerta(s)")

# ---------------------------------------------------
