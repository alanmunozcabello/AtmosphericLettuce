from fastapi import APIRouter
from services.chat_service import procesar_consulta

router = APIRouter()


@router.post("/chat/consulta")
def hacer_consulta(payload: dict):
    return {"respuesta": procesar_consulta(payload)}