from fastapi import APIRouter
from controllers.usuarios_controller import obtener_todos_los_usuarios, registrar_usuario

router=APIRouter()

@router.get("/") #"pagina inicial"
def root():
    return {"mensaje": "Bienvenido a la API"} #----------------front

@router.get("/ping") #test de mensaje
def hacer_ping():
    return {"mensaje": "pong"} #----------------front

@router.get("/usuarios") #get es para dar información
def ruta_obtener_usuarios(): #enrutador para obtener los usuarios y mostrarlos
    return {"usuarios":obtener_todos_los_usuarios()} #----------------front

@router.post("/usuarios/registrar") #post es para recibir información
def ruta_registrar_usuario(correo, nombre, contrasena): #se llama al controlador para procese el guardado del nuevo usuario
    return registrar_usuario(correo, nombre, contrasena) #----------------front