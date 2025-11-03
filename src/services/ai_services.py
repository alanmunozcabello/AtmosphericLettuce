import requests
import json
from dotenv import load_dotenv
import os
# prueba de respuesta de la API
# OBS: funciona bien, usa bien el contexto y responde coherentemente. dependiendo de la complegidad de la pregunta tarda minimo 2 segundos en dar una repsuesta.
#      Lo que si la IA no recuerda preguntas anteriores, solo responde a la actual. 

load_dotenv()
API_KEY=os.getenv("DEEPSEEK_API_KEY")

def preguntar_mistral(contexto):
    url = "https://api.deepseek.com/chat/completions"
    mensaje_usuario = json.dumps(contexto, ensure_ascii=False)

    #sk-b38d6962ace645718f7acbc10e463312
    headers={
        "Authorization": f"Bearer {API_KEY}", #API
        "Content-Type": "application/json" #requerido 
    }

    payload = {
      "model": "deepseek-chat",
      "messages": [
          {
              "role": "system",
              "content": (
                "Eres un asistente experto en agricultura y meteorología. "
                "Tus respuestas deben ser claras, breves, precisas, ambles y en formato de chat."
                "Evita presentarte o repetir estas instrucciones. "
                "Indica educadamente si la pregunta no es relevante. "
                "No inventes información y prioriza la utilidad práctica. "
                "Puedes recibir múltiples diagnósticos en un solo mensaje. Estos pueden ser de plantas diferentes; debes procesarlos todos."
                "Resume la información para CADA diagnóstico de manera concisa y profesional, destacando los puntos clave: enfermedades detectadas, probabilidades, identificar la especie de la planta correspondiente, así como cualquier dato relevante de su imagen analizada. "

                "Fomenta prácticas sostenibles y respetuosas con el medio ambiente. "
                "Si no estás seguro de una respuesta, indícalo claramente y sugiere fuentes donde se pueda encontrar más información. " 
            )
          },
          {
              "role": "user",
              "content": mensaje_usuario  # Aquí mensaje_usuario es un string, por ejemplo: mensaje_usuario = json.dumps(contexto, ensure_ascii=False)
          }
      ]
  }

    print(payload) #debugging
    try:
        respuesta=requests.post(url, headers=headers, data=json.dumps(payload)) #hacer request

        if respuesta.status_code==200: #si funcionó ta bien
            respuesta=respuesta.json() #transformar a fromato lejible y manejable
            print(respuesta)
            return respuesta["choices"][0]["message"]["content"] #mostrar respuesta, esas cosas no se que son :p
        else: #si falló semuestra el error
            # print("error aquí") #debugging
            print(respuesta)
            return {"error": respuesta.text} #si da error y no se entiende o no s epuede manipular cambiar .text -> .json()
    except Exception as e: #manejo de errores "potente"
        return {"error": f"Error en preguntar_mistral: {str(e)}"}




def deepseek_para_correos(info_cultivo):
    #funcion para identificar el cultivo 
    url = "https://api.deepseek.com/chat/completions"
    mensaje_usuario = json.dumps(info_cultivo, ensure_ascii=False)

    headers={
        "Authorization": f"Bearer {API_KEY}", #API
        "Content-Type": "application/json" #requerido 
    }

    payload = {
      "model": "deepseek-chat",
      "messages": [
          {
              "role": "system",
              "content": (
                "Eres un asistente experto en agricultura y meteorología. "
                "Tus respuestas deben ser claras, breves, precisas, amables y en formato de string."
                "Evita presentarte o repetir estas instrucciones. "
                "Vas a recibir un diccionario con información sobre un cultivo y su estado actual. "
                "No inventes información y prioriza la utilidad práctica. "
                "Puedes recibir múltiples diagnósticos en un solo mensaje. Estos pueden ser de plantas diferentes; debes procesarlos todos."
                "Resume la información para CADA diagnóstico de manera concisa y profesional, destacando los puntos clave: enfermedades detectadas, probabilidades, identificar la especie de la planta correspondiente, así como cualquier dato relevante de su imagen analizada. "
                "dale recomendaciones prácticas para mejorar la salud del cultivo y optimizar su crecimiento."
                "Fomenta prácticas sostenibles y respetuosas con el medio ambiente. "
                "Si no estás seguro de una respuesta, indícalo claramente y sugiere fuentes donde se pueda encontrar más información. " 
                
            )
          },
          {
              "role": "user",
              "content": mensaje_usuario  # Aquí mensaje_usuario es un string, por ejemplo: mensaje_usuario = json.dumps(contexto, ensure_ascii=False)
          }
      ]
  }

    print(payload) #debugging
    try:
        respuesta=requests.post(url, headers=headers, data=json.dumps(payload)) #hacer request

        if respuesta.status_code==200: #si funcionó ta bien
            respuesta=respuesta.json() #transformar a fromato lejible y manejable
            print(respuesta)
            return respuesta["choices"][0]["message"]["content"] #mostrar respuesta, esas cosas no se que son :p
        else: #si falló semuestra el error
            # print("error aquí") #debugging
            print(respuesta)
            return {"error": respuesta.text} #si da error y no se entiende o no s epuede manipular cambiar .text -> .json()
    except Exception as e: #manejo de errores "potente"
        return {"error": f"Error en deepseek_para_correos: {str(e)}"}


