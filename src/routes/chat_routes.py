from fastapi import APIRouter
from services.chat_service import procesar_consulta
from models import ChatConsulta

router = APIRouter()


@router.post("/chat/consulta")
def hacer_consulta(payload: ChatConsulta):
    # Convertir a dict para mantener compatibilidad con chat_service
    return {
        "respuesta": procesar_consulta(
            payload.model_dump(exclude_none=True)
        )
    }
