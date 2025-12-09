from fastapi import APIRouter, Header, HTTPException
from services.auth_service import verificar_token
from jose import JWTError

router = APIRouter()


@router.get("/api/validar-token")
async def validar_token(authorization: str = Header(None)):
    """
    Valida si el token JWT es válido.
    Retorna el correo del usuario si el token es válido.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token no proporcionado"
        )

    token = authorization.split(" ")[1]

    try:
        # Usar la función existente de jwt_service
        correo = verificar_token(token)

        if not correo:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return {
            "valido": True,
            "correo": correo
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error validando token: {str(e)}"
        )
