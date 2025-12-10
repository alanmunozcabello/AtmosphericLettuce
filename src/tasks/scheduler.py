import threading
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from tasks.enviar_correos_tasks import (
    enviar_correos_a_todos,
    verificar_y_enviar_alertas_diarias
)

scheduler = BackgroundScheduler(daemon=True)
scheduler_thread = None


def start_scheduler():
    """Inicia el scheduler en un thread separado del proceso principal"""
    global scheduler_thread
    
    if scheduler.running:
        print("⚠️  Scheduler ya está corriendo")
        return scheduler
    
    print("\n🚀 Iniciando scheduler en thread separado...")

    # ========== PRODUCCIÓN ==========

    # # Job 1: Correo semanal - Todos los LUNES a las 8:00 AM
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

    # # Job 2: Alertas diarias - Martes a Domingo a las 9:00 AM
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

    
    scheduler.add_job(
        enviar_correos_a_todos,
        "interval",
        minutes=1,
        id="correo_semanal_test",
        replace_existing=True
    )
    print("🧪 PRUEBA - Correo semanal: cada 2 minutos")

    # Job 2: Alertas diarias - cada 3 minutos
    scheduler.add_job(
        verificar_y_enviar_alertas_diarias,
        "interval",
        minutes=2,
        id="alertas_diarias_test",
        replace_existing=True
    )
    print("🧪 PRUEBA - Alertas diarias: cada 3 minutos")
    
    # Iniciar scheduler en thread separado
    def run_scheduler():
        """Función que ejecuta el scheduler en el thread"""
        try:
            scheduler.start()
            print("✅ Scheduler iniciado correctamente en thread separado")
            print(f"🧵 Thread ID: {threading.current_thread().ident}")
            print("📋 Jobs activos:", [job.id for job in scheduler.get_jobs()])
        except Exception as e:
            print(f"❌ Error al iniciar scheduler: {e}")
    
    # Crear y iniciar thread daemon (se cierra cuando el proceso principal termina)
    scheduler_thread = threading.Thread(
        target=run_scheduler,
        name="SchedulerThread",
        daemon=True  # Thread daemon se cierra automáticamente al cerrar la app
    )
    scheduler_thread.start()
    
    # Registrar función de limpieza al cerrar la aplicación
    atexit.register(stop_scheduler)
    
    return scheduler


def stop_scheduler():
    """Detiene el scheduler de forma limpia"""
    global scheduler
    if scheduler and scheduler.running:
        print("\n⏹️  Deteniendo scheduler...")
        scheduler.shutdown(wait=False)
        print("✅ Scheduler detenido correctamente")

    # ========== MODO DE PRUEBA ==========

    # Job 1: Correo semanal - cada 2 minutos

    # scheduler.start()
    # print("\n✅ Scheduler iniciado en MODO PRUEBA")
    # print(
    #     "💡 Para producción, comenta el bloque de PRUEBA y "
    #     "descomenta PRODUCCIÓN\n"
    # )
