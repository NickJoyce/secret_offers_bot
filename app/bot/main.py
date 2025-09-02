import logging.config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from settings import TG_BOT_TOKEN, LOGGING, TG_ADMIN_ID



logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


bot = Bot(token=TG_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()


async def start_bot():
    try:
        await bot.send_message(TG_ADMIN_ID, f'Бот запущен')
    except Exception as e:
        await bot.send_message(TG_ADMIN_ID, f'{e}')


async def stop_bot():
    try:
        await bot.send_message(TG_ADMIN_ID, 'Бот остановлен')
    except Exception as e:
        await bot.send_message(TG_ADMIN_ID, f'{e}')