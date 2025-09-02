from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import Newsletter
from sqlalchemy import select, update, delete, insert


async def get_newsletter(nl_id):
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(Newsletter).where(Newsletter.id == nl_id))
        return user

async def update_newsletter(newsletter):
    async with AsyncSessionLocal() as session:
        session.add(newsletter)
        await session.commit()

async def get_newsletters():
    async with AsyncSessionLocal() as session:
        users = await session.execute(select(Newsletter))
        return users.scalars().all()


async def create_newsletters(items: list[dict]):
    async with AsyncSessionLocal() as session:
        await session.execute(insert(Newsletter), items)
        await session.commit()
