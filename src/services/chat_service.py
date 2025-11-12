import fitz
import base64
import os
from services.plant_service import preguntar_enfermedad
from services.ai_services import preguntar_mistral
from services.usuarios_service import service_obtener_info_cultivo


# Pseudo implementación de la gestión del chat.
# NO IMPLEMENTACIÓN COMPLETA!!!!!


def pdf_to_txt(pdf):
    # Función en desuso, el PDF ya viene en base64 desde el frontend
    pdf = fitz.open("Proyecto_pdf.pdf")
    with open("transcripcion.txt", "w", encoding="utf-8") as transcripcion:
        for pagina in pdf:
            transcripcion.write(pagina.get_text() + '\n')
        return transcripcion  # Retorna objeto temporal
    pdf.close()


def procesar_consulta(payload):
    # Recibe un diccionario con el contenido a procesar
    contexto = []  # Lista de diccionarios para enviar a ai_service

    if payload.get("texto"):  # Procesar texto si existe en el payload
        contexto.append({"mensaje usuario": payload["texto"]})

    if payload.get("imagen"):  # Procesar imágenes múltiples
        for imagen in payload["imagen"]:
            contexto.append({"json": preguntar_enfermedad(imagen)})

    if payload.get("correo") is not None and payload.get("cultivo") is not None:
        info_cultivo = service_obtener_info_cultivo(
            payload.get("correo"),
            payload.get("cultivo")
            ) 
        contexto.append({"info_cultivo": info_cultivo})
    
    if payload.get("pdf"):  # Procesar PDFs múltiples
        for pdf_64 in payload["pdf"]:
            # Decodificar el PDF desde base64
            pdf_decodificado = base64.b64decode(pdf_64)

            # Guardar PDF temporal
            with open("temp.pdf", "wb") as f:
                f.write(pdf_decodificado)

            # Extraer contenido del PDF
            doc = fitz.open("temp.pdf")
            texto = ""
            for pagina in doc:
                texto += pagina.get_text() + "\n"
            doc.close()

            # Eliminar archivo temporal
            os.remove("temp.pdf")
            contexto.append({"contenido pdf": texto})

    return preguntar_mistral(contexto)  # Retornar respuesta del chatbot
