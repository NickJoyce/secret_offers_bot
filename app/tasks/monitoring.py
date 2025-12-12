from app.celery import celery_app
import time
import logging
from app.bot.main import bot
import requests
from asyncio import sleep
from app.database.queries.tg_channels_post import get_last_channel_post
from app.database.queries.tg_deeplink_requests import create_deeplink_request
from app.database.conn import SyncSession


logger = logging.getLogger(__name__)


@celery_app.task(bind=True,
                 max_retries=3, 
                 default_retry_delay=5)
def is_subscriber(self):
    user_id = '520704135'
    response = requests.get(f'https://secret-offers-bot.podrugeapi.ru/is_subscriber?user_id={user_id}')
    logger.info(f"response: {str(response.json())}")
    
    
    
@celery_app.task(bind=True,
                 max_retries=3,
                 default_retry_delay=5)
def delete_buttons(self):
    "проверяет дату истечение кнопок и удаляет клавиатуру если она просрочена"
    requests.get('https://secret-offers-bot.podrugeapi.ru/delete-buttons')



@celery_app.task(bind=True,
                 max_retries=1,
                 default_retry_delay=5)
def create_deeplink_request_task(self, deeplink_id, tg_id, received_at):
    item = {
        "deeplink_id": deeplink_id,
        "tg_id": tg_id,
        "received_at": received_at
    }
    create_deeplink_request(item=item)

