from app.celery import celery_app
import time


@celery_app.task
def test_task():
    time.sleep(2)
    print("Task completed")