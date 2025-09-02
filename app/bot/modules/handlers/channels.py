from aiogram import Router
from aiogram.types import Message
import logging


logger = logging.getLogger(__name__)


router = Router()

@router.channel_post()
async def on_channel_post(msg: Message):
    # msg.chat.id — id канала, msg.message_id — id поста
    text = msg.text
    logger.info(f"Channel post: {text}")
    # сохраните в БД и т.д.