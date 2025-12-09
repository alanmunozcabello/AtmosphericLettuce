from fastapi import Header, HTTPException
from services.auth_service import verificar_token

def verificar_autenticacion(authorization: str = Header(None)):
    """
    Verifica autenticación mediante header Authorization: Bearer {token}
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token no proporcionado"
        )
    
    try:
        # Esperamos formato: "Bearer {token}"
        parts = authorization.split()
        
        if len(parts) != 2:
            raise HTTPException(
                status_code=401,
                detail="Formato incorrecto. Use: Bearer {token}"
            )
        
        scheme, token = parts
        
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Esquema inválido. Use: Bearer {token}"
            )
        
        # Verificar token
        correo = verificar_token(token)
        if not correo:
            raise HTTPException(
                status_code=401,
                detail="Token inválido o expirado"
            )
        
        return correo
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error validando token: {str(e)}"
        )
