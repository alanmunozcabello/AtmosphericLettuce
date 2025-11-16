from services.chat_service import procesar_consulta


def consultar(payload):
    if not payload:
        return {
            "success": False,
            "error": "El payload es obligatorio"
        }

    mensaje = payload.get("mensaje")

    if not mensaje:
        return {
            "success": False,
            "error": "El campo 'mensaje' es obligatorio"
        }

    if "'" in mensaje:
        return {
            "success": False,
            "error": "El mensaje no puede contener comillas simples (')"
        }

    return procesar_consulta(payload)
