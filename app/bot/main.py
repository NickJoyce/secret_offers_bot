import logging.config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from settings import TG_BOT_TOKEN, LOGGING, TG_ADMIN_IDS
from app.bot.modules.utils import ParseModes
from app.bot.modules.utils import escape_markdown_v2
from aiogram.types import LinkPreviewOptions



logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


bot = Bot(token=TG_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()


async def send_message_to_admin(message: str):
    parse_mode=ParseModes.MARKDOWN_V2
    message = escape_markdown_v2(message)
    for admin_id in TG_ADMIN_IDS:
        try:
            await bot.send_message(admin_id, message, parse_mode=parse_mode, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception as e:
            logger.error(f"send_message_to_admin: {e}")
            await bot.send_message(admin_id, f'{e}', parse_mode=parse_mode, link_preview_options=LinkPreviewOptions(is_disabled=True))


async def start_bot():
    await send_message_to_admin(f'Бот запущен')



async def stop_bot():
    await send_message_to_admin(f'Бот остановлен')
