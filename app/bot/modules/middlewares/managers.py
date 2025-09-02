from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, CallbackQuery
import logging.config
from app.database.queries.tg_managers import get_manager, update_manager, create_managers


logger = logging.getLogger(__name__)

class AuthMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[ [TelegramObject, Dict[str, Any]], Awaitable[Any] ],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        # Логика, которая выполняется ДО вызова обработчика
        logger.info(f"--- Manager Middleware: Processing event of type {type(event).__name__} ---")
        # Список ID пользователей, которым разрешен доступ из бд
        user = await get_manager(tg_id=event.from_user.id)
        if not user or not user.is_active:
            # Если пользователь не разрешен, отправляем сообщение и прерываем цепочку
            if isinstance(event, Message):
                await event.reply(f"Доступ для пользователя (id: {event.from_user.id}) запрещен")
            elif isinstance(event, CallbackQuery):
                await event.answer(f"Доступ для пользователя (id: {event.from_user.id}) запрещен", show_alert=True)
            return # Прерываем дальнейшую обработку 
        # Вызываем следующий обработчик в цепочке (это может быть другой middleware или конечный хендлер)
        result = await handler(event, data)
        # Логика, которая выполняется ПОСЛЕ вызова обработчика
        logger.info(f"--- Manager Middleware: Finished processing event of type {type(event).__name__} ---")
        return result








