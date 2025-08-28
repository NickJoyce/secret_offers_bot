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


@router.get("/chat-member-check", include_in_schema=False)
async def chat_member_check(user_id: str, request: Request):
    try:
        chat_member = await bot.get_chat_member(chat_id='-1002525082412', user_id=user_id)
        status = dict(chat_member)['status']
        if status != 'left':
            return 'Участник все еще в группе'
        else:
            return 'Участник покинул группу'
    except Exception as e:
        logger.error(f"Error: {traceback.format_exc()}")
        return str(traceback.format_exc())

    