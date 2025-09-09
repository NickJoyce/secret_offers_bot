from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



post_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Записаться сейчас в TG", url="http://t.me/podruge_close_club_direct_bot")],
        [InlineKeyboardButton(text="Записаться сейчас в WA", url="https://wa.me/79672121788")]
    ]
)