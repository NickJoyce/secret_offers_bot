from app.celery import celery_app
import time
import logging
from app.bot.main import bot
import requests
from asyncio import sleep
from app.database.queries.tg_channels_post import get_last_channel_post


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
    last_channel_post = await get_last_channel_post()

    if last_channel_post.buttons_expiration and last_channel_post.buttons_expiration < datetime.now():
        logger.info(datetime.now())
        logger.info(last_channel_post.buttons_expiration)
        ...
    # await bot.edit_message_reply_markup(chat_id=last_channel_post.chat_id, message_id=last_channel_post.message_id, reply_markup=None)


