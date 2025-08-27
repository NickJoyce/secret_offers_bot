from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import FirstStartMessage
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError
import logging
import asyncio

logger = logging.getLogger(__name__)



async def get_first_start_message(tg_id):
    async with AsyncSessionLocal() as session:
        first_start_message = await session.scalar(select(FirstStartMessage).where(FirstStartMessage.tg_id == tg_id))
        return first_start_message


async def update_first_start_message(first_start_message):
    async with AsyncSessionLocal() as session:
        session.add(first_start_message)
        await session.commit()


async def get_first_start_messages():
    async with AsyncSessionLocal() as session:
        first_start_messages = await session.execute(select(FirstStartMessage))
        return first_start_messages.scalars().all()


async def create_first_start_messages(items: list[dict]):
    try:
        async with AsyncSessionLocal() as session:
                await session.execute(insert(FirstStartMessage), items)
                await session.commit()
    except IntegrityError as e:
        logger.info(f"Обработана ошибка IntegrityError")
        # Пример использования asyncio.sleep() для задержки
        await asyncio.sleep(1)  # Задержка на 1 секунду

        