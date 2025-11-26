from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from services.jwt_service import crear_token
from middleware.autenticacion_mw import verificar_autenticacion
from middleware.permisos_mw import verificar_propietario
from services.usuarios_service import (
    service_leer_usuarios,
    service_registrar_usuario,
    service_obtener_usuario_para_frontend,
    service_obtener_cultivos_usuario,
    service_eliminar_cultivo,
    service_modificar_usuario,
    service_modificar_ubicacion_usuario,
    service_iniciar_sesion,
    service_modificar_region_ciudad_usuario,
    service_eliminar_usuario,
    service_agregar_cultivo,
    service_modificar_formulario_cultivo,
    service_modificar_area_cultivo,
    service_modificar_notificaciones_usuario,
    service_filtrar_cultivos,
)


router = APIRouter()


# "pagina inicial"
@router.get("/")
def root():
    # ----------------front
    return {"mensaje": "Bienvenido a la API"}


# test de mensaje
@router.get("/ping")
def hacer_ping():
    # ----------------front
    return {"mensaje": "pong"}


# get es para dar información
@router.get("/usuarios")
def ruta_obtener_usuarios():
    # enrutador para obtener los usuarios y mostrarlos
    # ----------------front
    return service_leer_usuarios()


# usar {correo} hace que automaticamente se ponga el correo
# que venga en la url como parametro para la funcion!!! :O
# get es para dar información
@router.get("/usuarios/{correo}")
def ruta_obtener_usuario(
    correo: str,
    correo_token: str = Depends(verificar_autenticacion),
):
    # enrutador para obtener la informacion de un usuario
    # ----------------front
    verificar_propietario(correo, correo_token)
    return service_obtener_usuario_para_frontend(correo)


# funcion no tan necesaria, el frontend puede saltarse esta
# y llamar directamente a ruta_obtener_usuario(correo)
# ver como seria cuando se vaya a usar coso de java token coso
@router.get("/usuarios/iniciar_sesion/{correo}/{contrasena}")
def ruta_iniciar_sesion(correo, contrasena):
    resultado =  service_iniciar_sesion(correo, contrasena)
    
    if "error" in resultado:
        return resultado
    
    token = crear_token(correo)
    
    return {
        **resultado,
        "token": token
    }


class UsuarioRegistro(BaseModel):
    correo: str
    nombre: str
    contrasena: str


@router.post("/usuarios/registrar")
def ruta_registrar_usuario(usuario: UsuarioRegistro):
    return service_registrar_usuario(
        usuario.correo,
        usuario.nombre,
        usuario.contrasena
    )


@router.get("/usuarios/{correo}/cultivos")
def ruta_obtener_cultivos_usuario(
    correo: str,
    pagina: int = 1,
    limite: int = 20
):
    """
    Obtener cultivos de un usuario con paginación
    
    Parámetros:
    - correo: Email del usuario
    - pagina: Número de página (default: 1)
    - limite: Cantidad de resultados por página (default: 20, máx: 100)
    
    Retorna:
    {
        "cultivos": [...],
        "paginacion": {
            "pagina_actual": 1,
            "limite": 20,
            "total": 45,
            "total_paginas": 3,
            "tiene_siguiente": true,
            "tiene_anterior": false
        }
    }
    """
    return service_obtener_cultivos_usuario(correo, pagina, limite)


class CultivoCreate(BaseModel):
    nombre_cultivo: str
    hectareas: int


# post para agregar
@router.post("/usuarios/{correo}/agregar_cultivo")
def ruta_agregar_cultivo(correo: str, cultivo: CultivoCreate):
    return service_agregar_cultivo(
        correo, cultivo.nombre_cultivo, cultivo.hectareas)


class CultivoDatos(BaseModel):
    nombre_cultivo: str
    hectareas: Optional[float]
    fecha_siembra: Optional[str]
    notas: Optional[str]
    etapa_planta: Optional[str]
    tipo_riego: Optional[str]
    ultimo_riego: Optional[str]  # datetime como string
    frecuencia_riego: Optional[str]
    humedad_suelo: Optional[str]
    textura_suelo: Optional[str]
    variedad_planta: Optional[str]
    estado_planta: Optional[str]
    estres_hidrico: Optional[int]  # boolean: 0=No, 1=Sí
    profundidad_radical: Optional[int]
    densidad_plantacion: Optional[int]
    tipo_sensor: Optional[str]
    eficiencia_riego: Optional[float]  # decimal
    caudal: Optional[float]  # decimal
    ph_agua: Optional[float]  # decimal
    acolchado: Optional[int]  # boolean: 0=No, 1=Sí


