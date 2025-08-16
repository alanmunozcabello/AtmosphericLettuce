from fastapi import APIRouter
from controllers.usuarios_controller import obtener_todos_los_usuarios, guardar_nuevos_usuarios

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
def registrar_usuario(nombre, contrasena): 
    usuarios=obtener_todos_los_usuarios() #validaciones para registrar un usuario
    if any(usuario["nombre"]==nombre for usuario in usuarios) or any(usuario["contrasena"]==contrasena for usuario in usuarios):
        return {"mensaje":"usuario ya registrado o contraseña ya utilizada"} #----------------front
    nuevo_usuario={"id":len(usuarios)+1, "nombre":nombre, "contrasena":contrasena} #si el usuario o contraseña no existen se crea un nuevo usuario con los parametros de llegada
    usuarios.append(nuevo_usuario)
    guardar_nuevos_usuarios(usuarios) #se llama al controlador para procese el guardado del nuevo usuario
    return {"mensaje":"usuario ingresado correctamente"} #----------------front