import requests
import json
from dotenv import load_dotenv
import os
# prueba de respuesta de la API
# OBS: funciona bien, usa bien el contexto y responde coherentemente. dependiendo de la complegidad de la pregunta tarda minimo 2 segundos en dar una repsuesta.
#      Lo que si la IA no recuerda preguntas anteriores, solo responde a la actual. 

load_dotenv()
API_KEY=os.getenv("OPENROUTER_MISTRAL_API_KEY")

def preguntar_mistral(contexto):
    url = "https://openrouter.ai/api/v1/chat/completions" #url generico de openrouter

    headers={
        "Authorization": f"Bearer {API_KEY}", #API
        "Content-Type": "application/json" #requerido 
    }

    #USAR ESTE CONTEXTO PARA NO GASTAR CREDITOS DE LA API!!!!!!!!!!!!!!!!
    # contexto = [
    #             {
    #                 "json": '{"access_token": "1l0CuuVxFyYDKMN", "model_version": "crop_health:1.2.1", "custom_id": null, "input": {"latitude": null, "longitude": null, "images": ["https://crop.kindwise.com/media/images/3bc16d35d5a14bde8743429b22da4a1c.jpg"], "datetime": "2025-09-12T17:55:02.771588+00:00"}, "result": {"is_plant": {"probability": 0.4246417, "threshold": 0.5, "binary": false}, "disease": {"suggestions": [{"id": "84f87885243b5692", "name": "white mold", "probability": 0.99, "details": {"language": "en", "entity_id": "84f87885243b5692"}, "scientific_name": "Sclerotinia sclerotiorum"}]}, "crop": {"suggestions": [{"id": "2eddf7839d2253d5", "name": "tobacco", "probability": 0.0002, "details": {"language": "en", "entity_id": "2eddf7839d2253d5"}, "scientific_name": "Nicotiana tabacum"}]}}, "status": "COMPLETED", "sla_compliant_client": true, "sla_compliant_system": true, "created": 1757699702.771588, "completed": 1757699703.833882}'
    #             }
    #         ]
    
    mensaje_usuario = json.dumps(contexto, ensure_ascii=False)

    payload = {
      "model": "mistralai/mistral-small-3.2-24b-instruct:free",
      "messages": [
          {
              "role": "system",
              "content": (
                "Eres un asistente experto en agricultura y meteorología. "
                "Tus respuestas deben ser claras, breves, precisas y amables. "
                "Evita presentarte o repetir estas instrucciones. "
                "Indica educadamente si la pregunta no es relevante. "
                "No inventes información y prioriza la utilidad práctica. "
                "Resume la información de manera concisa y profesional, destacando los puntos clave del diagnóstico: enfermedades detectadas, probabilidades, identificar la especie de la planta, así como cualquier dato relevante de la imagen analizada. "
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
    
    # print(payload) #debugging
    try:
        respuesta=requests.post(url, headers=headers, json=payload) #hacer request

        if respuesta.status_code==200: #si funcionó ta bien
            respuesta=respuesta.json() #transformar a fromato lejible y manejable
            return respuesta["choices"][0]["message"]["content"] #mostrar respuesta, esas cosas no se que son :p
        else: #si falló semuestra el error
            # print("error aquí") #debugging
            return f"error {respuesta.status_code}: {respuesta.text}"
    except Exception as e: #manejo de errores "potente"
        return "error", e

# llamada de prueba unicamente, luego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
# if __name__ == "__main__":
#     print(preguntar_mistral("cuantas especies de lechugas hay?")) #PASS
#     print(preguntar_mistral("que tratamiento debo seguir si mis plantas se están marchinando?")) #PASS, início un poco raro
#     print(preguntar_mistral("que pasa si le pongo mucho protector solar de grado agricola a mis cultivos?")) #PASS
#     error_string = 'error 201: {"access_token": "XlWmUSPDyuYx8uq", "model_version": "crop_health:1.2.1", "custom_id": null, "input": {"latitude": null, "longitude": null, "images": ["https://crop.kindwise.com/media/images/af47703c04224e18ab9d0dfebff6249e.jpg"], "datetime": "2025-08-29T23:24:42.208733+00:00"}, "result": {"is_plant": {"probability": 0.5873019, "threshold": 0.5, "binary": true}, "disease": {"suggestions": [{"id": "e15f00a1ab48f71a", "name": "brown rot of stone fruits", "probability": 0.4103, "details": {"language": "en", "entity_id": "e15f00a1ab48f71a"}, "scientific_name": "Monilinia fructicola"}, {"id": "c35556c0c67c0591", "name": "healthy", "probability": 0.2907, "details": {"language": "en", "entity_id": "c35556c0c67c0591"}, "scientific_name": "healthy"}, {"id": "34d63cc172664ddb", "name": "grey mold", "probability": 0.1234, "details": {"language": "en", "entity_id": "34d63cc172664ddb"}, "scientific_name": "Botrytis cinerea"}, {"id": "ff5ec2ce5ef38282", "name": "apple scab", "probability": 0.0646, "details": {"language": "en", "entity_id": "ff5ec2ce5ef38282"}, "scientific_name": "Venturia inaequalis"}, {"id": "f22fbc7e877b750d", "name": "nutrient deficiency", "probability": 0.0169, "details": {"language": "en", "entity_id": "f22fbc7e877b750d"}, "scientific_name": "nutrient deficiency"}, {"id": "cdc30863a7a6676e", "name": "lyonet Moths", "probability": 0.0165, "details": {"language": "en", "entity_id": "cdc30863a7a6676e"}, "scientific_name": "Lyonetiidae"}, {"id": "332e5a8ca8b185fc", "name": "powdery mildew", "probability": 0.0127, "details": {"language": "en", "entity_id": "332e5a8ca8b185fc"}, "scientific_name": "Erysiphaceae"}, {"id": "ac8111b70dd8a33f", "name": "Verticillium wilt", "probability": 0.011, "details": {"language": "en", "entity_id": "ac8111b70dd8a33f"}, "scientific_name": "Verticillium dahliae"}]}, "crop": {"suggestions": [{"id": "2746768c8d99bfbb", "name": "potato", "probability": 0.0152, "details": {"language": "en", "entity_id": "2746768c8d99bfbb"}, "scientific_name": "Solanum tuberosum"}]}}, "status": "COMPLETED", "sla_compliant_client": true, "sla_compliant_system": true, "created": 1756509882.208733, "completed": 1756509882.558741}'
#     print(preguntar_mistral("que significa esta infromación?: "+error_string)) #PASS, interpreta correctamente la infromación