from services.clima_service import clima_hora_service, clima_hoy_service, clima_semana_service

def clima_hora_controller(lat, lon):
    return clima_hora_service(lat, lon)

def clima_hoy_controller(lat, lon):
    return clima_hoy_service(lat, lon)

def clima_semana_controller(lat, lon):
    return clima_semana_service(lat, lon)