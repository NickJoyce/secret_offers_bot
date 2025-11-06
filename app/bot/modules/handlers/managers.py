from aiogram import types, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile, InputMediaPhoto, InputMediaDocument
from aiogram.filters import Command, CommandStart, StateFilter
import logging.config
from app.bot.modules.middlewares.managers import AuthMiddleware
from app.database.queries.tg_managers import get_managers, update_manager, create_managers
from app.database.queries.tg_clients import get_clients
from app.database.queries.tg_newsletters import get_newsletter
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from app.bot.modules.keyboards.managers import settings_menu_callback, select_newsletter_callback, create_bot_newsletter_callback
from aiogram.exceptions import TelegramBadRequest
import asyncio
from app.bot.modules.utils import escape_markdown_v2
import pandas as pd



from app.conns.es.accounts import es
from datetime import datetime, timezone, date


import os
from settings import BASE_DIR, IS_AUTH

from app.database.conn import AsyncSessionLocal
from app.bot.main import bot


logger = logging.getLogger(__name__)

router = Router(name=__name__)


if IS_AUTH:
    router.message.middleware(AuthMiddleware())
    
    
class PostCreateStates(StatesGroup):
    post_data = State()
   
    
    
    
# Настройки пользователя
@router.message(Command('settings'))
async def settings_command_handler(msg: Message):
    await msg.answer(text="Настройки", reply_markup = await settings_menu_callback())


@router.callback_query(F.data == 'settings')
async def select_model(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="Настройки",
                                     reply_markup = await settings_menu_callback())
    
    
# Настройки пользователя -> Расссылки в канале
@router.callback_query(F.data == 'newsletters')
async def select_newsletter(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=f"Выберете рассылку",
                                     reply_markup = await select_newsletter_callback())


# Настройки пользователя -> Расссылки в боте
@router.callback_query(F.data == 'bot_newsletters')
async def select_bot_newsletter(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=f"Выберете действие",
                                     reply_markup = await create_bot_newsletter_callback())


@router.callback_query(F.data.startswith("create_bot_newsletter"), StateFilter(None))
async def get_selected_newsletter(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(PostCreateStates.post_data)
    await callback.message.answer(text=f"Создайте пост")
    

# --- Обработчик для получения данных для поста ---
@router.message(PostCreateStates.post_data)
async def process_post_data(request: Message, message: types.Message, state: FSMContext):
    logger.info(f"message: {request}")
    
    








@router.callback_query(F.data.startswith("create_bot_newsletter"))
async def get_selected_newsletter(callback: CallbackQuery):
    clients = await get_clients()
    selected_newsletter_id = int(callback.data.split('_')[2])
    newsletter = await get_newsletter(nl_id=selected_newsletter_id)
    # обработаем файл с id пользователей
    if newsletter.tg_ids:
        file_id = newsletter.tg_ids['file_id']
        df = pd.read_excel(f"{BASE_DIR}/app/uploads/attachment/{file_id}")
        logger.info(f"df: {df}")
        
        # получим список tg id из файла
        newsletters_client_tg_ids = [int(client.id) for client in df.itertuples()]

    else:
        await bot.send_message(chat_id=callback.message.chat.id, text=f"Не добавлен файл для рассылки")
        return
            

            

    
    
    await callback.answer(text=f"Рассылка запущена", show_alert=False)
    
    
    # Кол-во зарегестрированных пользователей в боте
    bot_clients_count = len(clients)
    # Кол-во пользователей в рассылке
    newsletter_clients_count = len(newsletters_client_tg_ids)
    # Кол-во пользователей, которым была отправлена рассылка
    sent_clients_count = 0

    
    for client in clients:
        logger.info(f"client: {client.tg_id}")
        if client.is_active and client.tg_id and client.tg_id in newsletters_client_tg_ids:
            try:
                
                # текст рассылки
                text = newsletter.text
                                       
                # Отправляем изображения 
                media_group = []
                try:
                    if newsletter.images:
                        for n, image in enumerate(newsletter.images, start=1):
                            image_id = image['file_id']
                            image_path = f"{BASE_DIR}/app/uploads/attachment/{image_id}"
                            if n == 1:
                                media_group.append(InputMediaPhoto(media=FSInputFile(image_path, filename=image['filename']), caption=text))
                            else:
                                media_group.append(InputMediaPhoto(media=FSInputFile(image_path, filename=image['filename'])))
                                
                        await bot.send_media_group(
                            chat_id=client.tg_id,
                            media=media_group
                        )
                except Exception as e:
                    logger.error(f"Ошибка при отправке изображений пользователю {client.tg_id}: {e}")
                    
                    
                # Файлы рассылки
                media_group = []
                try:
                    if newsletter.files:
                        for n, file_ in enumerate(newsletter.files, start=1):
                            file_id = file_['file_id']
                            file_path = f"{BASE_DIR}/app/uploads/attachment/{file_id}"
                            if n == 1:
                                media_group.append(InputMediaDocument(media=FSInputFile(file_path, filename=file_['filename'])))
                            else:
                                media_group.append(InputMediaDocument(media=FSInputFile(file_path, filename=file_['filename'])))
                    
                        data = await bot.send_media_group(
                            chat_id=client.tg_id,
                            media=media_group
                        )
                except Exception as e:
                    logger.error(f"Ошибка при отправке файла пользователю {client.tg_id}: {e}")
                        
                    

                # Кол-во пользователей, которым была отправлена рассылка
                sent_clients_count += 1
                
                
                successful_sends += 1
                await asyncio.sleep(0.05)
            except TelegramBadRequest as e:
                if "bot was blocked by the user" in str(e):
                    print(f"Пользователь {client.tg_id} заблокировал бота. Удалить из списка подписчиков.")
                else:
                    print(f"Ошибка при отправке сообщения пользователю {client.tg_id}: {e}")
            except Exception as e:
                print(f"Неизвестная ошибка при отправке сообщения пользователю {client.tg_id}: {e}")
    await bot.send_message(chat_id=callback.message.chat.id, 
                           text=(f"В боте: {bot_clients_count}"
                                 f"\nВ файле рассылки: {newsletter_clients_count}"
                                 f"\nОтправлено: {sent_clients_count}"
                                 f"\nНе отправлено: {newsletter_clients_count - sent_clients_count}"))  


@router.message(Command('info'))
async def settings_command_handler(msg: Message):
    text = (f"*Доступные команды*\n"
            "/info - Выводит список доступных команд\n"
            "/settings - Настройки. Выводит меню для управлением рассылками.\n\n"
            "*Админ панель*\n"
            "Клиенты:\n"
            "https://marketing-bot.podrugeapi.ru/admin/tg_user/list\n"
            "Менеджеры:\n"
            "https://marketing-bot.podrugeapi.ru/admin/tg_manager/list\n"
            "Рассылки:\n"
            "https://marketing-bot.podrugeapi.ru/admin/tg_newsletter/list")
    await msg.answer(escape_markdown_v2(text), parse_mode=ParseMode.MARKDOWN_V2)