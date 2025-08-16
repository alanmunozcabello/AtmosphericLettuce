from fastapi import FastAPI
from routes import usuarios_routes

app = FastAPI()
app.include_router(usuarios_routes.router)

#iniciar servidor: python -m uvicorn app:app --reload