from services.clima_service import (
    clima_hora_service,
    clima_hoy_service,
    clima_semana_service,
)


def clima_hora_controller(lat, lon):
    if lat is None or lon is None:
        return {
            "success": False,
            "error": "Latitud y longitud son obligatorias"
        }

    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return {
            "success": False,
            "error": "Latitud y longitud deben ser números válidos"
        }

    if not (-90 <= lat <= 90):
        return {
            "success": False,
            "error": "Latitud debe estar entre -90 y 90"
        }

    if not (-180 <= lon <= 180):
        return {
            "success": False,
            "error": "Longitud debe estar entre -180 y 180"
        }

    lat = round(lat, 6)
    lon = round(lon, 6)

    return clima_hora_service(lat, lon)


def clima_hoy_controller(lat, lon):
    if lat is None or lon is None:
        return {
            "success": False,
            "error": "Latitud y longitud son obligatorias"
        }

    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return {
            "success": False,
            "error": "Latitud y longitud deben ser números válidos"
        }

    if not (-90 <= lat <= 90):
        return {
            "success": False,
            "error": "Latitud debe estar entre -90 y 90"
        }

    if not (-180 <= lon <= 180):
        return {
            "success": False,
            "error": "Longitud debe estar entre -180 y 180"
        }

    lat = round(lat, 6)
    lon = round(lon, 6)

    return clima_hoy_service(lat, lon)


def clima_semana_controller(lat, lon):
    if lat is None or lon is None:
        return {
            "success": False,
            "error": "Latitud y longitud son obligatorias"
        }

    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return {
            "success": False,
            "error": "Latitud y longitud deben ser números válidos"
        }

    if not (-90 <= lat <= 90):
        return {
            "success": False,
            "error": "Latitud debe estar entre -90 y 90"
        }

    if not (-180 <= lon <= 180):
        return {
            "success": False,
            "error": "Longitud debe estar entre -180 y 180"
        }

    lat = round(lat, 6)
    lon = round(lon, 6)

    return clima_semana_service(lat, lon)
