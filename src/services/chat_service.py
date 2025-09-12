import fitz
import json
# from plant_service import preguntar_enfermedad
from services.ai_service import preguntar_mistral

#pseudo implementación de la gestión del chat. NO IMPLEMENTACIÓN COMPLETA!!!!!
def pdf_to_txt(pdf): #ver como pasar pdf o dirección de almacenamiento, etc. de momento la entrada es para que no explote nada
    pdf = fitz.open("Proyecto_pdf.pdf")
    with open("transcripcion.txt", "w", encoding="utf-8") as transcripcion: 
        for pagina in pdf:
            transcripcion.write(pagina.get_text()+'\n')
        return transcripcion #retorna algo sin sentido de mientras
    pdf.close()

def procesar_consulta(payload): #deberia de ser un diccionario
    contexto=[] #esto arreglo de diccionarios se le pasará a ai_service

    # mensaje=json.loads(mensaje_string)
    print(payload)
    contexto.append(f"mensaje usuario: {payload["texto"]}")
    # if "imagenes" in mensaje: #por cada imagen en el mensaje llama a preguntar_enfermedad() y se guarda la respuesta
    #     for imagen in mensaje["imagenes"]:
    #         resultado_imagen=preguntar_enfermedad(imagen)#revisar funcion en plant_service!!!!!----------------------------------------------
    #         contexto.append(f"resultado imagen {imagen}: {resultado_imagen}")

    # if "pdfs" in mensaje: #por cada pdf en el mensaje se transforma a texto llamando a pdf_to_txt() y se guarda la respuesta
    #     for pdf in mensaje["pdfs"]:
    #         texto_pdf=pdf_to_txt(pdf)
    #         contexto.append(f"resultado pdf {pdf}: {texto_pdf}")
    
    # if "texto" in mensaje: #se añade el texto del usuario al contexto
    #     contexto.append(f"mensaje usuario: {mensaje["texto"]}")

    return preguntar_mistral(contexto) #retornar la respuesta del chatbot al frontend
    