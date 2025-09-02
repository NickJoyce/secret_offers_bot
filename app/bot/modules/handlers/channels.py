from aiogram import Router
from aiogram.types import Message
import logging


logger = logging.getLogger(__name__)


router = Router()

@router.channel_post()
async def on_channel_post(msg: Message):
    logger.info(f"Channel post: {msg}")
