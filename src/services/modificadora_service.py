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
