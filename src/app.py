from fastapi import FastAPI
from routes import (notificaciones_routes, usuarios_routes, clima_routes,
                    chat_routes, auth_routes, recuperacion_routes)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from tasks.scheduler import start_scheduler
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


app = FastAPI()

# ========== MIDDLEWARE PARA DESHABILITAR CACHE ==========
class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Aplicar a todas las páginas HTML
        if request.url.path.endswith('.html') or request.url.path == '/':
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
            
            # ✅ Headers adicionales para deshabilitar bfcache
            response.headers['Clear-Site-Data'] = '"cache"'
        
        return response


app.add_middleware(NoCacheMiddleware)

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
app.include_router(auth_routes.router)
app.include_router(recuperacion_routes.router)


# # Montar carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


# Iniciar scheduler de tareas
@app.on_event("startup")
def startup_event():
    start_scheduler()


# Comandos útiles:
# Iniciar servidor: python -m uvicorn app:app --reload
# Iniciar servidor LAN público:
#     python -m uvicorn app:app --host 0.0.0.0 --port 8000
# Abrir chatbot:
#     http://127.0.0.1:8000/static/chat_bot/chat_bot.html
# Migrar datos: python scripts\migracion_sqlite.py
# Consulta directa:
#     python scripts\consultas_sqlite.py --query
#     "SELECT * FROM usuarios WHERE ciudad IS NOT NULL"

# pruebas unitarias
# todos los tets: pytest ../tests/ -v
# para ver los print durante la ejecucion: pytest ../tests/ -v -s
# todos los tests de routes: pytest ../tests/routes/ -v
# todos los tests de controllers: pytest ../tests/controllers/ -v
# todos los tests de services: pytest ../tests/services/ -v
