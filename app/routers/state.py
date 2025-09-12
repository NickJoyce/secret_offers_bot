from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
import logging
from fastapi.templating import Jinja2Templates
from settings.base import TEMPLATES_DIR, BASE_DIR, TG_CHANNEL_ID
from app.tasks.monitoring import is_subscriber
import traceback
from app.bot.main import bot
from traceback import format_exc
from app.bot.modules.keyboards.channels import post_keyboard
from asyncio import sleep
from aiogram.types import FSInputFile
from app.database.queries.tg_channels_post import get_channel_posts, get_last_channel_post, update_channel_post
from app.bot.modules.utils import ParseModes, escape_markdown_v2
from app.database.queries.tg_clients import get_clients
from app.database.queries.promocodes import create_promocodes, get_promocode
from datetime import datetime, timedelta
import traceback
import random
import string
from app.utils.main import generate_promocode



logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)



@router.get("/is_subscriber", include_in_schema=False)
async def is_subscriber(user_id: str, request: Request):
    try:
        chat_member = await bot.get_chat_member(chat_id=TG_CHANNEL_ID, user_id=user_id)
        logger.info(dict(chat_member))
        status = dict(chat_member)['status']
        if status != 'left':
            # return HTMLResponse(content=f'Участник {user_id} все еще в группе. status: {status}')
            return JSONResponse({'is_subscriber': True})
        else:
            # return HTMLResponse(content=f'Участник {user_id} покинул группу. status: {status}')
            return JSONResponse({'is_subscriber': False})

    except Exception as e:
        return JSONResponse({'is_subscriber': None})






@router.get("/manage-channel-post", include_in_schema=False)
async def manage_channel_post(request: Request):
    try:
        last_channel_post = await get_last_channel_post()
        
        photo_id = last_channel_post.photo['file_id']
        photo_path = f"{BASE_DIR}/app/uploads/attachment/{photo_id}"

        # отправляем сообщение c фото
        message = await bot.send_photo(chat_id=TG_CHANNEL_ID,
                                       photo=FSInputFile(photo_path),
                                       caption=escape_markdown_v2(last_channel_post.caption),
                                       reply_markup=post_keyboard,
                                       parse_mode=ParseModes.MARKDOWN_V2)
        message_id = message.message_id
        last_channel_post.message_id = message_id
        last_channel_post.chat_id = TG_CHANNEL_ID
        await update_channel_post(last_channel_post)
        return JSONResponse({"message_id": message_id})
    except Exception as e:
        return JSONResponse({'error': format_exc()})
    
    
@router.get("/link-gen", include_in_schema=False)
async def link_gen(request: Request):
    try:
    # получим текущих пользователей
        clients = await get_clients()
        for client in clients:
            if client.is_active:
                promocodes = []
                expire_date = datetime.now() + timedelta(days=1)
                await bot.send_message(text=escape_markdown_v2("Поделитесь ссылкой на закрытый канал"), 
                                           chat_id=client.tg_id, 
                                           parse_mode=ParseModes.MARKDOWN_V2)
                for i in range(2):
                    value = generate_promocode(length=10)
                    
                    is_unique = await get_promocode(value=value)
                    logger.info(f"is_unique: {is_unique}")
                    
                    
                    
                    link = await bot.create_chat_invite_link(chat_id=TG_CHANNEL_ID, expire_date=expire_date, member_limit=1)
                    promocode =  {
                        "client_id": client.id,
                        "value": value,
                        "link": link.invite_link,
                        "expire_date": expire_date,
                    }
                    promocodes.append(promocode)
                    text = f"Пройдите регистрацию в боте @secret_offers_bot и получите сслыку на закрытый канал с лучшими предложениями. \n Ваш индивидуальный промокод: `{promocode['value']}`" 
                    await bot.send_message(text=escape_markdown_v2(text), 
                                           chat_id=client.tg_id, 
                                           parse_mode=ParseModes.MARKDOWN_V2)
                await create_promocodes(promocodes)
        return JSONResponse({"success": "Промокоды успешно созданы"})
    except Exception as e:
        return JSONResponse({'error': format_exc()})   
    

    
@router.get("/delete-buttons", include_in_schema=False)
async def delete_buttons(request: Request):
    try:
        last_channel_post = await get_last_channel_post()
        if last_channel_post.buttons_expiration and not last_channel_post.is_buttons_deleted and last_channel_post.buttons_expiration < datetime.now():
            await bot.edit_message_reply_markup(chat_id=last_channel_post.chat_id, message_id=last_channel_post.message_id, reply_markup=None)
            last_channel_post.is_buttons_deleted = True
            await update_channel_post(last_channel_post)
            return JSONResponse({"result": "buttons deleted"})
    except Exception as e:
        return JSONResponse({"error": format_exc()})


        