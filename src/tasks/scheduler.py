from apscheduler.schedulers.background import BackgroundScheduler
from tasks.enviar_correos_tasks import enviar_correos_a_todos

scheduler = BackgroundScheduler()


def start_scheduler():

    if scheduler.running:
        return  # evita reinicios duplicados si se usa --reload

    #  MODO DE PRUEBA: Ejecutar cada 1 minuto
    scheduler.add_job(
        enviar_correos_a_todos,
        "interval",
        minutes=1,
        id="correo_periodico",
        replace_existing=True
    )
    print("🧪 Scheduler iniciado: se ejecutará cada 1 minuto (MODO PRUEBA)")
    scheduler.start()

    """ # PRODUCCIÓN: Todos los lunes a las 8:00 AM
    # formato de dia a hasta dia b a-b

    scheduler.add_job(
        enviar_correos_a_todos,
        "cron",
        day_of_week="mon",
        hour=8,
        minute=0,
        id="correo_periodico",
        replace_existing=True
    )
    print("🕓 Scheduler iniciado: se ejecutará todos los lunes a las 8:00 AM")
    scheduler.start()"""

