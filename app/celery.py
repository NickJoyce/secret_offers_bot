from celery import Celery

# celery init
celery_app = Celery("celery_worker", broker_url="redis://127.0.0.1:6379/0", result_backend="redis://127.0.0.1:6379/0",)
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,  # Убедитесь, что UTC включен
    timezone='Europe/Moscow',  # Устанавливаем московское время
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

celery_app.autodiscover_tasks()