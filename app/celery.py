from celery import Celery
from celery.schedules import crontab


# celery init
celery_app = Celery("celery_worker", 
                    broker_url="redis://127.0.0.1:6379/0", 
                    result_backend="redis://127.0.0.1:6379/0",)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,  
    timezone='Europe/Moscow',  
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    imports=("app.tasks.monitoring",)
)



celery_app.conf.beat_schedule = {
    # "tg_channel_monitoring": {
    #     "task": "app.tasks.monitoring.is_subscriber",
    #     "schedule": crontab(minute="*/1")
    # },
    # "check_subscriptions": {
    #     "task": "app.tasks.monitoring.check_subscriptions",
    #     # every day at 10:00
    #     "schedule": crontab(hour=10, minute=0)  
    # },
    "delete_buttons": {
        "task": "app.tasks.monitoring.delete_buttons",
        "schedule": crontab(minute="*/5")
    }
}


celery_app.autodiscover_tasks()