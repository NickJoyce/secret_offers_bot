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





logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/check-all-subscriptions", include_in_schema=False)
async def check_all_subscriptions(request: Request):
    """Проверяет подписку всех клиентов на канал и отправляет напоминание отписавшимся"""
    try:
        clients = [await get_client(tg_id=520704135)]
        unsubscribed = []
        errors = []

        for client in clients:
            try:
                await sleep(0.05) 
                chat_member = await bot.get_chat_member(chat_id=TG_CHANNEL_ID, user_id=client.tg_id)
                
                status = chat_member.status
                
                logger.info(f"status: {status}")
                
                # if status == 'left':
                #     # Пользователь отписался — шлём напоминание
                #     try:
                #         await sleep(0.05) 
                #         await bot.send_message(
                #             chat_id=client.tg_id,
                #             text=(
                #                 "👋 Привет! Мы заметили, что ты покинул(а) наш закрытый канал "
                #                 "«Подружки».\n\n"
                #                 "Там мы регулярно публикуем секретные скидки до 70% "
                #                 "на самые популярные услуги! 💎\n\n"
                #                 "Вернись, чтобы не пропустить выгодные предложения! 🔥"
                #             )
                #         )
                #         unsubscribed.append(client.tg_id)
                    # except Exception as e:
                    #     # Пользователь заблокировал бота
                    #     errors.append({"tg_id": client.tg_id, "error": str(e)})
            except Exception as e:
                # Ошибка при проверке (например, пользователь никогда не был в канале)
                errors.append({"tg_id": client.tg_id, "error": str(e)})

        return JSONResponse({
            "notified": len(unsubscribed),
            "errors": len(errors),
            "unsubscribed_ids": unsubscribed
        })
    except Exception as e:
        return JSONResponse({"error": traceback.format_exc()})