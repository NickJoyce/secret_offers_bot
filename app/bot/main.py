import logging.config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from settings import TG_BOT_TOKEN, LOGGING, TG_ADMIN_IDS
from app.bot.modules.utils import ParseModes



logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


bot = Bot(token=TG_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()


async def send_message_to_admin(message: str):
    for admin_id in TG_ADMIN_IDS:
        try:
            await bot.send_message(admin_id, message, parse_mode=ParseModes.MARKDOWN_V2)
        except Exception as e:
            await bot.send_message(admin_id, f'{e}')


async def start_bot():
    await send_message_to_admin(f'Бот запущен')



async def stop_bot():
    await send_message_to_admin(f'Бот остановлен')
