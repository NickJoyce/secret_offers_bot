from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import logging.config
from app.database.queries.greeting_offers import get_greeting_offers
from app.bot.modules.utils import unique_first_letters

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
        [InlineKeyboardButton(text="👉 Подписаться", url="https://t.me/+uZjXQYiEkC9iMGFi")],

])

# Клавиатура для записи в Telegram и WhatsApp
registration_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Записаться сейчас в TG", url="http://t.me/podruge_close_club_direct_bot")],
        [InlineKeyboardButton(text="Записаться сейчас в WA", url="https://wa.me/79672121788")]
    ]
)

# Альтернативная версия с использованием InlineKeyboardBuilder
def create_registration_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Записаться сейчас в TG", url="http://t.me/podruge_close_club_direct_bot"))
    builder.add(InlineKeyboardButton(text="Записаться сейчас в WA", url="https://wa.me/79672121788"))
    return builder.adjust(1).as_markup()




async def first_letters():
    builder = InlineKeyboardBuilder()
    for letter in unique_first_letters:
        builder.add(InlineKeyboardButton(text=letter, callback_data=f"first_letter_{letter}"))
    return builder.adjust(5).as_markup()


async def cities_list(cities):
    builder = InlineKeyboardBuilder()
    for city in cities:
        builder.add(InlineKeyboardButton(text=city, callback_data=f"selected_city_{city}"))
    
    return builder.adjust(2).as_markup()