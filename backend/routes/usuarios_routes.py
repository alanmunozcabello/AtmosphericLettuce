from fastapi import APIRouter
from controllers.usuaios_controller import *

router=APIRouter()

@router.get("/usuarios")
def ruta_obtener_usuarios(): #enrutador para obtener los usuarios
    return {"usuarios":obtener_todos_los_usuarios}