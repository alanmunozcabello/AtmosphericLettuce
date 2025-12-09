from fastapi import HTTPException


def verificar_propietario(correo_url: str, correo_token: str):
    if correo_url.lower() != correo_token.lower():
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a este recurso"
        )
    return True
