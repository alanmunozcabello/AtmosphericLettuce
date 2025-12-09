from fastapi import APIRouter, Depends
from middleware.autenticacion_mw import verificar_autenticacion
from services.ai_integration_service import procesar_consulta_chat
from models import ChatConsulta

router = APIRouter()


@router.post("/chat/consulta")
def hacer_consulta(
    payload: ChatConsulta,
    correo_token: str = Depends(verificar_autenticacion)
):
    # Convertir a dict para mantener compatibilidad con chat_service
    return {
        "respuesta": procesar_consulta_chat(
            payload.model_dump(exclude_none=True)
        )
    }
