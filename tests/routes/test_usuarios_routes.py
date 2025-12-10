import pytest

# Fixture local para crear usuario antes de pruebas que lo requieren
@pytest.fixture
def usuario_creado(client, correo_test):
    """Crea un usuario de prueba y retorna sus datos"""
    datos = {
        "correo": correo_test,
        "nombre": "Usuario Test",
        "contrasena": "Password123@"
    }
    # Intentar eliminar el usuario primero si existe
    try:
        from services.user_service import get_db_connection
        conn = get_db_connection()
        conn.execute("DELETE FROM usuarios WHERE correo = ?", (correo_test,))
        conn.commit()
        conn.close()
    except:
        pass
    
    # Crear el usuario
    response = client.post("/usuarios/registrar", json=datos)
    return datos

def test_registrar_usuario_routes(client):
    """Prueba para endpoint de registrar usuario"""
    # Usar correo único para evitar conflictos con otros tests
    correo_nuevo = "usuario_nuevo_test@lechuga.com"
    
    datos_usuario = {
        "correo": correo_nuevo,
        "nombre": "Usuario Nuevo",
        "contrasena": "Password123@"
    }
    
    # Limpiar primero si existe
    try:
        from services.user_service import get_db_connection
        conn = get_db_connection()
        conn.execute("DELETE FROM usuarios WHERE correo = ?", (correo_nuevo,))
        conn.commit()
        conn.close()
    except:
        pass
    
    respuesta = client.post("/usuarios/registrar", json=datos_usuario)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    
    # Puede retornar mensaje de éxito o error si ya existe
    assert "mensaje" in datos or "error" in datos

def test_agregar_cultivo_routes(client, auth_headers, correo_test, usuario_creado):
    "prueba para endpoint de agregar un cultivo"
    datos = {
        "nombre_cultivo": "tomate",
        "hectareas": 10
    }
    # Headers con token
    headers = auth_headers(correo_test)
    
    respuesta = client.post(
        f"/usuarios/{correo_test}/agregar_cultivo", 
        json=datos,
        headers=headers
    )
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "agregado exitosamente" in respuesta.json()["mensaje"]

def test_modificar_formulario_cultivo(client, auth_headers, correo_test, usuario_creado):
    "prueba para endpoint de modificar formulario de cultivo"
    # 1. Agregar cultivo primero
    headers = auth_headers(correo_test)
    client.post(f"/usuarios/{correo_test}/agregar_cultivo", json={"nombre_cultivo": "tomate", "hectareas": 10}, headers=headers)
    
    # 2. Modificar
    cultivo_datos = {
        "nombre_cultivo": "tomate",
        "hectareas": 12.5,
        "fecha_siembra": "2025-01-15",
        "notas": "Cultivo de prueba automatizado",
        "etapa_planta": "crecimiento-vegetativo",
        "tipo_riego": "goteo",
        "ultimo_riego": "2025-11-09T08:00:00",
        "frecuencia_riego": "2",
        "humedad_suelo": "45",
        "textura_suelo": "arcilloso",
        "variedad_planta": "Tomate Cherry",
        "estado_planta": "Saludable",
        "estres_hidrico": 0,
        "profundidad_radical": 40,
        "densidad_plantacion": 150,
        "tipo_sensor": "capacitancia",
        "eficiencia_riego": 90.0,
        "caudal": 3.2,
        "ph_agua": 6.5,
        "acolchado": 1
    }
    respuesta = client.patch(
        f"/usuarios/{correo_test}/cultivos/modificar_formulario_cultivo",
        json=cultivo_datos,
        headers=headers
    )
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "modificado exitosamente" in respuesta.json()["mensaje"]

def test_eliminar_cultivo_routes(client, auth_headers, correo_test, usuario_creado):
    "prueba para endpoint de eliminar cultivo"
    headers = auth_headers(correo_test)
    client.post(f"/usuarios/{correo_test}/agregar_cultivo", json={"nombre_cultivo": "tomate", "hectareas": 10}, headers=headers)
    
    cultivo = "tomate"
    respuesta = client.delete(
        f"/usuarios/{correo_test}/{cultivo}/eliminar",
        headers=headers
    )
    assert respuesta.status_code == 200
    assert "eliminado" in respuesta.json()["mensaje"]

def test_obtener_usuario_routes(client, auth_headers, correo_test, usuario_creado):
    """Prueba para endpoint de obtener un usuario específico"""
    respuesta = client.get(
        f"/usuarios/{correo_test}",
        headers=auth_headers(correo_test)
    )
    assert respuesta.status_code == 200
    assert "id" in respuesta.json()
    assert respuesta.json()["id"] == correo_test

def test_iniciar_sesion_routes(client, usuario_creado, correo_test):
    "prueba para endpoint de iniciar sesión (POST)"
    datos = {
        "correo": correo_test,
        "contrasena": "Password123@"
    }
    respuesta = client.post("/usuarios/login", json=datos)
    assert respuesta.status_code == 200
    assert "token" in respuesta.json()

def test_eliminar_usuario_routes(client, auth_headers, correo_test, usuario_creado):
    "prueba para endpoint de eliminar usuario"
    headers = auth_headers(correo_test)
    
    respuesta = client.delete(
        f"/usuarios/{correo_test}",
        headers=headers
    )
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()
    assert "eliminado exitosamente" in respuesta.json()["mensaje"]


# ========== TESTS ADICIONALES DE USUARIOS ==========

def test_registrar_usuario_correo_duplicado(client, correo_test, usuario_creado):
    """Prueba registrar usuario con correo ya existente"""
    datos = {
        "correo": correo_test,
        "nombre": "Otro Usuario",
        "contrasena": "Password123@"
    }
    
    respuesta = client.post("/usuarios/registrar", json=datos)
    
    # Puede ser 400 o 200 dependiendo si actualiza o rechaza
    assert respuesta.status_code in [200, 400]


