from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
import logging
from fastapi.templating import Jinja2Templates
from settings.base import TEMPLATES_DIR, BASE_DIR
from app.tasks.monitoring import is_subscriber
import traceback
from app.bot.main import bot
from traceback import format_exc
from app.bot.modules.keyboards.channels import post_keyboard
from asyncio import sleep
from aiogram.types import FSInputFile
from app.database.queries.tg_channels_post import get_channel_posts, get_last_channel_post, update_channel_post
from app.bot.modules.utils import ParseModes, escape_markdown_v2




logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/is_subscriber", include_in_schema=False)
async def is_subscriber(user_id: str, request: Request):
    try:
        chat_member = await bot.get_chat_member(chat_id='-1002525082412', user_id=user_id)
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
        chat_id = '-1003007138318'
        message_id = 80

        last_channel_post = await get_last_channel_post()
        
        photo_id = last_channel_post.photo['file_id']
        photo_path = f"{BASE_DIR}/app/uploads/attachment/{photo_id}"

        # отправляем сообщение c фото
        message = await bot.send_photo(chat_id=chat_id,
                                       photo=FSInputFile(photo_path),
                                       caption=escape_markdown_v2(last_channel_post.caption),
                                       reply_markup=post_keyboard,
                                       parse_mode=ParseModes.MARKDOWN_V2)
        message_id = message.message_id
        
        last_channel_post.message_id = message_id
        last_channel_post.chat_id = chat_id
        await update_channel_post(last_channel_post)
        
    

        await sleep(25)
        new_message = await bot.get_message(chat_id=last_channel_post.chat_id, message_id=last_channel_post.message_id)
        
    
        # редактируем сообщение: удаляем клавиатуру
        await new_message.edit_reply_markup(reply_markup=None)
        

    
        return JSONResponse({"message_id": message_id})

    except Exception as e:
        return JSONResponse({'error': format_exc()})