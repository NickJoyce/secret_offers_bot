from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import ChannelPost
from sqlalchemy import select, update, delete, insert


async def get_channel_post(id):
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(ChannelPost).where(ChannelPost.id == id))
        return user


async def get_channel_posts():
    async with AsyncSessionLocal() as session:
        users = await session.execute(select(ChannelPost))
        return users.scalars().all()



