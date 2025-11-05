import pytest

def test_registrar_usuario_routes(client):
    "prueba para usuario correcto"
    datos_usuario = {
        "correo": "ejemplo8@lechuga.com",
        "nombre": "Usuario Nuevo",
        "contrasena": "password123"
    }

    respuesta = client.post("/usuarios/registrar", json=datos_usuario)
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "Usuario registrado exitosamente" in respuesta.json()["mensaje"]

""" asegurarse de que retorna cada metodo... 
    recordar que en las rutas probamos los endpoints 
    codigos de error generalees 400 y  402
    
"""