from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
import logging
from fastapi.templating import Jinja2Templates
from settings.base import TEMPLATES_DIR
from aiogram.types import Update
from app.bot.main import bot, dp
from settings import WEBHOOK_PATH
from fastapi import Depends
from aiohttp import ClientSession
from app.utils.dependencies import get_http_session
from app.database.queries.tg_clients import get_client
import json
from app.database.queries.first_start_messages import create_first_start_messages, get_first_start_message, update_first_start_message
import asyncio
from app.bot.main import send_message_to_admin
from traceback import format_exc
from app.bot.modules.utils import escape_markdown_v2


logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)



@router.post(WEBHOOK_PATH)
async def bot_webhook(request: Request, session: ClientSession = Depends(get_http_session)) -> None:
    request_data = await request.json()
    logger.info(f"request_data: {request_data}")
    
    # обработка обнавления статуса пользователя в канале
    try:
        chat_id = request_data["chat_member"]["chat"]["id"]
        user_id = request_data["chat_member"]["from"]["id"]
        old_status = request_data["chat_member"]["old_chat_member"]["status"]
        new_status = request_data["chat_member"]["new_chat_member"]["status"]
        try:
            invite_link = request_data["chat_member"]["invite_link"]["invite_link"]
        except KeyError:
            invite_link = None
        
        await send_message_to_admin(escape_markdown_v2(f"chat_id: {chat_id}\n"
                                    f"user_id: {user_id}\n"
                                    f"{old_status} -> {new_status} \n"
                                    f"invite_link: {invite_link}\n"))
          
    except KeyError as e:
        logger.error(f"KeyError {format_exc()}")

        
    
    
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")

    
