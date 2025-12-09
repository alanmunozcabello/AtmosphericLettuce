from fastapi import APIRouter, Depends
from middleware.autenticacion_mw import verificar_autenticacion
from services.chat_service import procesar_consulta
from models import ChatConsulta

router = APIRouter()


@router.post("/chat/consulta")
def hacer_consulta(
    payload: ChatConsulta,
    correo_token: str = Depends(verificar_autenticacion)
):
    # Convertir a dict para mantener compatibilidad con chat_service
    return {
        "respuesta": procesar_consulta(
            payload.model_dump(exclude_none=True)
        )
    }
