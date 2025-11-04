from fastapi import APIRouter
from controllers.chat_controllers import consultar

router = APIRouter()


@router.post("/chat/consulta")
def hacer_consulta(payload: dict):
    return {"respuesta": consultar(payload)}