# llamada de prueba unicamente, luego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
# if __name__ == "__main__":
#     print(preguntar_mistral("cuantas especies de lechugas hay?")) #PASS
#     print(preguntar_mistral("que tratamiento debo seguir si mis plantas se están marchinando?")) #PASS, início un poco raro
#     print(preguntar_mistral("que pasa si le pongo mucho protector solar de grado agricola a mis cultivos?")) #PASS
#     error_string = 'error 201: {"access_token": "XlWmUSPDyuYx8uq", "model_version": "crop_health:1.2.1", "custom_id": null, "input": {"latitude": null, "longitude": null, "images": ["https://crop.kindwise.com/media/images/af47703c04224e18ab9d0dfebff6249e.jpg"], "datetime": "2025-08-29T23:24:42.208733+00:00"}, "result": {"is_plant": {"probability": 0.5873019, "threshold": 0.5, "binary": true}, "disease": {"suggestions": [{"id": "e15f00a1ab48f71a", "name": "brown rot of stone fruits", "probability": 0.4103, "details": {"language": "en", "entity_id": "e15f00a1ab48f71a"}, "scientific_name": "Monilinia fructicola"}, {"id": "c35556c0c67c0591", "name": "healthy", "probability": 0.2907, "details": {"language": "en", "entity_id": "c35556c0c67c0591"}, "scientific_name": "healthy"}, {"id": "34d63cc172664ddb", "name": "grey mold", "probability": 0.1234, "details": {"language": "en", "entity_id": "34d63cc172664ddb"}, "scientific_name": "Botrytis cinerea"}, {"id": "ff5ec2ce5ef38282", "name": "apple scab", "probability": 0.0646, "details": {"language": "en", "entity_id": "ff5ec2ce5ef38282"}, "scientific_name": "Venturia inaequalis"}, {"id": "f22fbc7e877b750d", "name": "nutrient deficiency", "probability": 0.0169, "details": {"language": "en", "entity_id": "f22fbc7e877b750d"}, "scientific_name": "nutrient deficiency"}, {"id": "cdc30863a7a6676e", "name": "lyonet Moths", "probability": 0.0165, "details": {"language": "en", "entity_id": "cdc30863a7a6676e"}, "scientific_name": "Lyonetiidae"}, {"id": "332e5a8ca8b185fc", "name": "powdery mildew", "probability": 0.0127, "details": {"language": "en", "entity_id": "332e5a8ca8b185fc"}, "scientific_name": "Erysiphaceae"}, {"id": "ac8111b70dd8a33f", "name": "Verticillium wilt", "probability": 0.011, "details": {"language": "en", "entity_id": "ac8111b70dd8a33f"}, "scientific_name": "Verticillium dahliae"}]}, "crop": {"suggestions": [{"id": "2746768c8d99bfbb", "name": "potato", "probability": 0.0152, "details": {"language": "en", "entity_id": "2746768c8d99bfbb"}, "scientific_name": "Solanum tuberosum"}]}}, "status": "COMPLETED", "sla_compliant_client": true, "sla_compliant_system": true, "created": 1756509882.208733, "completed": 1756509882.558741}'
#     print(preguntar_mistral("que significa esta infromación?: "+error_string)) #PASS, interpreta correctamente la infromación