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

        
        




        # Редактируем сообщение
        # await bot.edit_message_caption(
        #     chat_id=chat_id,
        #     message_id=message_id,
        #     caption='🎲Играем по-новым правиламм!\nВсе прошлые акции уже ушли в историю — но на их место пришло нечто особенное ✨\n\nУ тебя есть всего 7 дней, чтобы поймать новый бонус!\n\n📍Место действия: Москва, пр-т Вернадского 41, стр. 1\n🗓Срок: с 01.09 по 07.09\nА вот и список «бонусов» 👇\n\n💎BBL Forever Clear (лицо) — 9 540 ₽ вместо 15 900 ₽\n💎BBL Forever Young (лицо) — 17 940 ₽ вместо 29 900 ₽\n💎BBL Skin Tyte (лицо) — 11 940 ₽ вместо 19 900 ₽\n💎BBL Удаление пигментации и сосудов (лицо) — 10 140 ₽ вместо 16 900 ₽\n💎BBL Усиленная программа (лицо) — 14 940 ₽ вместо 24 900 ₽\n\n⏳Время пошло — осталось всего несколько дней, чтобы успеть.\n👇Жми на кнопку, выбирай свою процедуру и забирай скидку!',
        #     reply_markup= post_keyboard
        # )
       
       
        # photo_path = f"{BASE_DIR}/app/uploads/attachment/222.jpg"
        # photo_file = FSInputFile(photo_path)
       
        # отправляем сообщение c фото
        message = await bot.send_photo(chat_id=chat_id,
                                        photo=FSInputFile(photo_path),
                                        caption='![👍](tg://emoji?id=5368324170671202286)'+escape_markdown_v2(last_channel_post.caption),
                                        reply_markup=post_keyboard, 
                                        disable_notification=True,
                                        parse_mode=ParseModes.MARKDOWN_V2)
        message_id = message.message_id
        
        last_channel_post.message_id = message_id
        last_channel_post.chat_id = chat_id
        await update_channel_post(last_channel_post)
        
        
        
        
        # await sleep(3)
        
        # # редактируем сообщение: удаляем клавиатуру
        # await bot.edit_message_caption(
        #     chat_id=chat_id,
        #     message_id=message_id,
        #     caption=message_body,
        #     reply_markup= None
        # )

    
        return JSONResponse({"message_id": message_id})

    except Exception as e:
        return JSONResponse({'error': format_exc()})