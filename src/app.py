from fastapi import FastAPI
from routes import usuarios_routes, clima_routes, chat_routes
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(usuarios_routes.router)
app.include_router(clima_routes.router)
app.include_router(chat_routes.router)

# # Montar carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

#iniciar servidor: python -m uvicorn app:app --reload
#iniciar servidor LAN publico: python -m uvicorn app:app --host 0.0.0.0 --port 8000
