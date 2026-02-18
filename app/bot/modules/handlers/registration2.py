from datetime import datetime, timedelta
from aiogram import types, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter
import logging.config
from app.database.queries.tg_clients import get_client, update_client, create_clients
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from app.bot.modules.keyboards.registration import request_contact_keyboard, select_greeting_offer_callback, link_kb, first_letters, cities_list
from app.bot.modules.utils import escape_markdown_v2
from app.database.queries.greeting_offers import get_greeting_offer
from app.conns.talk_me.accounts import talk_me
from app.database.queries.talk_me_messages_from_client import get_client_id
from asyncio import sleep
from zoneinfo import ZoneInfo
import pytz
from app.tasks.monitoring import is_subscriber
from app.bot.modules.utils import unique_first_letters, CITIES
from aiogram.utils.markdown import link, hlink
from app.bot.modules.utils import escape_markdown_v2
from app.database.queries.tg_deeplinks import get_deeplink
from app.tasks.monitoring import add_step_to_deeplink_request_task
from app.bot.modules.utils import create_deeplink_request, RegistrationSteps
import json
from app.database.queries.tg_deeplink_requests import add_step_to_deeplink_request
from app.database.queries.tg_deeplink_requests import aupdate_deeplink_request
from copy import deepcopy
from app.bot.main import send_message_to_admin


from settings import TG_CHANNEL_ID






from app.conns.es.accounts import es
from datetime import datetime, timezone, date, time


import os
from settings import BASE_DIR, IS_AUTH,  PRIVACY_POLICY_URL

from app.database.conn import AsyncSessionLocal
from app.bot.main import bot


logger = logging.getLogger(__name__)

router = Router(name=__name__)



class RegistrationStates(StatesGroup):
    tg_id = State()
    reg_name = State()  
    reg_phone = State()
    tg_username = State()
    tg_first_name = State()
    tg_last_name = State()
    city = State()
    deeplink_request_id = State()
    is_registred = State()
    
    

    


