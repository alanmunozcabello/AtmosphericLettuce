from fastapi import FastAPI
from routes import  notificaciones_routes, usuarios_routes, clima_routes, chat_routes #, notificaciones_routes
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para pruebas locales; luego puedes restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_routes.router)
app.include_router(clima_routes.router)
app.include_router(chat_routes.router)
app.include_router(notificaciones_routes.router)


# # Montar carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

#iniciar servidor: python -m uvicorn app:app --reload
#iniciar servidor LAN publico: python -m uvicorn app:app --host 0.0.0.0 --port 8000
#para abrir el chatbot una vez el servidor esté andando: http://127.0.0.1:8000/static/chat_bot/chat_bot.html