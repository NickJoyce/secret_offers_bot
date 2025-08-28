from app.celery import celery_app
import time
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True,
                 max_retries=3, 
                 default_retry_delay=5)
def tg_channel(self):
    logger.info("Task started")
    time.sleep(2)
    logger.info("Task completed")
