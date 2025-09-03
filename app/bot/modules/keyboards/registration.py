from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import logging.config
from app.database.queries.greeting_offers import get_greeting_offers


logger = logging.getLogger(__name__)


# Клавиатура с кнопкой для запроса контакта
request_contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поделиться номером телефона", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)



async def select_greeting_offer_callback():
    greeting_offers = await get_greeting_offers()
    builder = InlineKeyboardBuilder()
    for n, greeting_offer in enumerate(greeting_offers, start=1):
        text = f"{greeting_offer.name} {greeting_offer.old_price} → {greeting_offer.new_price}"
        builder.add(InlineKeyboardButton(text=text, callback_data=f"greeting_offer_choice_{greeting_offer.id}"))
    builder.add(InlineKeyboardButton(text="Поговорить с менеджером", callback_data="greeting_offer_choice_manager"))
    return builder.adjust(1).as_markup()






link_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [ReplyKeyboardRemove()]
        [InlineKeyboardButton(text="👉 Подписаться", url="https://www.google.com/")],

])