from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
import logging
from fastapi.templating import Jinja2Templates
from settings.base import TEMPLATES_DIR
from app.tasks.monitoring import tg_channel
import traceback
from app.bot.main import bot

logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/state", include_in_schema=False)
async def health_check(request: Request):
    try:
        user_channel_status = await bot.get_chat_member(chat_id='-1002525082412', user_id='520704135')
        logger.info(f"user_channel_status: {user_channel_status}")
        return user_channel_status
    except Exception as e:
        logger.error(f"Error: {traceback.format_exc()}")
        return str(traceback.format_exc())

    