@router.message(CommandStart(), StateFilter(None))
async def start_command_handler(msg: Message, state: FSMContext):
    # сбрасываем состояние
    await state.clear()
    
    # получаем текущую дату и время поступления данных
    received_at = datetime.now()

    
    # проверяем есть ли пользователь в базе данных
    user = await get_client(tg_id=msg.from_user.id)
    
    # Сохраняем is_registred в контекст FSM
    is_registred = True if user else False
    await state.update_data(is_registred=is_registred)
    
    
    # подтягиваем соответсвуюй диплинк и записываем deeplink_request
    deeplink_request = None
    registration_steps = json.dumps({"data": [RegistrationSteps.START_COMMAND_RECEIVED.value]}, ensure_ascii=False)
    try:
        deeplink_id = int(msg.text.split(' ')[1])
    except IndexError:
        DEEPLINK_WITHOUT_PARAMS_ID = 16
        # создаем объект DeeplinkRequest без параметров (должен быть в базе с этим id) БЕЗ celery, в синхронном режиме
        # create_deeplink_request_task.delay(received_at=received_at, deeplink_id=DEEPLINK_WITHOUT_PARAMS_ID, tg_id=msg.from_user.id)
        logger.info(f"create_deeplink_request data: {DEEPLINK_WITHOUT_PARAMS_ID}, {msg.from_user.id}, {received_at}")
        deeplink_request = await create_deeplink_request(deeplink_id=DEEPLINK_WITHOUT_PARAMS_ID,
                                                         tg_id=msg.from_user.id, 
                                                         received_at=received_at,
                                                         registration_steps=registration_steps,
                                                         is_registred=is_registred)
        deeplink_id = None
        
    if deeplink_id:
        deeplink = await get_deeplink(id_=deeplink_id)
        if deeplink:
            # создаем объект DeeplinkRequest без параметров (должен быть в базе с этим id) БЕЗ celery, в синхронном режиме
            # create_deeplink_request_task.delay(received_at=received_at, deeplink_id=deeplink.id, tg_id=msg.from_user.id)
            deeplink_request = await create_deeplink_request(deeplink_id=deeplink.id, 
                                                             tg_id=msg.from_user.id, 
                                                             received_at=received_at,
                                                             registration_steps=registration_steps,
                                                             is_registred=is_registred)
    
    # Сохраняем deeplink_request_id в контекст FSM
    await state.update_data(deeplink_request_id=deeplink_request.id if deeplink_request else None)

    

    if user:
        if user.is_active:
            await msg.answer(
            "Привет! Добро пожаловать в бот",
        )
        else:
            await msg.answer(
                "Ошибка подключения к боту. Пожалуйста, обратитесь к администратору",
            )
    else:
        await state.set_state(RegistrationStates.reg_name)

        text = f"""👋 Добро пожаловать в ЗАКРЫТЫЙ КЛУБ «ПОДРУЖКИ»

Это закрытый Telegram-канал от крупнейшей сети клиник лазерной эпиляции и косметологии Подружки, в котором мы делимся секретными скидками на самые популярные услуги сети

Только здесь ты сможешь записаться на RF-лифтинг,  лазерную эпиляцию и самую желанную процедуру 2025 года BBL Forever Young со скидками до 70%!  

👉 Чтобы продолжить и получить доступ к каналу, нужно зарегистрироваться. Отправляя форму ты даешь согласие на обработку <a href="{PRIVACY_POLICY_URL}">персональных данных</a>. 

Напиши, как тебя зовут:"""
        await msg.answer(text=text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        
    
   


# --- Обработчик для получения промокода---
# @router.message(RegistrationStates.promocode)
# async def process_promocode(message: types.Message, state: FSMContext):
#     promocode = message.text
#     # выполняем проверку промокода
#     # Сохраняем промокод в контекст FSM
#     await state.update_data(promocode=promocode)
#     # Переходим к следующему состоянию
#     await state.set_state(RegistrationStates.reg_name)
    
#     await message.answer(
#         f"Промокод принят! Напиши, как тебя зовут:",




# --- Обработчик для получения имени пользователя ---
@router.message(RegistrationStates.reg_name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    # Сохраняем имя в контекст FSM
    await state.update_data(reg_name=user_name)
    
    # добавим статус к диплинку
    # Получаем все собранные данные
    user_data = await state.get_data()
    if  user_data.get('deeplink_request_id'):
        # Запишем статус NAME_INPUT_RECEIVED (фоновая задача celery)
        add_step_to_deeplink_request_task.delay(id_=user_data.get('deeplink_request_id'), step=RegistrationSteps.NAME_INPUT.value)


    # Переходим к следующему состоянию
    await state.set_state(RegistrationStates.reg_phone)
    

        
    
    
    
    await message.answer(
        f"Отлично, {user_name}! Теперь, пожалуйста, поделись своим номером телефона, нажав на кнопку ниже 👇",
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
    
        else:
            await message.answer("Пожалуйста, поделитесь своим собственным номером телефона, нажав на кнопку")
            return    
    else:
        await message.answer("Не удалось получить номер телефона. Пожалуйста, используйте кнопку ниже")
        return      

    # добавим статус к диплинку
    # Получаем все собранные данные
    user_data = await state.get_data()
    if  user_data.get('deeplink_request_id'):
        # Запишем статус (фоновая задача celery)
        add_step_to_deeplink_request_task.delay(id_=user_data.get('deeplink_request_id'), step=RegistrationSteps.PHONE_INPUT.value)



    await state.set_state(RegistrationStates.city)
    
    await message.answer(
        f"Укажи первую букву названия города, в котором планируется посещение 👇",
        reply_markup=await first_letters()
    )


@router.callback_query(F.data.startswith('first_letter_'))
async def process_first_letter(callback: CallbackQuery, state: FSMContext):
    letter = callback.data.split('_')[2]
    # получим список городов начинающихся на букву letter
    cities = [city for city in CITIES if city.startswith(letter)]
    
    # добавим статус к диплинку
    # Получаем все собранные данные
    user_data = await state.get_data()
    if  user_data.get('deeplink_request_id'):
        # Запишем статус (фоновая задача celery)
        add_step_to_deeplink_request_task.delay(id_=user_data.get('deeplink_request_id'), step=RegistrationSteps.CITY_FIRST_LETTER_RECEIVED.value)
    
    
    await callback.answer()
    await callback.message.edit_text(text=f"Выбери город из списка:",
                                     reply_markup = await cities_list(cities))
    

@router.callback_query(F.data.startswith('selected_city_'), RegistrationStates.city)
async def process_selected_city(callback: CallbackQuery, state: FSMContext):
    city = callback.data.split('_')[2]
    await state.update_data(city=city)
    
    # добавим статус к диплинку
    # Получаем все собранные данные
    user_data = await state.get_data()
    if  user_data.get('deeplink_request_id'):
        # Запишем статус (фоновая задача celery)
        add_step_to_deeplink_request_task.delay(id_=user_data.get('deeplink_request_id'), step=RegistrationSteps.CITY_RECEIVED.value)
    # await callback.answer(text=f"data {await state.get_data()}", show_alert=False)
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
        'city': user_data.get('city') if user_data.get('city') else '',
    }
    # Записываем в базу данных
    await create_clients([user])
    deeplink_request_id = deepcopy(user_data.get('deeplink_request_id'))
    if  deeplink_request_id:
        # Запишем статус  (фоновая задача celery)
        add_step_to_deeplink_request_task.delay(id_=deeplink_request_id, step=RegistrationSteps.WRITTEN_TO_DB.value)
    
    # сбрасываем состояние
    await state.clear()
        
    await callback.message.answer(text=f"🩷 Регистрация прошла успешно!",
                                  reply_markup = types.ReplyKeyboardRemove())
    
    
    # генерируем ссылку на закрытый канал
    expire_hours = 24
    member_limit = 1
    link = await bot.create_chat_invite_link(
        chat_id=TG_CHANNEL_ID,
        name="Промо ссылка",           
        expire_date=datetime.now() + timedelta(hours=expire_hours), 
        member_limit=member_limit,            
        creates_join_request=False      
    )
    
    await aupdate_deeplink_request(deeplink_request_id=deeplink_request_id, update_data={"invite_link": link.invite_link})
    
    await send_message_to_admin(f"Промо ссылка\n"
                                f"expire_hours: {expire_hours}\n"
                                f"member_limit: {member_limit}\n"
                                f"link: {link.invite_link}\n"
                                f"invite link is updated for deeplink_request_id: {deeplink_request_id}"
                                )
    
    await callback.message.answer("""Вот твоя персональная ссылка-приглашение в канал: 

Подписывайся, не пропускай публикации и добро пожаловать в КЛУБ 💘"""
                                , reply_markup=link_kb)
    
    if deeplink_request_id:
        # Запишем статус (фоновая задача celery)
        add_step_to_deeplink_request_task.delay(id_=deeplink_request_id, step=RegistrationSteps.LINK_SENT.value)
        
    
    
    









        
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

    