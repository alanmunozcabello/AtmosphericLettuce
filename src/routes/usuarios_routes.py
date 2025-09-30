from fastapi import APIRouter
from controllers.usuarios_controller import controller_obtener_todos_los_usuarios, controller_obtener_usuario, controller_registrar_usuario, controller_obtener_cultivos_usuario, controller_agregar_o_modificar_cultivo, controller_eliminar_cultivo, controller_iniciar_sesion, controller_modificar_usuario, controller_modificar_ubicacion_usuario, controller_modificar_region_ciudad_usuario
from pydantic import BaseModel

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

# @router.post("/usuarios/registrar") #post es para recibir información
# def ruta_registrar_usuario(correo, nombre, contrasena): #se llama al controlador para procese el guardado del nuevo usuario
#     return controller_registrar_usuario(correo, nombre, contrasena) #----------------front

@router.get("/usuarios/{correo}/cultivos")
def ruta_obtener_cultivos_usuario(correo):
    return controller_obtener_cultivos_usuario(correo)

@router.patch("/usuarios/{correo}/{cultivo}/{hectareas}/agregar_modificar") #patch para modificar
def ruta_agregar_o_modificar_cultivo(correo, cultivo, hectareas):
    return controller_agregar_o_modificar_cultivo(correo, cultivo, hectareas)

@router.delete("/usuarios/{correo}/{cultivo}/eliminar") #delete para borrar
def ruta_eliminar_cultivo(correo, cultivo):
    return controller_eliminar_cultivo(correo, cultivo)

class UsuarioModificado(BaseModel):
    correo: str
    nombre: str
    ciudad: str
    region: str

@router.put("/usuarios/{correo}/modificar") #HAY QUE CAMBIAR TODITO EL COSIACO
def ruta_modificar_usuario(correo, usuarioMOD: UsuarioModificado): #usuarioMOD es el dict completo del usuario a modificar
    return controller_modificar_usuario(correo, usuarioMOD)

@router.patch("/usuarios/{correo}/ubicacion/{lat}/{lon}/modificar")
def ruta_modificar_ubicacion_usuario(correo, lat, lon): #lat y lon pueden ser pasadon como string sin problema
    return controller_modificar_ubicacion_usuario(correo, lat, lon)

@router.patch("/usuarios/{correo}/ubicacion/region/{region}/{ciudad}/modificar")
def ruta_modificar_region_ciudad_usuario(correo, region, ciudad):
    return controller_modificar_region_ciudad_usuario(correo, region, ciudad)