from fastapi import APIRouter
from controllers.usuarios_controller import obtener_todos_los_usuarios

router=APIRouter()

@router.get("/usuarios")
def ruta_obtener_usuarios(): #enrutador para obtener los usuarios
    return {"usuarios":obtener_todos_los_usuarios()}