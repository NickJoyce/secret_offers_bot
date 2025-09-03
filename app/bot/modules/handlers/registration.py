from aiogram import types, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter
import logging.config
from app.database.queries.tg_clients import get_client, update_client, create_clients
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from app.bot.modules.keyboards.registration import request_contact_keyboard, select_greeting_offer_callback
from app.bot.modules.utils import escape_markdown_v2
from app.database.queries.greeting_offers import get_greeting_offer
from app.conns.talk_me.accounts import talk_me
from app.database.queries.talk_me_messages_from_client import get_client_id
from asyncio import sleep
from zoneinfo import ZoneInfo
import pytz
from app.tasks.monitoring import is_subscriber




from app.conns.es.accounts import es
from datetime import datetime, timezone, date, time


import os
from settings import BASE_DIR, IS_AUTH

from app.database.conn import AsyncSessionLocal
from app.bot.main import bot


logger = logging.getLogger(__name__)

router = Router(name=__name__)


# if IS_AUTH:
#     router.message.middleware(AuthMiddleware())



class RegistrationStates(StatesGroup):
    tg_id = State()
    reg_name = State()  
    reg_phone = State()
    tg_username = State()
    tg_first_name = State()
    tg_last_name = State()

    


@router.message(CommandStart(), StateFilter(None))
async def start_command_handler(msg: Message, state: FSMContext):
    # проверяем есть ли пользователь в базе данных
    user = await get_client(tg_id=msg.from_user.id)
    if user:
        if user.is_active:
            await msg.answer(
            "Привет! Добро пожаловать в бот",
        )
        else:
            await msg.answer(
                "Ваш аккаунт заблокирован. Пожалуйста, обратитесь к администратору",
            )
    else:
        await state.set_state(RegistrationStates.reg_name)
        await msg.answer(
            "Привет! Давайте зарегистрируемся. Как вас зовут?",
        )
    
   


