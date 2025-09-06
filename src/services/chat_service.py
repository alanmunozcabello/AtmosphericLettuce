import fitz
from plant_service import preguntar_enfermedad
from ai_service import preguntar_mistral
#pseudo implementación de la gestión del chat. NO IMPLEMENTACIÓN COMPLETA!!!!!
def pdf_to_txt(entrada_de_relleno): #ver como pasar pdf o dirección de almacenamiento, etc. de momento la entrada es para que no explote nada
    doc = fitz.open("Proyecto_pdf.pdf")
    with open("transcripcion.txt", "w", encoding="utf-8") as transcripcion: 
        for pagina in doc:
            transcripcion.write(pagina.get_text()+'\n')
            return " " #retorna algo sin sentido de mientras
    doc.close()

def procesar_mensaje(mensaje): #deberia de ser un diccionario
    contexto=[] #esto arreglo de diccionarios se le pasará a ai_service

    if "imagenes" in mensaje: #por cada imagen en el mensaje llama a preguntar_enfermedad() y se guarda la respuesta
        for imagen in mensaje["imagenes"]:
            resultado_imagen=preguntar_enfermedad(imagen)#revisar funcion en plant_service!!!!!----------------------------------------------
            contexto.append(f"resultado imagen {imagen}: {resultado_imagen}")

    if "pdfs" in mensaje: #por cada pdf en el mensaje se transforma a texto llamando a pdf_to_txt() y se guarda la respuesta
        for pdf in mensaje["pdfs"]:
            texto_pdf=pdf_to_txt(pdf)
            contexto.append(f"resultado pdf {pdf}: {texto_pdf}")
    
    if "texto" in mensaje: #se añade el texto del usuario al contexto
        contexto.append(f"mensaje usuario: {mensaje["texto"]}")

    return preguntar_mistral(contexto) #retornar la respuesta del chatbot al frontend