import requests
import json
from dotenv import load_dotenv
import os
# prueba de respuesta de la API
# OBS: funciona bien, usa bien el contexto y responde coherentemente. dependiendo de la complegidad de la pregunta tarda minimo 2 segundos en dar una repsuesta.
#      Lo que si la IA no recuerda preguntas anteriores, solo responde a la actual. 

load_dotenv()
API_KEY=os.getenv("OPENROUTER_MISTRAL_API_KEY")

def preguntar_mistral(pregunta):
    url = "https://openrouter.ai/api/v1/chat/completions" #url generico de openrouter

    headers={
        "Authorization": f"Bearer {API_KEY}", #API
        "Content-Type": "application/json" #requerido 
    }

    payload = {
        "model": "mistralai/mistral-small-3.2-24b-instruct:free", #end point del modelo
        "messages": [
            {"role": "system", "content": "Eres un asistente especializado en agricultura y meteorología, que respuestas sean cortas y no ambiguas de ser posible."}, #contexto para la IA
            {"role": "user", "content": pregunta} #pregunta del usuario (podriamos hacer algo con el rol, en vez de usuario que sea la pega que espesificó el usuario en su perfil)
        ]
    }
    try:
        respuesta=requests.post(url, headers=headers, json=payload) #hacer request

        if respuesta.status_code==200: #si funcionó ta bien
            respuesta=respuesta.json() #transformar a fromato lejible y manejable
            return respuesta["choices"][0]["message"]["content"] #mostrar respuesta, esas cosas no se que son :p
        else: #si falló semuestra el error
            return f"error {respuesta.status_code}: {respuesta.text}"
    except Exception as e: #manejo de errores "potente"
        return "error", e

# llamada de prueba unicamenteluego se llamará desde las capas
# sin el __name__ == "__main__" no funcionaba
if __name__ == "__main__":
    print(preguntar_mistral("cuantas especies de lechugas hay?")) #PASS
    print(preguntar_mistral("que tratamiento debo seguir si mis plantas se están marchinando?")) #PASS, início un poco raro
    print(preguntar_mistral("que pasa si le pongo mucho protector solar de grado agricola a mis cultivos?")) #PASS
    error_string = 'error 201: {"access_token": "XlWmUSPDyuYx8uq", "model_version": "crop_health:1.2.1", "custom_id": null, "input": {"latitude": null, "longitude": null, "images": ["https://crop.kindwise.com/media/images/af47703c04224e18ab9d0dfebff6249e.jpg"], "datetime": "2025-08-29T23:24:42.208733+00:00"}, "result": {"is_plant": {"probability": 0.5873019, "threshold": 0.5, "binary": true}, "disease": {"suggestions": [{"id": "e15f00a1ab48f71a", "name": "brown rot of stone fruits", "probability": 0.4103, "details": {"language": "en", "entity_id": "e15f00a1ab48f71a"}, "scientific_name": "Monilinia fructicola"}, {"id": "c35556c0c67c0591", "name": "healthy", "probability": 0.2907, "details": {"language": "en", "entity_id": "c35556c0c67c0591"}, "scientific_name": "healthy"}, {"id": "34d63cc172664ddb", "name": "grey mold", "probability": 0.1234, "details": {"language": "en", "entity_id": "34d63cc172664ddb"}, "scientific_name": "Botrytis cinerea"}, {"id": "ff5ec2ce5ef38282", "name": "apple scab", "probability": 0.0646, "details": {"language": "en", "entity_id": "ff5ec2ce5ef38282"}, "scientific_name": "Venturia inaequalis"}, {"id": "f22fbc7e877b750d", "name": "nutrient deficiency", "probability": 0.0169, "details": {"language": "en", "entity_id": "f22fbc7e877b750d"}, "scientific_name": "nutrient deficiency"}, {"id": "cdc30863a7a6676e", "name": "lyonet Moths", "probability": 0.0165, "details": {"language": "en", "entity_id": "cdc30863a7a6676e"}, "scientific_name": "Lyonetiidae"}, {"id": "332e5a8ca8b185fc", "name": "powdery mildew", "probability": 0.0127, "details": {"language": "en", "entity_id": "332e5a8ca8b185fc"}, "scientific_name": "Erysiphaceae"}, {"id": "ac8111b70dd8a33f", "name": "Verticillium wilt", "probability": 0.011, "details": {"language": "en", "entity_id": "ac8111b70dd8a33f"}, "scientific_name": "Verticillium dahliae"}]}, "crop": {"suggestions": [{"id": "2746768c8d99bfbb", "name": "potato", "probability": 0.0152, "details": {"language": "en", "entity_id": "2746768c8d99bfbb"}, "scientific_name": "Solanum tuberosum"}]}}, "status": "COMPLETED", "sla_compliant_client": true, "sla_compliant_system": true, "created": 1756509882.208733, "completed": 1756509882.558741}'
    print(preguntar_mistral("que significa esta infromación?: "+error_string)) #PASS, interpreta correctamente la infromación