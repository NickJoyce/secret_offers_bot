from celery import Celery

# celery init
celery_app = Celery("celery_worker")
celery_app.config_from_object("settings", namespace="CELERY")
celery_app.autodiscover_tasks()