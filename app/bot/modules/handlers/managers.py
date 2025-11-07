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
from aiogram.types.message_entity import MessageEntity
from app.bot.modules.keyboards.registration import first_letters, cities_list
from app.bot.modules.keyboards.managers import yes_or_no_callback
from app.bot.modules.utils import CITIES, unique_first_letters




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
    text = State()
    caption = State()
    photo = State()
    entities = State()
    caption_entities = State()
    city = State()
    yes_or_no = State()
   
    
    
    
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
    state.clear()
    await callback.answer()
    await state.set_state(PostCreateStates.text)
    await callback.message.answer(text=f"Создайте пост")
    

# --- Обработчик для получения данных для поста ---
@router.message(PostCreateStates.text)
async def process_post_data(message: types.Message, state: FSMContext, ):
    text = message.text
    caption = message.caption
    photo = message.photo
    entities = message.entities
    caption_entities = message.caption_entities
    
    # logger.info(f"message: {message}")
    # logger.info(f"caption: {caption}")
    # logger.info(f"photo: {photo}")
    # logger.info(f"entities: {entities}")
    # logger.info(f"caption_entities: {caption_entities}")
    
    await state.update_data(text=text)
    await state.update_data(caption=caption)
    await state.update_data(photo=photo)
    await state.update_data(entities=entities)
    await state.update_data(caption_entities=caption_entities)
    
    # возвращаем пост
    if text:
        sent_message = await message.answer(escape_markdown_v2(f"{text}"), entities=entities, parse_mode=ParseMode.MARKDOWN_V2)
        logger.info(f"sent_message: {sent_message}")

    
    
    # если фото много
    if message.media_group_id:
        # получаем фото из media_group_id
        await state.clear()
        await message.answer(escape_markdown_v2(f"Добавлено более 1 фотографии. Состояние спрошено. Начните сначала"), parse_mode=ParseMode.MARKDOWN_V2)
        return
    # если фото одно
    else:
        if photo:
            await message.answer_photo(photo=photo[0].file_id, caption=escape_markdown_v2(caption), caption_entities=caption_entities, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            pass

    

    await state.set_state(PostCreateStates.city)
    
    await message.answer(
        f"Укажи первую букву названия города, в котором будет проходить рассылка 👇",
        reply_markup=await first_letters()
    )
        
   
@router.callback_query(F.data.startswith('first_letter_'))
async def process_first_letter(callback: CallbackQuery):
    letter = callback.data.split('_')[2]
    # получим список городов начинающихся на букву letter
    cities = [city for city in CITIES if city.startswith(letter)]
    
    await callback.answer()
    await callback.message.edit_text(text=f"Выбери город из списка:",
                                     reply_markup = await cities_list(cities))
   
   
   
@router.callback_query(F.data.startswith('selected_city_'), PostCreateStates.city)
async def process_selected_city(callback: CallbackQuery, state: FSMContext):
    city = callback.data.split('_')[2]
    await state.update_data(city=city)
    await callback.message.edit_text(
    f"Запустить рассылку ☝️ в городе {city}?",
        reply_markup=await yes_or_no_callback()
    ) 
    
    
    await state.set_state(PostCreateStates.yes_or_no)
    
    state.clear()
    
    
@router.callback_query(F.data.startswith('yes_or_no_'), PostCreateStates.yes_or_no)
async def process_yes_no(callback: CallbackQuery, state: FSMContext):
    yes_or_no = callback.data.split('_')[3]
    await state.update_data(yes_or_no=yes_or_no)
    data = await state.get_data()
    city = data.get('city')
    logger.info(f"data: {data}")

    if yes_or_no == 'yes':
        await state.clear()
        await callback.message.answer(text=f"Рассылка в городе {city} запущена")
        return
    else:
        await state.clear()
        await callback.message.answer(text=f"Рассылкав городе {city} не запущена")
        return

    

    # формируем медиа группу
    # media_group = []
    # if photos:
    #     photo_ids = [p.file_id for p in photos][:1]
    #     logger.info(f"photo_ids: {photo_ids}")
    #     for n, photo_id in enumerate(photo_ids):
    #         if n == 0:
    #             media_group.append(InputMediaPhoto(media=photo_id, caption=caption))
    #         else:
    #             media_group.append(InputMediaPhoto(media=photo_id))

    # if media_group:
    #     await message.answer_media_group(media=media_group)
    
    
    # await message.answer_photo(photo=photo, caption=caption)
    
    
    
    # сбрасываем состояние

    
    
    
    








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