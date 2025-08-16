from fastapi import APIRouter
from controllers.usuarios_controller import obtener_todos_los_usuarios, guardar_nuevos_usuarios

router=APIRouter()

@router.get("/usuarios")
def ruta_obtener_usuarios(): #enrutador para obtener los usuarios
    return {"usuarios":obtener_todos_los_usuarios()}

@router.post("/usuarios/registrar")
def registrar_usuario(nombre, contrasena):
    usuarios=obtener_todos_los_usuarios()
    if any(usuario["nombre"]==nombre for usuario in usuarios) or any(usuario["contrasena"]==contrasena for usuario in usuarios):
        return {"mensaje":"usuario ya registrado o contraseña ya utilizada"}
    nuevo_usuario={"id":len(usuarios)+1, "nombre":nombre, "contrasena":contrasena}
    usuarios.append(nuevo_usuario)
    guardar_nuevos_usuarios(usuarios)
    return {"mensaje":"usuario ingresado correctamente"}