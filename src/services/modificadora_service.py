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

def modificar_warning_html(correo, usuariop1, cultivos_alertas, condiciones_iniciales, condiciones_actuales, consejos):
    """
    Genera HTML de advertencia con alertas climáticas.
    
    Args:
        correo: Email del usuario
        usuariop1: Datos del usuario
        cultivos_alertas: Lista de cultivos con alertas [{nombre, tipo_alerta, severidad}]
        condiciones_iniciales: Lista de condiciones climáticas iniciales
        condiciones_actuales: Lista de condiciones climáticas actuales
        consejos: Lista de consejos [{cultivo, consejo, alerta}]
    """
    env = Environment(loader=FileSystemLoader("services/Archivos_HTML"))
    template = env.get_template("warning.html")
    
    # Combinar datos para el template
    alertas_completas = []
    for i, cultivo_alerta in enumerate(cultivos_alertas):
        alerta_data = {
            "cultivo": cultivo_alerta["nombre"],
            "tipo_alerta": cultivo_alerta["tipo_alerta"],
            "severidad": cultivo_alerta["severidad"],
            "condicion_inicial": condiciones_iniciales[i] if i < len(condiciones_iniciales) else {},
            "condicion_actual": condiciones_actuales[i] if i < len(condiciones_actuales) else {},
            "consejo": consejos[i]["consejo"] if i < len(consejos) else "Se recomienda monitorear de cerca."
        }
        alertas_completas.append(alerta_data)
    
    html_renderizado = template.render(
        usuario=usuariop1,
        usuario_correo=correo,
        alertas=alertas_completas,
        total_alertas=len(alertas_completas)
    )
    
    with open("services/Archivos_HTML/warning_salida.html", "w", encoding="utf-8") as f:
        f.write(html_renderizado)
    
    print(f"✅ HTML de advertencia generado con {len(alertas_completas)} alerta(s)")
# ---------------------------------------------------