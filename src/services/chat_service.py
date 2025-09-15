import fitz
import json
import base64
import os
from services.plant_service import preguntar_enfermedad
from services.ai_service import preguntar_mistral

#pseudo implementación de la gestión del chat. NO IMPLEMENTACIÓN COMPLETA!!!!!
def pdf_to_txt(pdf): #ver como pasar pdf o dirección de almacenamiento, etc. de momento la entrada es para que no explote nada
    pdf = fitz.open("Proyecto_pdf.pdf")
    with open("transcripcion.txt", "w", encoding="utf-8") as transcripcion: 
        for pagina in pdf:
            transcripcion.write(pagina.get_text()+'\n')
        return transcripcion #retorna algo sin sentido de mientras
    pdf.close()

def procesar_consulta(payload):  # debería ser un diccionario
    contexto = []  # este arreglo de diccionarios se le pasará a ai_service
    if payload.get("texto"): #si el payload tiene la clave "texto" se añade al contexto
        contexto.append({"mensaje usuario": payload["texto"]})

    if payload.get("imagen"): #una ves esté listo volver a esto (implementar soporte para multiples imágenes)------------------------------
        for imagen in payload["imagen"]:
            contexto.append({"json":preguntar_enfermedad(imagen)})

    if payload.get("pdf"): #una ves esté listo volver a esto (implementar soporte para multiples pdf (un for simple y cambiar linea 15 en el script de base64 -> [base64]))
        
        for pdf_64 in payload["pdf"]:
            # pdf_64 = payload["pdf"]
            pdf_decodificado = base64.b64decode(pdf_64) #decodificar el pdf en base64

            with open("temp.pdf", "wb") as f: #pdf temporal
                f.write(pdf_decodificado)

            doc = fitz.open("temp.pdf") #extraer contenido del pdf con fitz
            texto = ""
            for pagina in doc:
                texto += pagina.get_text() + "\n"
            doc.close()
            os.remove("temp.pdf") #matar el pdf temporal

            contexto.append({"contenido pdf": texto})

    print(contexto)

    return preguntar_mistral(contexto)  # retornar la respuesta del chatbot al frontend