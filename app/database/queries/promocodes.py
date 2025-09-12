from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import Promocode
from sqlalchemy import select, update, delete, insert


async def get_promocode(promocode_id):
    async with AsyncSessionLocal() as session:
        promocode = await session.scalar(select(Promocode).where(Promocode.id == promocode_id))
        return promocode

async def get_promocode_by_value(value: str):
    async with AsyncSessionLocal() as session:
        promocode = await session.scalar(select(Promocode).where(Promocode.value == value))
        return promocode



async def get_promocode():
    async with AsyncSessionLocal() as session:
        promocodes = await session.execute(select(Promocode))
        return promocodes.scalars().all()


async def create_promocodes(items: list[dict]):
    async with AsyncSessionLocal() as session:
        await session.execute(insert(Promocode), items)
        await session.commit()