# --- Обработчик для получения имени пользователя ---
@router.message(RegistrationStates.reg_name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    # Сохраняем имя в контекст FSM
    await state.update_data(reg_name=user_name)
    # Переходим к следующему состоянию
    await state.set_state(RegistrationStates.reg_phone)
    
    await message.answer(
        f"Отлично, {user_name}! Теперь, пожалуйста, поделитесь своим номером телефона, нажав на кнопку ниже.",
        reply_markup=request_contact_keyboard
    )
    

@router.message(RegistrationStates.reg_phone)
async def process_phone(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.CONTACT:
        phone_number = message.contact.phone_number
        user_id_from_contact = message.contact.user_id
        if user_id_from_contact == message.from_user.id:
            await state.update_data(reg_phone=phone_number)
            await state.update_data(tg_id=message.from_user.id)
            await state.update_data(tg_username=message.from_user.username)
            await state.update_data(tg_first_name=message.from_user.first_name)
            await state.update_data(tg_last_name=message.from_user.last_name)
    
            # Получаем все собранные данные
            user_data = await state.get_data()
            user = {
                "timestamp": datetime.now(ZoneInfo("Europe/Moscow")).isoformat(timespec='seconds'),
                'tg_id': user_data.get('tg_id'),
                'reg_name': user_data.get('reg_name') if user_data.get('reg_name') else '',
                'reg_phone': user_data.get('reg_phone') if user_data.get('reg_phone') else '',
                'tg_username': user_data.get('tg_username') if user_data.get('tg_username') else '',
                'tg_first_name': user_data.get('tg_first_name') if user_data.get('tg_first_name') else '',
                'tg_last_name': user_data.get('tg_last_name') if user_data.get('tg_last_name') else '',
            }
            # Записываем в базу данных
            await create_clients([user])
            
            
            # send to es index: marketing-bot-registration
            # try:
            #     user['tg_id'] = str(user['tg_id'])
            #     await es.create_document(index_name='marketing-bot-registration', document=user)
            # except Exception as e:
            #     logger.error(f"Error creating document in Elasticsearch: {e}")
                 
            
            
            await message.answer(
                f"Спасибо за регистрацию! Ваши данные сохранены",
                # Убираем клавиатуру после завершения
                reply_markup=types.ReplyKeyboardRemove() 
            )
            # Сбрасываем состояние, завершая регистрацию
            await state.clear()
            
            
            
            await message.reply('<a href="https://vk.com/id41732290">VK</a>', parse_mode="HTML")
            
            # Отправляем сообщение и сслки на закрытый канал
            await message.answer_photo(
                photo="https://marketing-bot.podrugeapi.ru/static/img/b905423b-962b-4c78-95f0-96bdfe39b8cc.jpeg",
                caption=escape_markdown_v2("""
                Специально для вас мы подготовили несколько преветственных предложений! 
                """),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup = await select_greeting_offer_callback()
            )
            
            
            await message.reply('<a href="https://vk.com/id41732290">VK</a>',parse_mode="HTML")
            
            
            await message.answer_photo(
                photo="https://marketing-bot.podrugeapi.ru/static/img/b905423b-962b-4c78-95f0-96bdfe39b8cc.jpeg",
                caption=escape_markdown_v2("""
                Специально для вас мы подготовили несколько преветственных предложений! 
                """),
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup = await select_greeting_offer_callback()
            )
            
            # await message.answer(text="оформить заказ", reply_markup = await select_greeting_offer_callback())
            
            
        else:
            await message.answer("Пожалуйста, поделитесь своим собственным номером телефона, нажав на кнопку")
            return
    else:
        await message.answer("Не удалось получить номер телефона. Пожалуйста, используйте кнопку ниже")
        return
        

        
@router.callback_query(F.data.startswith("greeting_offer_choice_"))
async def get_selected_greeting_offer(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await get_client(tg_id=user_id)
    user_data = {
            "tg_id": str(user.tg_id),
            "reg_name": user.reg_name,
            "reg_phone": user.reg_phone,
            "tg_username": user.tg_username,
            "tg_first_name": user.tg_first_name,
            "tg_last_name": user.tg_last_name,
        }
    # получаем client_id talk-me из базы данных (последняя запись по полю created_at в таблице talk_me_messages_from_client)
    for i in range(5):
        client_id = await get_client_id(tg_id=user.tg_id)
        logger.info(f"[try {i}] talk-me client_id: {client_id}")
        if client_id:
            break
        else:
            await sleep(1)    
    
    
    
    
    if callback.data.split('_')[3] == 'manager':
        bot_msg = f"Менеджер ответит Вам в ближайшие несколько минут"
        await bot.send_message(chat_id=callback.message.chat.id, 
                               text=escape_markdown_v2(bot_msg), 
                               parse_mode=ParseMode.MARKDOWN_V2)
        
        await callback.answer()
        response = await talk_me.send_message_to_operator(client_id=client_id, 
                                                text=(
                                    f"[ Нажата кнопка Позвать менеджера ]\n"
                                    f"[ Автоответ бота: {bot_msg} ]\n"
                                    f"[ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ ]\n"
                                    f"Имя: {user.reg_name}\n"
                                    f"Телефон: {user.reg_phone}\n"
                                    ))
        logger.info(f"talk-me response send_message_to_operator: {response}")
        
        # send to es index: marketing-bot-manager-button
        index_name = 'marketing-bot-manager-button'
        try:
            ts = {
                "timestamp": datetime.now(ZoneInfo("Europe/Moscow")).isoformat(timespec='seconds')
            }
            await es.create_document(index_name=index_name, document= {**ts, **user_data})
        except Exception as e:
            logger.error(f"Error creating document in Elasticsearch (index name: {index_name}): {e}")
        
        
        
    else:
        greeting_offer_id = int(callback.data.split('_')[3])
        greeting_offer = await get_greeting_offer(offer_id=greeting_offer_id)
        general_data = {
            "user": user_data,
            "greeting_offer": {
                "id": str(greeting_offer.id),
                "name": greeting_offer.name,
                "old_price": str(greeting_offer.old_price),
                "new_price": str(greeting_offer.new_price),
                "equipment": greeting_offer.equipment,
            }
        }
        
        bot_msg = f"Заявка на услугу *{greeting_offer.name}* оформлена. Спасибо!"
        await bot.send_message(chat_id=callback.message.chat.id, 
                            text=escape_markdown_v2(bot_msg), 
                            parse_mode=ParseMode.MARKDOWN_V2)
        
        await callback.answer()
        
        # отправка заказа оператору в talk-me
        response = await talk_me.send_message_to_operator(client_id=client_id, 
                                                        text=(
                                            f"[ Нажата кнопка выбора приветсвенного предложения ]\n"
                                            f"[ Автоответ бота: {bot_msg} ]\n"
                                            f"[ ЗАЯВКА ]\n"
                                            f"Имя: {user.reg_name}\n"
                                            f"Телефон: {user.reg_phone}\n"
                                            f"Услуга: {greeting_offer.name}\n"
                                            f"Старая цена: {greeting_offer.old_price}\n"
                                            f"Новая цена: {greeting_offer.new_price}\n"
                                            ))
        logger.info(f"talk-me response send_message_to_operator: {response}")
        
        
        # send to es index: marketing-bot-greeting-offer-buttons
        index_name = 'marketing-bot-greeting-offer-buttons'
        try:
            ts = {
                "timestamp": datetime.now(ZoneInfo("Europe/Moscow")).isoformat(timespec='seconds')
            }
            await es.create_document(index_name=index_name, document= {**ts, **general_data})
        except Exception as e:
            logger.error(f"Error creating document in Elasticsearch (index name: {index_name}): {e}")

    