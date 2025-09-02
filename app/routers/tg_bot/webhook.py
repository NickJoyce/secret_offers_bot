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


logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)



@router.post(WEBHOOK_PATH)
async def bot_webhook(request: Request, session: ClientSession = Depends(get_http_session)) -> None:

    request_data = await request.json()
    
    logger.info(f"request_data: {request_data}")
    
    # получаем tg_id из request_data
    try:
        tg_id = request_data['message']['from']['id']
        try:
            if request_data['message']['text'] == '/start':
                # запишем сообщение из тг в базу данных
                await create_first_start_messages([{'tg_id': tg_id, 'message': request_data}])
                logger.info(f"first start command from tg is saved")
        except KeyError:
            pass
    except KeyError:
        tg_id = request_data['callback_query']['from']['id']
    
    client = await get_client(tg_id=tg_id)

    logger.info(f"client: {client}")

        
    if client:
        # отправляем данные из tg в talk-me 
        first_start_message = await get_first_start_message(tg_id=tg_id)
        
        
        # существует ли инициированный диалог с клиентом в talk-me
        
        # отправляем данные для инициации диалога в talk-me
        if not first_start_message.is_sent:
            async with session.post(
                url="https://api.integracio.ru/json/anonymous/integration/event/telegram/i78u22rqbxteoy5t8f5vr7ogfmkjbwyb",
                json=first_start_message.message,
                timeout=30
            ) as response:
                logging.info(f"Статус пересылки данных в talk-me: {response.status}")  
                first_start_message.is_sent = True
                await update_first_start_message(first_start_message)
            await asyncio.sleep(1)

        
        async with session.post(
            url="https://api.integracio.ru/json/anonymous/integration/event/telegram/i78u22rqbxteoy5t8f5vr7ogfmkjbwyb",
            json=request_data,
            timeout=30
        ) as response:
            logging.info(f"Статус пересылки данных в talk-me: {response.status}")

        
    # обработка tg webhook
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")
    # return {"Status": "OK"}
    
