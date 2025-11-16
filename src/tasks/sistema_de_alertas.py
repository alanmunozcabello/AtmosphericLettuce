from services.usuarios_service import (
    service_obtener_usuario_para_frontend,
    obtener_clima_guardado
)
from services.clima_service import clima_hoy_service


def analizar_condiciones_adversas(correo):
    """
    Analiza condiciones climáticas adversas comparando clima guardado
    vs actual.

    Detecta 5 situaciones adversas:
    1. Lluvia no pronosticada
    2. Temperaturas máximas más altas de lo esperado (>10°C)
    3. Temperaturas mínimas más bajas de lo esperado (>10°C)
    4. Viento fuerte no pronosticado (>30 km/h)
    5. Cambio drástico de estado climático (Soleado → Tormenta)

    Returns:
        dict: {
            "alertas": [
                {
                    "cultivo": "nombre",
                    "tipo_alerta": "descripción",
                    "clima_inicial": {...},
                    "clima_actual": {...}
                }
            ]
        }
    """
    usuario = service_obtener_usuario_para_frontend(correo)

    # Extraer coordenadas de la estructura anidada
    ubicacion = usuario.get("ubicacion", {})
    lat = ubicacion.get("latitud")
    lon = ubicacion.get("longitud")

    if not lat or not lon:
        return {
            "error": "Usuario no tiene coordenadas configuradas",
            "alertas": []
        }
    condiciones_actuales_response = clima_hoy_service(lat, lon)
    if not condiciones_actuales_response.get("success"):
        return {
            "error": "No se pudo obtener el clima actual",
            "alertas": []
        }

    condiciones_actuales = condiciones_actuales_response.get("data", {})
    alertas = []

    print(
        f"📋 DEBUG - Usuario tiene {len(usuario.get('cultivos', []))} cultivos")

    for cultivo in usuario.get("cultivos", []):
        # El cultivo puede tener "nombre" o "nombre_cultivo" dependiendo de la
        # fuente
        nombre_cultivo = cultivo.get("nombre_cultivo") or cultivo.get("nombre")

        print(f"  🌱 Procesando cultivo: {nombre_cultivo}")

        if not nombre_cultivo:
            print("    ⏭️  Saltando - sin nombre")
            continue
        clima_guardado_response = obtener_clima_guardado(
            correo, nombre_cultivo)

        print(
            f"    📊 Clima guardado response: "
            f"{list(clima_guardado_response.keys())}")

        if clima_guardado_response.get("error"):
            print(
                f"    ⏭️  Saltando - error: "
                f"{clima_guardado_response.get('error')}")
            continue
        clima_guardado = clima_guardado_response.get("clima", {})
        if not clima_guardado:
            print("    ⏭️  Saltando - clima vacío")
            continue

        print("    ✅ Clima guardado encontrado")
        if not clima_guardado:
            continue
        clima_inicial = None
        if isinstance(clima_guardado, dict):

            if "1" in clima_guardado:
                clima_inicial = clima_guardado.get("1", {})
            elif "daily" in clima_guardado:

                daily = clima_guardado.get("daily", {})
                if daily and isinstance(daily, dict):
                    clima_inicial = {
                        "temp_max": daily.get(
                            "temperature_2m_max", [None])[0],
                        "temp_min": daily.get(
                            "temperature_2m_min", [None])[0],
                        "precipitation": daily.get(
                            "precipitation_sum", [None])[0],
                        "wind_speed": daily.get(
                            "wind_speed_10m_max", [None])[0],
                        "weather_code": daily.get(
                            "weather_code", [None])[0]
                    }
        if not clima_inicial:
            continue

        temp_actual = condiciones_actuales.get("temp", 0)
        temp_max_actual = condiciones_actuales.get("max", 0)
        temp_min_actual = condiciones_actuales.get("min", 0)
        estado_actual = condiciones_actuales.get("estado", "").lower()

        temp_max_inicial = clima_inicial.get(
            "max") or clima_inicial.get("temp_max") or 0
        temp_min_inicial = clima_inicial.get(
            "min") or clima_inicial.get("temp_min") or 0
        estado_inicial = (clima_inicial.get("estado") or "").lower()
        precipitacion_inicial = clima_inicial.get("precipitation") or 0
        viento_inicial = clima_inicial.get("wind_speed") or 0

        estados_lluvia = [
            "rain",
            "drizzle",
            "thunderstorm",
            "lluvia",
            "tormenta"]
        llueve_ahora = any(
            estado in estado_actual for estado in estados_lluvia)
        lloveria_inicial = (
            any(estado in estado_inicial for estado in estados_lluvia)
            or precipitacion_inicial > 0
        )

        # DEBUG: Imprimir valores
        print(f"\n🔍 DEBUG - Cultivo: {nombre_cultivo}")
        print(
            f"   Clima inicial: max={temp_max_inicial}, "
            f"min={temp_min_inicial}, estado='{estado_inicial}'")
        print(
            f"   Clima actual:  max={temp_max_actual}, "
            f"min={temp_min_actual}, estado='{estado_actual}'")
        print(
            f"   Llueve ahora: {llueve_ahora}, "
            f"Llovería inicial: {lloveria_inicial}")
        print(
            f"   Diferencia temp max: {
                temp_max_actual -
                temp_max_inicial}°C")
        print(
            f"   Diferencia temp min: {
                temp_min_inicial -
                temp_min_actual}°C")

        # 1. LLUVIA NO PRONOSTICADA
        if llueve_ahora and not lloveria_inicial:
            alertas.append({
                "cultivo": nombre_cultivo,
                "tipo_alerta": "⚠️ Lluvia no pronosticada",
                "severidad": "media",
                "clima_inicial": {
                    "estado": estado_inicial or "Desconocido",
                    "precipitacion": precipitacion_inicial
                },
                "clima_actual": {
                    "estado": estado_actual,
                    "temp": temp_actual
                }
            })

        # 2. TEMPERATURA MÁXIMA MÁS ALTA (>10°C)
        if temp_max_inicial and temp_max_actual > temp_max_inicial + 10:
            alertas.append({
                "cultivo": nombre_cultivo,
                "tipo_alerta": (
                    f"🌡️ Temperatura máxima más alta "
                    f"(+{round(temp_max_actual - temp_max_inicial, 1)}°C)"
                ),
                "severidad": "alta",
                "clima_inicial": {
                    "temp_max": temp_max_inicial,
                    "estado": estado_inicial
                },
                "clima_actual": {
                    "temp_max": temp_max_actual,
                    "estado": estado_actual
                }
            })

        # 3. TEMPERATURA MÍNIMA MÁS BAJA (>10°C)
        if temp_min_inicial and temp_min_actual < temp_min_inicial - 10:
            alertas.append(
                {
                    "cultivo": nombre_cultivo,
                    "tipo_alerta": f"❄️ Temperatura mínima más baja ({
                        round(
                            temp_min_inicial -
                            temp_min_actual,
                            1)}°C menos)",
                    "severidad": "alta",
                    "clima_inicial": {
                        "temp_min": temp_min_inicial,
                        "estado": estado_inicial},
                    "clima_actual": {
                        "temp_min": temp_min_actual,
                        "estado": estado_actual}})
        # 4. VIENTO FUERTE NO PRONOSTICADO (>30 km/h)
        viento_fuerte_actual = (
            "wind" in estado_actual or "windy" in estado_actual
        )
        viento_fuerte_inicial = viento_inicial > 8.33  # 30 km/h = 8.33 m/s

        if viento_fuerte_actual and not viento_fuerte_inicial:
            alertas.append({
                "cultivo": nombre_cultivo,
                "tipo_alerta": "💨 Vientos fuertes no pronosticados",
                "severidad": "media",
                "clima_inicial": {
                    "viento": (
                        f"{viento_inicial} m/s"
                        if viento_inicial else "Desconocido"
                    ),
                    "estado": estado_inicial
                },
                "clima_actual": {
                    "estado": estado_actual,
                    "descripcion": "Condiciones ventosas detectadas"
                }
            })
        estados_buenos = ["clear", "clouds", "despejado", "nublado"]
        estados_malos = [
            "thunderstorm",
            "rain",
            "drizzle",
            "snow",
            "tormenta",
            "lluvia",
            "nieve"]

        era_bueno = any(estado in estado_inicial for estado in estados_buenos)
        es_malo_ahora = any(
            estado in estado_actual for estado in estados_malos)

        if era_bueno and es_malo_ahora:
            alertas.append({
                "cultivo": nombre_cultivo,
                "tipo_alerta": (
                    "⛈️ Cambio drástico: "
                    "Clima favorable → Condiciones adversas"
                ),
                "severidad": "alta",
                "clima_inicial": {
                    "estado": estado_inicial,
                    "temp": temp_max_inicial
                },
                "clima_actual": {
                    "estado": estado_actual,
                    "temp": temp_actual
                }
            })

    return {
        "success": True,
        "total_alertas": len(alertas),
        "alertas": alertas
    }
