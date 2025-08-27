from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
import logging
from fastapi.templating import Jinja2Templates
from settings.base import TEMPLATES_DIR
from aiogram.types import Update
from app.bot.main import bot, dp
from settings import TALK_ME_BASE_WEBHOOKS_PATH
from fastapi import Depends
from aiohttp import ClientSession
from app.utils.dependencies import get_http_session
from app.database.queries.tg_clients import get_client
from app.database.queries.talk_me_messages_from_client import create_talk_me_messages_from_client
import json
from app.conns.talk_me.accounts import talk_me


logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.post(f"{TALK_ME_BASE_WEBHOOKS_PATH}/new-message-from-client")
async def new_message_from_client(request: Request, 
                                  session: ClientSession = Depends(get_http_session)) -> None:
    data = await request.json()
    
    # данные из talk-me для идентификации диалога
    talk_me_search_id = data['client']['searchId']
    talk_me_client_id = data['client']['clientId']
    talk_me_tg_id = data['client']['source']['data']['id']
    
    # записываем Сообщение от клиента полученное от TALK-ME в бд
    talk_me_message_from_client_data = {
        "tg_id": int(talk_me_tg_id),
        "search_id": int(talk_me_search_id),
        "client_id": talk_me_client_id,
        "webhook_data": json.dumps(data)
    }
    await create_talk_me_messages_from_client([talk_me_message_from_client_data])

    
    
    
    
    # # получаем клиента приложения из бд
    # app_client = await get_client(tg_id=int(talk_me_tg_id))
    
    # if app_client and not app_client.talk_me_client_id and not app_client.talk_me_search_id:
    #     ...
    #     # записываем search_id и client_id для данного пользователя приложения
    
    
    logging.info(f"search_id: {talk_me_search_id}")
    logging.info(f"client_id: {talk_me_client_id}")
    logging.info(f"tg_client_id: {talk_me_tg_id}")
    # logging.info(f"app_client: {app_client}")
    logging.info(f"Received new message from client webhook (talk-me): {data}")
