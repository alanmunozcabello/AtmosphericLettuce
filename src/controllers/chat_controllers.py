from services.chat_service import procesar_consulta


def consultar(payload):
    return procesar_consulta(payload)