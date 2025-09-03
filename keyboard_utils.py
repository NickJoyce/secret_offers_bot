from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot
import logging

logger = logging.getLogger(__name__)

async def remove_keyboard_without_message(bot: Bot, chat_id: int, message_id: int = None):
    """
    Удаляет ReplyKeyboard без отправки нового сообщения
    
    Args:
        bot: Экземпляр бота
        chat_id: ID чата
        message_id: ID сообщения для редактирования (опционально)
    """
    try:
        if message_id:
            # Редактируем существующее сообщение
            await bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            # Отправляем пустое сообщение с удалением клавиатуры
            await bot.send_message(
                chat_id=chat_id,
                text=" ",  # пробел вместо пустой строки
                reply_markup=ReplyKeyboardRemove()
            )
        logger.info(f"ReplyKeyboard удален для чата {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при удалении ReplyKeyboard: {e}")

async def remove_keyboard_silently(bot: Bot, chat_id: int):
    """
    Удаляет ReplyKeyboard "тихо" - отправляет пробел
    """
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=" ",  # пробел вместо пустой строки
            reply_markup=ReplyKeyboardRemove()
        )
        logger.info(f"ReplyKeyboard удален для чата {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при удалении ReplyKeyboard: {e}")

async def remove_keyboard_with_text(bot: Bot, chat_id: int, text: str = "Клавиатура убрана"):
    """
    Удаляет ReplyKeyboard с текстовым сообщением
    """
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=ReplyKeyboardRemove()
        )
        logger.info(f"ReplyKeyboard удален для чата {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при удалении ReplyKeyboard: {e}")

# Пример использования в обработчике
async def example_handler(message):
    """
    Пример обработчика, который удаляет клавиатуру
    """
    # Удаляем клавиатуру без отправки сообщения
    await remove_keyboard_silently(message.bot, message.chat.id)
    
    # Или можно просто:
    # await message.answer(" ", reply_markup=ReplyKeyboardRemove())