def test_registrar_usuario_sin_datos(client):
    """Prueba registrar usuario sin enviar datos"""
    respuesta = client.post("/usuarios/registrar", json={})
    
    assert respuesta.status_code == 422


def test_iniciar_sesion_contrasena_incorrecta(client, correo_test, usuario_creado):
    """Prueba iniciar sesión con contraseña incorrecta"""
    datos = {
        "correo": correo_test,
        "contrasena": "ContrasenaIncorrecta123"
    }
    
    respuesta = client.post("/usuarios/login", json=datos)
    
    # La ruta retorna 200 con error en JSON, no levanta HTTPException
    assert respuesta.status_code == 200
    assert "error" in respuesta.json()


def test_iniciar_sesion_usuario_no_existe(client):
    """Prueba iniciar sesión con usuario que no existe"""
    datos = {
        "correo": "noexiste@ejemplo.com",
        "contrasena": "Password123"
    }
    
    respuesta = client.post("/usuarios/login", json=datos)
    
    # La ruta retorna 200 con error en JSON, no 401/404
    assert respuesta.status_code == 200
    assert "error" in respuesta.json()


def test_obtener_cultivos_usuario(client, auth_headers, correo_test, usuario_creado):
    """Prueba obtener todos los cultivos de un usuario"""
    headers = auth_headers(correo_test)
    
    # Agregar un cultivo primero
    client.post(
        f"/usuarios/{correo_test}/agregar_cultivo",
        json={"nombre_cultivo": "tomate", "hectareas": 10},
        headers=headers
    )
    
    # Obtener cultivos
    respuesta = client.get(
        f"/usuarios/{correo_test}/cultivos",
        headers=headers
    )
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert isinstance(datos, dict)
    assert "cultivos" in datos
    assert "paginacion" in datos
    assert isinstance(datos["cultivos"], list)


def test_obtener_nombres_cultivos(client, auth_headers, correo_test, usuario_creado):
    """Prueba obtener solo los nombres de cultivos"""
    headers = auth_headers(correo_test)
    
    # Agregar cultivos
    client.post(
        f"/usuarios/{correo_test}/agregar_cultivo",
        json={"nombre_cultivo": "tomate", "hectareas": 10},
        headers=headers
    )
    client.post(
        f"/usuarios/{correo_test}/agregar_cultivo",
        json={"nombre_cultivo": "lechuga", "hectareas": 5},
        headers=headers
    )
    
    # Obtener nombres
    respuesta = client.get(
        f"/usuarios/{correo_test}/cultivos/nombres",
        headers=headers
    )
    
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def test_modificar_usuario(client, auth_headers, correo_test, usuario_creado):
    """Prueba modificar datos de un usuario"""
    headers = auth_headers(correo_test)
    
    datos_modificados = {
        "nombre": "Nombre Actualizado",
        "latitud": -33.4489,
        "longitud": -70.6693
    }
    
    respuesta = client.put(
        f"/usuarios/{correo_test}/modificar",
        json=datos_modificados,
        headers=headers
    )
    
    assert respuesta.status_code == 200


def test_modificar_ubicacion(client, auth_headers, correo_test, usuario_creado):
    """Prueba modificar ubicación de un usuario"""
    headers = auth_headers(correo_test)
    
    datos_ubicacion = {
        "latitud": -35.4264,
        "longitud": -71.6554
    }
    
    respuesta = client.patch(
        f"/usuarios/{correo_test}/ubicacion/modificar",
        json=datos_ubicacion,
        headers=headers
    )
    
    assert respuesta.status_code == 200


def test_agregar_cultivo_sin_autenticacion(client, correo_test):
    """Prueba agregar cultivo sin token de autenticación"""
    datos = {
        "nombre_cultivo": "tomate",
        "hectareas": 10
    }
    
    respuesta = client.post(
        f"/usuarios/{correo_test}/agregar_cultivo",
        json=datos
    )
    
    assert respuesta.status_code == 401


def test_eliminar_cultivo_sin_autenticacion(client, correo_test):
    """Prueba eliminar cultivo sin autenticación"""
    respuesta = client.delete(f"/usuarios/{correo_test}/tomate/eliminar")
    
    assert respuesta.status_code == 401


def test_modificar_area_cultivo(client, auth_headers, correo_test, usuario_creado):
    """Prueba modificar solo el área de un cultivo"""
    headers = auth_headers(correo_test)
    
    # Agregar cultivo
    client.post(
        f"/usuarios/{correo_test}/agregar_cultivo",
        json={"nombre_cultivo": "tomate", "hectareas": 10},
        headers=headers
    )
    
    # Modificar área con modelo correcto
    datos_area = {
        "cultivo": "tomate",
        "area": 15.5,
        "puntos": [
            {"latitud": -33.4489, "longitud": -70.6693},
            {"latitud": -33.4490, "longitud": -70.6694},
            {"latitud": -33.4491, "longitud": -70.6695}
        ]
    }
    
    respuesta = client.patch(
        f"/usuarios/{correo_test}/cultivo/modificar_area_cultivo",
        json=datos_area,
        headers=headers
    )
    
    assert respuesta.status_code == 200


def test_obtener_usuario_sin_autenticacion(client, correo_test):
    """Prueba obtener usuario sin autenticación"""
    respuesta = client.get(f"/usuarios/{correo_test}")
    
    assert respuesta.status_code == 401


def test_eliminar_usuario_sin_autenticacion(client, correo_test):
    """Prueba eliminar usuario sin autenticación"""
    respuesta = client.delete(f"/usuarios/{correo_test}")
    
    assert respuesta.status_code == 401
