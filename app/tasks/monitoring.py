from app.celery import celery_app
import time
import logging

logger = logging.getLogger(__name__)


@celery_app.task()
def tg_channel():
    logger.info("Task started")
    time.sleep(2)
    logger.info("Task completed")
