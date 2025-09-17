from fastapi import APIRouter
from controllers.usuarios_controller import controller_obtener_todos_los_usuarios, controller_obtener_usuario, controller_registrar_usuario, controller_obtener_cultivos_usuario, controller_agregar_o_modificar_cultivo, controller_eliminar_cultivo, controller_iniciar_secion

router=APIRouter()

@router.get("/") #"pagina inicial"
def root():
    return {"mensaje": "Bienvenido a la API"} #----------------front

@router.get("/ping") #test de mensaje
def hacer_ping():
    return {"mensaje": "pong"} #----------------front

@router.get("/usuarios") #get es para dar información
def ruta_obtener_usuarios(): #enrutador para obtener los usuarios y mostrarlos
    return {"usuarios":controller_obtener_todos_los_usuarios()} #----------------front

@router.post("/usuarios/usuario") #get es para dar información
def ruta_obtener_usuario(correo): #enrutador para obtener la informacion de un usuario
    return {"usuario":controller_obtener_usuario(correo)} #----------------front

#funcion no tan necesaria, el frontend puede saltarse esta y llamar directamente a ruta_obtener_usuario(correo) -> ver como seria cuando se vaya a usar coso de java token coso
@router.post("usuarios/iniciar_secion")
def ruta_iniciar_secion(correo):
    return controller_iniciar_secion(correo)

@router.post("/usuarios/registrar") #post es para recibir información
def ruta_registrar_usuario(correo, nombre, contrasena): #se llama al controlador para procese el guardado del nuevo usuario
    return controller_registrar_usuario(correo, nombre, contrasena) #----------------front

@router.post("/usuarios/usuario/cultivos")
def ruta_obtener_cultivos_usuario(correo):
    return controller_obtener_cultivos_usuario(correo)

@router.post("/usuarios/usuario/cultivos/agregar_modificar")
def ruta_agregar_o_modificar_cultivo(correo, cultivo):
    return controller_agregar_o_modificar_cultivo(correo, cultivo)

@router.post("/usuarios/usuario/cultivos/eliminar")
def ruta_eliminar_cultivo(correo, cultivo):
    return controller_eliminar_cultivo(correo, cultivo)
