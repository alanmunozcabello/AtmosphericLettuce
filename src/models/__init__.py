"""
Modelos Pydantic para validación de datos en AtmosphericLettuce
"""

from .usuario import (
    LoginRequest,
    UsuarioRegistro,
    UsuarioModificado,
    UsuarioResponse,
    Coordenadas,
    NotificacionesConfig,
    UbicacionUsuario
)

from .cultivo import (
    CultivoCreate,
    CultivoDatos,
    AreaCultivoDatos,
    PuntoCoordenada,
    EtapaPlanta,
    TipoRiego,
    TexturaSuelo,
    TipoSensor
)

from .chat import ChatConsulta
from .clima import ClimaRequest

__all__ = [
    # Usuario models
    "LoginRequest",
    "UsuarioRegistro",
    "UsuarioModificado",
    "UsuarioResponse",
    "Coordenadas",
    "NotificacionesConfig",
    
    # Cultivo models
    "CultivoCreate",
    "CultivoDatos",
    "AreaCultivoDatos",
    "PuntoCoordenada",
    
    # Enums
    "EtapaPlanta",
    "TipoRiego",
    "TexturaSuelo",
    "TipoSensor",
    
    # Chat models
    "ChatConsulta",
    
    # Clima models
    "ClimaRequest",
]
