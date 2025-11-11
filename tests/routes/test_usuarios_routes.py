import pytest

def test_registrar_usuario_routes(client):
    "prueba para endpoint de registrar usuario"
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
def test_agregar_cultivo_routes(client):
    "prueba para endpoint de agregar un cultivo"
    correo = "ejemplo8@lechuga.com"
    datos = {
        "nombre_cultivo": "tomate",
        "hectareas": 10
    }
    respuesta = client.post(f"/usuarios/{correo}/agregar_cultivo", json=datos)
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "agregado exitosamente" in respuesta.json()["mensaje"]


def test_modificar_formulario_cultivo(client):
    "prueba para endpoint de modificar formulario de cultivo"
    correo = "ejemplo8@lechuga.com"
    cultivo_datos = {
        "nombre_cultivo": "tomate",
        "hectareas": 12.5,
        "fecha_siembra": "2025-01-15",
        "notas": "Cultivo de prueba automatizado",
        "etapa_planta": "Crecimiento",
        "tipo_riego": "Por goteo",
        "ultimo_riego": "2025-11-09T08:00:00",
        "frecuencia_riego": "Diario",
        "humedad_suelo": "Media",
        "textura_suelo": "Arcillosa",
        "variedad_planta": "Tomate Cherry",
        "estado_planta": "Saludable",
        "estres_hidrico": 0,
        "profundidad_radical": 40,
        "densidad_plantacion": 150,
        "tipo_sensor": "Capacitivo",
        "eficiencia_riego": 90.0,
        "caudal": 3.2,
        "ph_agua": 6.5,
        "acolchado": 1
    }
    respuesta = client.patch(
        f"/usuarios/{correo}/cultivos/modificar_formulario_cultivo",
        json=cultivo_datos
    )
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "modificado exitosamente" in respuesta.json()["mensaje"]


def test_eliminar_cultivo_routes(client):
    "prueba para endpoint de eliminar cultivo"
    correo = "ejemplo8@lechuga.com"
    cultivo = "tomate"
    respuesta = client.delete(f"/usuarios/{correo}/{cultivo}/eliminar")
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "eliminado" in respuesta.json()["mensaje"]


 
def test_obtener_todos_usuarios_routes(client):
    "prueba para endpoint de obtener todos los usuarios"
    respuesta = client.get("/usuarios")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), dict)  # Retorna dict de usuarios
    assert "ejemplo8@lechuga.com" in respuesta.json()  # Usuario existe


def test_obtener_usuario_routes(client):
    "prueba para endpoint de obtener un usuario específico"
    correo = "ejemplo8@lechuga.com"
    respuesta = client.get(f"/usuarios/{correo}")
    assert respuesta.status_code == 200
    assert "id" in respuesta.json()
    assert respuesta.json()["id"] == correo
    assert "nombre" in respuesta.json()  # Verifica estructura


def test_iniciar_sesion_routes(client):
    "prueba para endpoint de iniciar sesión"
    correo = "ejemplo8@lechuga.com"
    contrasena = "password123"
    respuesta = client.get(f"/usuarios/iniciar_sesion/{correo}/{contrasena}")
    assert respuesta.status_code == 200
    assert "id" in respuesta.json()
    assert respuesta.json()["id"] == correo
    assert "nombre" in respuesta.json()  # Verifica estructura


def test_obtener_cultivos_routes(client):
    "prueba para endpoint de obtener cultivos de un usuario"
    correo = "ejemplo8@lechuga.com"
    respuesta = client.get(f"/usuarios/{correo}/cultivos")
    assert respuesta.status_code == 200
    # Puede retornar lista o dict con error si no existe el usuario
    assert isinstance(respuesta.json(), (list, dict))


def test_modificar_area_cultivos_routes(client):
    "prueba para endpoint de modificar área de cultivo"
    correo = "ejemplo8@lechuga.com"
    area_datos = {
        "cultivo": "tomate",
        "area": 12.2,
        "puntos": [
            {"latitud": -33.4489, "longitud": -70.6693},
            {"latitud": -33.4490, "longitud": -70.6694},
            {"latitud": -33.4491, "longitud": -70.6695}
        ]
    }
    respuesta = client.patch(
        f"/usuarios/{correo}/cultivo/modificar_area_cultivo",
        json=area_datos
    )
    assert respuesta.status_code == 200
    # Puede retornar mensaje de éxito o error si no existe
    assert "mensaje" in respuesta.json() or "error" in respuesta.json()

def test_eliminar_usuario_routes(client):
    "prueba para endpoint de eliminar usuario"
    correo = "ejemplo8@lechuga.com"
    respuesta = client.delete(f"/usuarios/{correo}")
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "eliminado exitosamente" in respuesta.json()["mensaje"]
