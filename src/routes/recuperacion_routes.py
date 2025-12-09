
from fastapi import APIRouter, HTTPException
from services.auth_service import generar_codigo_recuperacion, verificar_codigo, cambiar_contrasena_recuperacion
from models.recuperacion import SolicitudRecuperacion, VerificacionCodigo, CambioContrasena

router = APIRouter(prefix="/api/recuperacion", tags=["Recuperación de Contraseña"])


@router.post("/solicitar")
def solicitar_recuperacion(solicitud: SolicitudRecuperacion):
    resultado = generar_codigo_recuperacion(solicitud.correo)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado


@router.post("/verificar")
def verificar_codigo_endpoint(verificacion: VerificacionCodigo):
    resultado = verificar_codigo(verificacion.correo, verificacion.codigo)
    if not resultado["valid"]:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return {"mensaje": "Código válido"}


@router.post("/cambiar")
def cambiar_contrasena_endpoint(cambio: CambioContrasena):
    resultado = cambiar_contrasena_recuperacion(cambio.correo, cambio.codigo, cambio.nueva_contrasena)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado
