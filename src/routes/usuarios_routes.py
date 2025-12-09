from fastapi import APIRouter, Depends, Path
from fastapi.responses import FileResponse
from typing import Optional
from services.auth_service import crear_token
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
    service_obtener_nombres_cultivos,
)
from models import (
    LoginRequest,
    UsuarioRegistro,
    UsuarioModificado,
    CultivoCreate,
    CultivoDatos,
    AreaCultivoDatos,
)


router = APIRouter()


# "pagina inicial" - Servir landing page
@router.get("/")
def root():
    return FileResponse("static/web/landing.html")


# test de mensaje
@router.get("/ping")
def hacer_ping():
    # ----------------front
    return {"mensaje": "pong"}


# get es para dar información
@router.get("/usuarios")
def ruta_obtener_usuarios(
    correo_token: str = Depends(verificar_autenticacion)
):
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


# Endpoint GET para el frontend (menos seguro pero compatible)
@router.get("/usuarios/iniciar_sesion/{correo}/{contrasena}")
def ruta_iniciar_sesion_get(correo: str, contrasena: str):
    """Endpoint sin autenticación para login"""
    resultado = service_iniciar_sesion(correo, contrasena)

    if "error" in resultado:
        return resultado

    token = crear_token(correo)

    return {
        **resultado,
        "token": token
    }


# Endpoint POST (más seguro, para uso futuro)
@router.post("/usuarios/login")
def ruta_iniciar_sesion(credenciales: LoginRequest):
    resultado = service_iniciar_sesion(
        credenciales.correo, credenciales.contrasena
    )

    if "error" in resultado:
        return resultado

    token = crear_token(credenciales.correo)

    return {
        **resultado,
        "token": token
    }


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
    correo_token: str = Depends(verificar_autenticacion),
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
    verificar_propietario(correo, correo_token)
    return service_obtener_cultivos_usuario(correo, pagina, limite)


@router.get("/usuarios/{correo}/cultivos/nombres")
def ruta_obtener_nombres_cultivos(
    correo: str,
    correo_token: str = Depends(verificar_autenticacion)
):
    """
    Endpoint ligero para obtener solo nombres de cultivos.
    Ideal para selectores y autocompletado.
    """
    verificar_propietario(correo, correo_token)
    return service_obtener_nombres_cultivos(correo)


# post para agregar
@router.post("/usuarios/{correo}/agregar_cultivo")
def ruta_agregar_cultivo(
    correo: str,
    cultivo: CultivoCreate,
    correo_token: str = Depends(verificar_autenticacion)
):
    verificar_propietario(correo, correo_token)
    return service_agregar_cultivo(
        correo, cultivo.nombre_cultivo, cultivo.hectareas)


# patch para modificar
@router.patch(
    "/usuarios/{correo}/cultivos/modificar_formulario_cultivo"
)
def ruta_modificar_formulario_cultivo(
    correo: str,
    cultivo_datos: CultivoDatos,
    correo_token: str = Depends(verificar_autenticacion)
):
    # Convertir Pydantic a dict para el service
    verificar_propietario(correo, correo_token)
    cultivo_dict = cultivo_datos.model_dump(exclude_unset=True)
    return service_modificar_formulario_cultivo(correo, cultivo_dict)


# patch para modificar
@router.patch(
    "/usuarios/{correo}/cultivo/modificar_area_cultivo"
)
def ruta_modificar_area_cultivo(
    correo: str,
    area_datos: AreaCultivoDatos,
    correo_token: str = Depends(verificar_autenticacion)
):
    # Convertir Pydantic a dict para el service
    verificar_propietario(correo, correo_token)
    area_dict = area_datos.model_dump()
    return service_modificar_area_cultivo(correo, area_dict)


# delete para borrar
@router.delete("/usuarios/{correo}/{cultivo}/eliminar")
def ruta_eliminar_cultivo(
    correo,
    cultivo,
    correo_token: str = Depends(verificar_autenticacion)
):
    verificar_propietario(correo, correo_token)
    return service_eliminar_cultivo(correo, cultivo)


# HAY QUE CAMBIAR TODITO EL COSIACO
@router.put("/usuarios/{correo}/modificar")
def ruta_modificar_usuario(
    correo: str,
    usuarioMOD: UsuarioModificado,
    correo_token: str = Depends(verificar_autenticacion)
):
    verificar_propietario(correo, correo_token)
    # Convertir Pydantic a dict para el service
    usuario_dict = usuarioMOD.model_dump(exclude_unset=True)
    return service_modificar_usuario(correo, usuario_dict)
    # usuarioMOD es el dict completo del usuario a modificar
    return service_modificar_usuario(correo, usuarioMOD)


@router.patch("/usuarios/{correo}/ubicacion/{lat}/{lon}/modificar")
def ruta_modificar_ubicacion_usuario(
    correo: str,
    lat: float = Path(..., ge=-90, le=90, description="Latitud"),
    lon: float = Path(..., ge=-180, le=180, description="Longitud"),
    correo_token: str = Depends(verificar_autenticacion)
):
    verificar_propietario(correo, correo_token)
    return service_modificar_ubicacion_usuario(correo, lat, lon)


@router.patch(
    "/usuarios/{correo}/ubicacion/region/{region}/{ciudad}/modificar"
)
def ruta_modificar_region_ciudad_usuario(
    correo,
    region,
    ciudad,
    correo_token: str = Depends(verificar_autenticacion)
):
    verificar_propietario(correo, correo_token)
    return service_modificar_region_ciudad_usuario(
        correo, region, ciudad
    )


@router.delete("/usuarios/{correo}")
def ruta_eliminar_usuario(
    correo,
    correo_token: str = Depends(verificar_autenticacion)
):
    verificar_propietario(correo, correo_token)
    return service_eliminar_usuario(correo)


@router.patch(
    "/usuarios/{correo}/modificar_notificaciones/{notificaciones}"
)
def ruta_modificar_notificaciones_usuario(
    correo,
    notificaciones: bool,
    correo_token: str = Depends(verificar_autenticacion)
):
    verificar_propietario(correo, correo_token)
    return service_modificar_notificaciones_usuario(
        correo, notificaciones
    )


@router.get("/cultivos/filtrar")
def ruta_filtrar_cultivos(
    correo_token: str = Depends(verificar_autenticacion),
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
    - /cultivos/filtrar?fecha_siembra_desde=2025-01-01&\
fecha_siembra_hasta=2025-03-31
    - /cultivos/filtrar?tiene_area=true&\
ordenar_por=hectareas&orden=DESC
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
