from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import TgManager
from sqlalchemy import select, update, delete, insert


async def get_manager(tg_id):
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(TgManager).where(TgManager.tg_id == tg_id))
        return user

async def update_manager(manager):
    async with AsyncSessionLocal() as session:
        session.add(manager)
        await session.commit()

async def get_managers():
    async with AsyncSessionLocal() as session:
        users = await session.execute(select(TgManager))
        return users.scalars().all()


async def create_managers(items: list[dict]):
    async with AsyncSessionLocal() as session:
        await session.execute(insert(TgManager), items)
        await session.commit()
