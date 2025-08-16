from fastapi import FastAPI
from routes import usuarios_routes

aplication= FastAPI()
aplication.include_router(usuarios_routes.router) #usar las rutas de los usuarios

@aplication.get("/ping")
def hacer_ping():
    return {"mensaje":"pong"}

# @aplication.get("/usuarios")
# def obtener_lista_usuarios():
#     return 