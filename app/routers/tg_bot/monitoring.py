from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
import logging
from fastapi.templating import Jinja2Templates
from settings.base import TEMPLATES_DIR, BASE_DIR, TG_CHANNEL_ID
from app.tasks.monitoring import is_subscriber
import traceback
from app.bot.main import bot
from app.database.queries.tg_clients import get_clients, get_client
from asyncio import sleep
from settings import TG_ADMIN_IDS





logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/check-all-subscriptions/{tg_id}", include_in_schema=False)
async def check_all_subscriptions(tg_id: int, request: Request):
    """Проверяет подписку всех клиентов на канал и отправляет напоминание отписавшимся"""
    try:
        clients = [await get_client(tg_id=tg_id)]
        # Не подписан
        not_subscribed = []
        # Отписался
        unsubscribed = []
        # Отправлено уведомление
        notified = []
        # Пользователь заблокировал бота
        bot_blocked = []
        # Подписан
        subscribed = []
        
        
        errors = []

        for client in clients:
            try:
                await sleep(0.05) 
                chat_member = await bot.get_chat_member(chat_id=TG_CHANNEL_ID, user_id=client.tg_id)
                
                status = chat_member.status
                
                logger.info(f"status: {status}")
                
                if status == 'left':
                    # добавляем список отписавшихся
                    unsubscribed.append(client.tg_id)
                    # Пользователь отписался — шлём напоминание
                    try:
                        await sleep(0.05) 
                        await bot.send_message(
                            chat_id=client.tg_id,
                            text=(
                                "👋 Привет! Мы заметили, что ты покинул(а) наш закрытый канал "
                                "«Подружки».\n\n"
                                "Там мы регулярно публикуем секретные скидки до 70% "
                                "на самые популярные услуги! 💎\n\n"
                                "Вернись, чтобы не пропустить выгодные предложения! 🔥"
                            )
                        )
                        notified.append(client.tg_id)
                    except Exception as e:
                        # Пользователь заблокировал бота
                        errors.append({"tg_id": client.tg_id, "error": str(e)})
                        bot_blocked.append(client.tg_id)
                elif status in ['member', 'administrator', 'creator']:
                    subscribed.append(client.tg_id)
                else:
                    errors.append({"tg_id": client.tg_id, "error": f"Неизвестный статус пользователя в канале: {status}"})
            except Exception as e:
                # Ошибка при проверке (например, пользователь никогда не был в канале)
                not_subscribed.append(client.tg_id) 
                errors.append({"tg_id": client.tg_id, "error": str(e)})

        for admin_id in TG_ADMIN_IDS:
            try:
                await bot.send_message(admin_id, (f"Проверка подписки всех клиентов на канал завершена.\n" 
                                                  f"Отправлено уведомлений: {len(notified)}.\n"
                                                  f"Отписавшихся: {len(unsubscribed)}.\n"
                                                  f"Блокировавших бота: {len(bot_blocked)}.\n"
                                                  f"Подписанных: {len(subscribed)}.\n"
                                                  f"Неподписанных: {len(not_subscribed)}.\n"
                                                  f"Ошибки: {errors}"))
            except Exception as e:
                await bot.send_message(admin_id, f'{e}')
                
        return JSONResponse({
            "notified": len(notified),
            "unsubscribed": len(unsubscribed),
            "bot_blocked": len(bot_blocked),
            "subscribed": len(subscribed),
            "not_subscribed": len(not_subscribed),
            "errors": len(errors),
        })
        
    except Exception as e:
        return JSONResponse({"error": traceback.format_exc()})