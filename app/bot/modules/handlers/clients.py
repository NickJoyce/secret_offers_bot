from aiogram import types, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter
import logging.config
from app.bot.modules.middlewares.clients import AuthMiddleware, BlackListMiddleware
from app.database.queries.tg_clients import get_clients, update_client, create_clients
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext

from app.conns.es.accounts import es
from datetime import datetime, timezone, date


import os
from settings import BASE_DIR, IS_AUTH, IS_BLACK_LIST

from app.database.conn import AsyncSessionLocal
from app.bot.main import bot


logger = logging.getLogger(__name__)

router = Router(name=__name__)


if IS_AUTH:
    router.message.middleware(AuthMiddleware())

# if IS_BLACK_LIST:
#     router.message.middleware(BlackListMiddleware())
    
    

# @router.message(F.text)
# async def message_handler(msg: Message):
#     await msg.answer(f"Have a nice day!")