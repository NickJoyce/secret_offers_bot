from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, CallbackQuery
import logging.config
from app.database.queries.tg_clients import get_client, update_client, create_clients


logger = logging.getLogger(__name__)

class AuthMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[ [TelegramObject, Dict[str, Any]], Awaitable[Any] ],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        # Логика, которая выполняется ДО вызова обработчика
        logger.info(f"--- Universal Middleware: Processing event of type {type(event).__name__} ---")
        # Список ID пользователей, которым разрешен доступ из бд
        user = await get_client(tg_id=event.from_user.id)
        if not user or not user.is_active:
            # Если пользователь не разрешен, отправляем сообщение и прерываем цепочку
            if isinstance(event, Message):
                await event.reply(f"Доступ для пользователя (id: {event.from_user.id}) запрещен\n\n"
                                    f"Пожалуйста зарегестрируйтесь, выполнив команду /start")
            elif isinstance(event, CallbackQuery):
                await event.answer(f"Доступ для пользователя (id: {event.from_user.id}) запрещен\n\n"
                                    f"Пожалуйста зарегестрируйтесь, выполнив команду /start", show_alert=True)
            return # Прерываем дальнейшую обработку 
        # Вызываем следующий обработчик в цепочке (это может быть другой middleware или конечный хендлер)
        result = await handler(event, data)
        # Логика, которая выполняется ПОСЛЕ вызова обработчика
        logger.info(f"--- Universal Middleware: Finished processing event of type {type(event).__name__} ---")
        return result








