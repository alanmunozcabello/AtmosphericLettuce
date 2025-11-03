from fastapi import APIRouter
from controllers.usuarios_controller import controller_obtener_todos_los_usuarios, controller_obtener_usuario, controller_registrar_usuario, controller_obtener_cultivos_usuario, controller_eliminar_cultivo, controller_iniciar_sesion, controller_modificar_usuario, controller_modificar_ubicacion_usuario, controller_modificar_region_ciudad_usuario, controller_eliminar_usuario, controller_agregar_cultivo, controller_modificar_formulario_cultivo, controller_modificar_area_cultivo,controller_modificar_notificaciones_usuario
from pydantic import BaseModel
from typing import Optional

router=APIRouter()

@router.get("/") #"pagina inicial"
def root():
    return {"mensaje": "Bienvenido a la API"} #----------------front

@router.get("/ping") #test de mensaje
def hacer_ping():
    return {"mensaje": "pong"} #----------------front

@router.get("/usuarios") #get es para dar información
def ruta_obtener_usuarios(): #enrutador para obtener los usuarios y mostrarlos
    return controller_obtener_todos_los_usuarios() #----------------front

#usar {correo} hace que automaticamente se ponga el correo que venga en la url como parametro para para la funcion!!! :O
@router.get("/usuarios/{correo}") #get es para dar información
def ruta_obtener_usuario(correo): #enrutador para obtener la informacion de un usuario
    return controller_obtener_usuario(correo) #----------------front

#funcion no tan necesaria, el frontend puede saltarse esta y llamar directamente a ruta_obtener_usuario(correo) -> ver como seria cuando se vaya a usar coso de java token coso
@router.get("/usuarios/iniciar_sesion/{correo}/{contrasena}")
def ruta_iniciar_sesion(correo, contrasena):
    return controller_iniciar_sesion(correo, contrasena)

class UsuarioRegistro(BaseModel):
    correo: str
    nombre: str
    contrasena: str

@router.post("/usuarios/registrar")
def ruta_registrar_usuario(usuario: UsuarioRegistro):
    return controller_registrar_usuario(usuario.correo, usuario.nombre, usuario.contrasena)

@router.get("/usuarios/{correo}/cultivos")
def ruta_obtener_cultivos_usuario(correo):
    return controller_obtener_cultivos_usuario(correo)

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
    estres_hidrico: Optional[int] # boolean: 0=No, 1=Sí
    profundidad_radical: Optional[int]
    densidad_plantacion: Optional[int]
    tipo_sensor: Optional[str]
    eficiencia_riego: Optional[float]  # decimal
    caudal: Optional[float]  # decimal
    ph_agua: Optional[float]  # decimal
    acolchado: Optional[int]  # boolean: 0=No, 1=Sí

class CultivoCreate(BaseModel):
    nombre_cultivo: str
    hectareas: int

@router.post("/usuarios/{correo}/agregar_cultivo") #post para agregar
def ruta_agregar_cultivo(correo: str, cultivo: CultivoCreate):
    return controller_agregar_cultivo(
        correo, cultivo.nombre_cultivo, cultivo.hectareas)

@router.patch("/usuarios/{correo}/cultivos/modificar_formulario_cultivo") #patch para modificar
def ruta_modificar_formulario_cultivo(correo: str, cultivo_datos: CultivoDatos):
    return controller_modificar_formulario_cultivo(correo, cultivo_datos)

class PuntoCoordenada(BaseModel):
    latitud: Optional[float]
    longitud: Optional[float]

class AreaCultivoDatos(BaseModel):
    cultivo: str
    area: float
    puntos: list[Optional[PuntoCoordenada]]

@router.patch("/usuarios/{correo}/cultivo/modificar_area_cultivo") #patch para modificar
def ruta_modificar_area_cultivo(correo: str, area_datos: AreaCultivoDatos):
    return controller_modificar_area_cultivo(correo, area_datos)

@router.delete("/usuarios/{correo}/{cultivo}/eliminar") #delete para borrar
def ruta_eliminar_cultivo(correo, cultivo):
    return controller_eliminar_cultivo(correo, cultivo)

class UsuarioModificado(BaseModel):
    #correo: str
    nombre: str
    ciudad: str
    region: str
    foto_perfil: str

@router.put("/usuarios/{correo}/modificar") #HAY QUE CAMBIAR TODITO EL COSIACO
def ruta_modificar_usuario(correo, usuarioMOD: UsuarioModificado): #usuarioMOD es el dict completo del usuario a modificar
    return controller_modificar_usuario(correo, usuarioMOD)

@router.patch("/usuarios/{correo}/ubicacion/{lat}/{lon}/modificar")
def ruta_modificar_ubicacion_usuario(correo, lat, lon): #lat y lon pueden ser pasadon como string sin problema
    return controller_modificar_ubicacion_usuario(correo, lat, lon)

@router.patch("/usuarios/{correo}/ubicacion/region/{region}/{ciudad}/modificar")
def ruta_modificar_region_ciudad_usuario(correo, region, ciudad):
    return controller_modificar_region_ciudad_usuario(correo, region, ciudad)

@router.delete("/usuarios/{correo}")
def ruta_eliminar_usuario(correo):
    return controller_eliminar_usuario(correo)

@router.patch("/usuarios/{correo}/modificar_notificaciones/{notificaciones}")
def ruta_modificar_notificaciones_usuario(correo, notificaciones: bool):
    return controller_modificar_notificaciones_usuario(correo, notificaciones)