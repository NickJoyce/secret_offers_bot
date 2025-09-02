from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from app.database.queries.tg_newsletters import get_newsletters
import logging.config


logger = logging.getLogger(__name__)


settings_menu = [('Рассылки', 'newsletters')]


async def settings_menu_callback():
    builder = InlineKeyboardBuilder()
    for text, data in settings_menu:
        builder.add(InlineKeyboardButton(text=text, callback_data=data))
    return builder.adjust(2).as_markup()



async def select_newsletter_callback():
    newsletters = await get_newsletters()
    builder = InlineKeyboardBuilder()
    for newsletter in newsletters:
        text = f"{newsletter.name}"
        builder.add(InlineKeyboardButton(text=text, callback_data=f"newsletter_choice_{newsletter.id}"))
    builder.add(InlineKeyboardButton(text='<< Настройки', callback_data='settings'))
    return builder.adjust(2).as_markup()