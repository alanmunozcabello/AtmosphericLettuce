from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import os # <--- Módulo importado para manejar rutas

# pip install reportlab PyPDF2

def crear_pdf(clima,usuarios):
    # --- INICIO DE CAMBIOS ---
    # Obtenemos la ruta del directorio donde se encuentra este script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Creamos las rutas completas para cada archivo
    ruta_imagen_chestappen = os.path.join(script_dir, "Imagenes", "chestappen.jpg")
    ruta_imagen_lechuga = os.path.join(script_dir, "Imagenes", "Lechuga.jpg")
    ruta_planilla = os.path.join(script_dir, "Planilla.pdf")
    ruta_pdf_modificado = os.path.join(script_dir, "pdf_modificado.pdf")
    # --- FIN DE CAMBIOS ---

    # Crear un PDF temporal con el texto que quieres escribir
    print(usuarios.get("nombre"))

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    # Parte superior del pdf

    can.setFont("Helvetica", 20)
    # Usamos la nueva ruta para la imagen
    can.drawImage(ruta_imagen_chestappen, 450, 700, width=100, height=100)
    #texto
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 15 
    style.textColor = colors.black
    style.leading = 15  # Espacio entre líneas
    texto = f"<b>{usuarios.get('nombre')}</b> <b>{usuarios.get('apellido')}</b>"
    p = Paragraph(texto, style)
    # x, y = esquina inferior izquierda del cuadro, w = ancho, h = alto
    p.wrapOn(can, 250, 150)  # ancho=200, alto=100 (ajusta según tu espacio)
    p.drawOn(can, 220, 770)  # posición del cuadro
    
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 15 
    style.textColor = colors.black
    style.leading = 15  # Espacio entre líneas
    texto = f"<b>{usuarios.get('correo')}</b>"
    p = Paragraph(texto, style)
    # x, y = esquina inferior izquierda del cuadro, w = ancho, h = alto
    p.wrapOn(can, 230, 150)  # ancho=200, alto=100 (ajusta según tu espacio)
    p.drawOn(can, 220, 750)  # posición del cuadro
     #-------------------

    #cuadros del tiempo 1
    can.setFillColorRGB(255, 255, 255) # Color blanco
    can.setFont("Helvetica", 18)
    can.drawString(20, 655, clima.get("dia1").get("dia")) #variable con el dia
    cadena_aux = str(clima.get("dia1").get("temp"))+"°C"            #str(20)+"°C" #variable con el tiempo de ese dia
    can.drawString(20, 633, cadena_aux)
    can.setFont("Helvetica", 12)
    cadena_aux = "Max: " + str(clima.get("dia1").get("max"))+"°C Min: " + str(clima.get("dia1").get("min"))+"°C" #variable con la temperatura maxima y minima 
    can.drawString(20, 615, cadena_aux)
    can.setFont("Helvetica", 18)
    can.drawString(20, 595, clima.get("dia1").get("estado")) #variable con el estado del tiempo

    #cuadros del tiempo 2
    can.drawString(20, 550, clima.get("dia4").get("dia")) #variable con el dia
    cadena_aux = str(clima.get("dia4").get("temp"))+"°C"
    can.drawString(20, 528, cadena_aux) 
    can.setFont("Helvetica", 12)
    cadena_aux = "Max: " + str(clima.get("dia4").get("max"))+"°C Min: " + str(clima.get("dia4").get("min"))+"°C" #variable con la temperatura maxima y minima 
    can.drawString(20, 510, cadena_aux)
    can.setFont("Helvetica", 18)
    can.drawString(20, 495, clima.get("dia4").get("estado")) #variable con el estado del tiempo


    #cuadros del tiempo 3
    can.drawString(215, 655, clima.get("dia2").get("dia")) #variable con el dia
    cadena_aux = str(clima.get("dia2").get("temp"))+"°C"
    can.drawString(215, 633, cadena_aux)
    can.setFont("Helvetica", 12)
    cadena_aux = "Max: " + str(clima.get("dia2").get("max"))+"°C Min: " + str(clima.get("dia2").get("min"))+"°C" #variable con la temperatura maxima y minima 
    can.drawString(215, 615, cadena_aux)
    can.setFont("Helvetica", 18)
    can.drawString(215, 595, clima.get("dia2").get("estado")) #variable con el estado del tiempo


    #cuadros del tiempo 4
    can.drawString(215, 550, clima.get("dia5").get("dia")) #variable con el dia
    cadena_aux =  str(clima.get("dia4").get("temp"))+"°C"
    can.drawString(215, 528, cadena_aux) 
    can.setFont("Helvetica", 12)
    cadena_aux = "Max: " + str(clima.get("dia5").get("max"))+"°C Min: " + str(clima.get("dia5").get("min"))+"°C" #variable con la temperatura maxima y minima 
    can.drawString(215, 510, cadena_aux)
    can.setFont("Helvetica", 18)
    can.drawString(215, 495, clima.get("dia5").get("estado")) #variable con el estado del tiempo


    #cuadros del tiempo 5
    can.drawString(410, 655, clima.get("dia3").get("dia")) #variable con el dia
    cadena_aux =  str(clima.get("dia3").get("temp"))+"°C"
    can.drawString(410, 633, cadena_aux) 
    can.setFont("Helvetica", 12)
    cadena_aux = "Max: " + str(clima.get("dia3").get("max"))+"°C Min: " + str(clima.get("dia3").get("min"))+"°C" #variable con la temperatura maxima y minima 
    can.drawString(410, 615, cadena_aux)
    can.setFont("Helvetica", 18)
    can.drawString(410, 595, clima.get("dia3").get("estado")) #variable con el estado del tiempo


    #cuadros del tiempo 6
    can.drawString(410, 550, clima.get("dia6").get("dia")) #variable con el dia
    cadena_aux =  str(clima.get("dia6").get("temp"))+"°C"
    can.drawString(410, 528, cadena_aux) 
    can.setFont("Helvetica", 12)
    cadena_aux = "Max: " + str(clima.get("dia6").get("max"))+"°C Min: " + str(clima.get("dia6").get("min"))+"°C" #variable con la temperatura maxima y minima 
    can.drawString(410, 510, cadena_aux)
    can.setFont("Helvetica", 18)
    can.drawString(410, 495, clima.get("dia6").get("estado")) #variable con el estado del tiempo



    #cultivos
    can.drawString(25, 430, "Cultivos") #variable con el cultivo 1
    #for each?
    i=0
    for cultivo in usuarios.get("cultivos").values():
        can.drawString(20, 390-i, "-Cultivo 2") #variable con el cultivo 2 
        i+=30

    #Emfermedades ----------------------------------------------------------- pendiente 
    can.drawString(215, 430, "Emfermedades") 
    # Usamos la nueva ruta para la imagen
    can.drawImage(ruta_imagen_lechuga, 215, 260, width=150, height=150)

    #texto
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 15 
    style.textColor = colors.white
    style.leading = 15  # Espacio entre líneas

    texto = (
        "Una planta enferma a menudo muestra sumalestar de forma visible ydramática. Sus hojas, queantes eran vibrantes, sevuelven pálidas oamarillentas, con bordesmarrones o manchascirculares de un colorextraño que se extiendenlentamente."
    )

    p = Paragraph(texto, style)
    # x, y = esquina inferior izquierda del cuadro, w = ancho, h = alto
    p.wrapOn(can, 180, 150)  # ancho=200, alto=100 (ajusta según tu espacio)
    p.drawOn(can, 380, 250)  # posición del cuadro

    #consejos ----------------------------------------------------------
    can.drawString(20, 190, "Consejos:") 
    #texto
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 15 
    style.textColor = colors.white
    style.leading = 15  # Espacio entre líneas

    texto = (
        "Para cuidar una planta, es clave observar sus necesidades de luz, agua y nutrientes. Cada planta esúnica, pero una regla de oro es evitar el exceso de riego, ya que la mayoría de las enfermedades yproblemas radiculares surgen de un suelo demasiado húmedo. Toca el sustrato para sentir si estáseco antes de volver a regar, y asegúrate de que tu planta reciba la cantidad de luz adecuada segúnsu especie."
    )

    p = Paragraph(texto, style)
    # x, y = esquina inferior izquierda del cuadro, w = ancho, h = alto
    p.wrapOn(can, 550, 150)  # ancho=200, alto=100 (ajusta según tu espacio)
    p.drawOn(can, 20, 90)  # posición del cuadro

    can.save()

    # Mover el puntero al inicio
    packet.seek(0)

    # Leer el PDF original y el PDF temporal usando las nuevas rutas
    existing_pdf = PdfReader(open(ruta_planilla, "rb"))
    new_pdf = PdfReader(packet)
    output = PdfWriter()

    # Superponer la página nueva sobre la original
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    # Guardar el resultado usando la nueva ruta
    with open(ruta_pdf_modificado, "wb") as outputStream:
        output.write(outputStream)