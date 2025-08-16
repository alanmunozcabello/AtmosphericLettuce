from fastapi import FastAPI
from routes import usuarios_routes

app = FastAPI()
app.include_router(usuarios_routes.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API"}

@app.get("/ping")
def hacer_ping():
    return {"mensaje": "pong"}

#iniciar servidor: python -m uvicorn app:app --reload