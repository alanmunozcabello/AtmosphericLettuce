from fastapi import Header, HTTPException
from services.jwt_service import verificar_token

def verificar_autenticacion(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token no proporcionado"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Esquema inválido. Use: Bearer {token}"
            )
        
        correo = verificar_token(token)
        if not correo:
            raise HTTPException(
                status_code=401,
                detail="Token inválido o expirado"
            )
        
        return correo
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Formato incorrecto. Use: Bearer {token}"
        )