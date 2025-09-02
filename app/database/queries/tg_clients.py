from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import TgClient
from sqlalchemy import select, update, delete, insert


async def get_client(tg_id):
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(TgClient).where(TgClient.tg_id == tg_id))
        return user

async def update_client(client):
    async with AsyncSessionLocal() as session:
        session.add(client)
        await session.commit()

async def get_clients():
    async with AsyncSessionLocal() as session:
        users = await session.execute(select(TgClient))
        return users.scalars().all()


async def create_clients(items: list[dict]):
    async with AsyncSessionLocal() as session:
        await session.execute(insert(TgClient), items)
        await session.commit()