# patch para modificar
@router.patch(
    "/usuarios/{correo}/cultivos/modificar_formulario_cultivo"
)
def ruta_modificar_formulario_cultivo(
    correo: str,
    cultivo_datos: CultivoDatos
):
    return service_modificar_formulario_cultivo(correo, cultivo_datos)


class PuntoCoordenada(BaseModel):
    latitud: Optional[float]
    longitud: Optional[float]


class AreaCultivoDatos(BaseModel):
    cultivo: str
    area: float
    puntos: list[Optional[PuntoCoordenada]]


# patch para modificar
@router.patch(
    "/usuarios/{correo}/cultivo/modificar_area_cultivo"
)
def ruta_modificar_area_cultivo(
    correo: str,
    area_datos: AreaCultivoDatos
):
    return service_modificar_area_cultivo(correo, area_datos)


# delete para borrar
@router.delete("/usuarios/{correo}/{cultivo}/eliminar")
def ruta_eliminar_cultivo(correo, cultivo):
    return service_eliminar_cultivo(correo, cultivo)

class UsuarioModificado(BaseModel):
    # correo: str
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    region: Optional[str] = None
    foto_perfil: Optional[str] = None


# HAY QUE CAMBIAR TODITO EL COSIACO
@router.put("/usuarios/{correo}/modificar")
def ruta_modificar_usuario(
    correo: str,
    usuarioMOD: UsuarioModificado,
    correo_token: str = Depends(verificar_autenticacion)
):
    verificar_propietario(correo, correo_token) 
    # usuarioMOD es el dict completo del usuario a modificar
    return service_modificar_usuario(correo, usuarioMOD)


@router.patch("/usuarios/{correo}/ubicacion/{lat}/{lon}/modificar")
def ruta_modificar_ubicacion_usuario(correo, lat, lon):
    # lat y lon pueden ser pasados como string sin problema
    return service_modificar_ubicacion_usuario(correo, lat, lon)


@router.patch(
    "/usuarios/{correo}/ubicacion/region/{region}/{ciudad}/modificar"
)
def ruta_modificar_region_ciudad_usuario(correo, region, ciudad):
    return service_modificar_region_ciudad_usuario(
        correo, region, ciudad
    )


@router.delete("/usuarios/{correo}")
def ruta_eliminar_usuario(correo):
    return service_eliminar_usuario(correo)


@router.patch(
    "/usuarios/{correo}/modificar_notificaciones/{notificaciones}"
)
def ruta_modificar_notificaciones_usuario(
    correo,
    notificaciones: bool
):
    return service_modificar_notificaciones_usuario(
        correo, notificaciones
    )


@router.get("/cultivos/filtrar")
def ruta_filtrar_cultivos(
    correo: Optional[str] = None,
    buscar: Optional[str] = None,
    etapa_planta: Optional[str] = None,
    fecha_siembra_desde: Optional[str] = None,
    fecha_siembra_hasta: Optional[str] = None,
    estado_planta: Optional[str] = None,
    tipo_riego: Optional[str] = None,
    tiene_area: Optional[bool] = None,
    tiene_formulario: Optional[bool] = None,
    ordenar_por: str = "nombre_cultivo",
    orden: str = "ASC",
    pagina: int = 1,
    limite: int = 20
):
    """
    Endpoint para filtrar cultivos con múltiples criterios

    Ejemplos de uso:
    - /cultivos/filtrar?correo=user@mail.com
    - /cultivos/filtrar?buscar=tomate&pagina=1&limite=10
    - /cultivos/filtrar?etapa_planta=cosecha&tipo_riego=goteo
    - /cultivos/filtrar?fecha_siembra_desde=2025-01-01&fecha_siembra_hasta=2025-03-31
    - /cultivos/filtrar?tiene_area=true&ordenar_por=hectareas&orden=DESC
    """
    return service_filtrar_cultivos(
        correo=correo,
        buscar=buscar,
        etapa_planta=etapa_planta,
        fecha_siembra_desde=fecha_siembra_desde,
        fecha_siembra_hasta=fecha_siembra_hasta,
        estado_planta=estado_planta,
        tipo_riego=tipo_riego,
        tiene_area=tiene_area,
        tiene_formulario=tiene_formulario,
        ordenar_por=ordenar_por,
        orden=orden,
        pagina=pagina,
        limite=limite
    )
