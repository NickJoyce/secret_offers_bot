from app.celery import celery_app
import time


@celery_app.task(name='channel_monitoring',
                 bind=True,
                 max_retries=3, 
                 default_retry_delay=5)
def test_task(self):
    time.sleep(2)
    print("Task completed")