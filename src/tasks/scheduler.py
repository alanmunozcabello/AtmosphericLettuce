from apscheduler.schedulers.background import BackgroundScheduler
from tasks.enviar_correos_tasks import (
    enviar_correos_a_todos,
    verificar_y_enviar_alertas_diarias
)

scheduler = BackgroundScheduler()


def start_scheduler():

    if scheduler.running:
        return

    # ========== PRODUCCIÓN ==========

    # Job 1: Correo semanal - Todos los LUNES a las 8:00 AM
    # scheduler.add_job(
    #    enviar_correos_a_todos,
    #    "cron",
    #    day_of_week="mon",
    #    hour=8,
    #    minute=0,
    #    id="correo_semanal",
    #    replace_existing=True
    # )
    # print("🕓 Job semanal: se ejecutará todos los LUNES a las 8:00 AM")

    # Job 2: Alertas diarias - Martes a Domingo a las 9:00 AM
    # scheduler.add_job(
    #    verificar_y_enviar_alertas_diarias,
    #    "cron",
    #    day_of_week="tue-sun",  # Martes a Domingo (todos menos lunes)
    #    hour=9,
    #    minute=0,
    #    id="alertas_diarias",
    #    replace_existing=True
    # )
    # print("⚠️  Job de alertas: se ejecutará MAR-DOM a las 9:00 AM")
    # scheduler.start()

    # ========== MODO DE PRUEBA ==========

    # Job 1: Correo semanal - cada 2 minutos
    scheduler.add_job(
        enviar_correos_a_todos,
        "interval",
        minutes=2,
        id="correo_semanal_test",
        replace_existing=True
    )
    print("🧪 PRUEBA - Correo semanal: cada 2 minutos")

    # Job 2: Alertas diarias - cada 3 minutos
    scheduler.add_job(
        verificar_y_enviar_alertas_diarias,
        "interval",
        minutes=3,
        id="alertas_diarias_test",
        replace_existing=True
    )
    print("🧪 PRUEBA - Alertas diarias: cada 3 minutos")

    scheduler.start()
    print("\n✅ Scheduler iniciado en MODO PRUEBA")
    print(
        "💡 Para producción, comenta el bloque de PRUEBA y "
        "descomenta PRODUCCIÓN\n"
    )
