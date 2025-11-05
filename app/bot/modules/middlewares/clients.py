from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, CallbackQuery
import logging.config
from app.database.queries.tg_clients import get_client, update_client, create_clients
from app.database.queries.balck_list import get_black_list


logger = logging.getLogger(__name__)

class AuthMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[ [TelegramObject, Dict[str, Any]], Awaitable[Any] ],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        # Логика, которая выполняется ДО вызова обработчика
        logger.info(f"--- Black List Middleware: Processing event of type {type(event).__name__} ---")
        black_list = await get_black_list()
        ids = [user.tg_id for user in black_list if user.tg_id is not None]
        usernames = [user.tg_username for user in black_list if user.tg_username is not None]
        
        if event.from_user.id in ids or event.from_user.username in usernames:
            # Если пользователь не разрешен, отправляем сообщение и прерываем цепочку
            if isinstance(event, Message):
                await event.reply(f"Ошибка подключения к боту (error code: blmw)")
            elif isinstance(event, CallbackQuery):
                await event.answer(f"Ошибка подключения к боту (error code: blmw)", show_alert=True)
            return # Прерываем дальнейшую обработку 
        
        # Вызываем следующий обработчик в цепочке (это может быть другой middleware или конечный хендлер)
        result = await handler(event, data)
        # Логика, которая выполняется ПОСЛЕ вызова обработчика
        logger.info(f"--- Black List Middleware: Finished processing event of type {type(event).__name__} ---")
        return result  


class BlackListMiddleware(BaseMiddleware):
        async def __call__(self,
                       handler: Callable[ [TelegramObject, Dict[str, Any]], Awaitable[Any] ],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
            # Логика, которая выполняется ДО вызова обработчика
            logger.info(f"--- Black List Middleware: Processing event of type {type(event).__name__} ---")
            black_list = await get_black_list()
            ids = [user.tg_id for user in black_list if user.tg_id is not None]
            usernames = [user.tg_username for user in black_list if user.tg_username is not None]
            
            if event.from_user.id in ids or event.from_user.username in usernames:
                # Если пользователь не разрешен, отправляем сообщение и прерываем цепочку
                if isinstance(event, Message):
                    await event.reply(f"Ошибка подключения к боту (error code: blmw)")
                elif isinstance(event, CallbackQuery):
                    await event.answer(f"Ошибка подключения к боту (error code: blmw)", show_alert=True)
                return # Прерываем дальнейшую обработку 
            
            # Вызываем следующий обработчик в цепочке (это может быть другой middleware или конечный хендлер)
            result = await handler(event, data)
            # Логика, которая выполняется ПОСЛЕ вызова обработчика
            logger.info(f"--- Black List Middleware: Finished processing event of type {type(event).__name__} ---")
            return result               
        
        
            





