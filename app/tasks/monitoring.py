from app.celery import celery_app
import time
import logging
from app.bot.main import bot
import requests

logger = logging.getLogger(__name__)


@celery_app.task(bind=True,
                 max_retries=3, 
                 default_retry_delay=5)
def is_subscriber(self):
    user_id = '520704135'
    response = requests.get(f'https://secret-offers-bot.podrugeapi.ru/is_subscriber?user_id={user_id}')
    logger.info(f"response: {str(response.json())}")


