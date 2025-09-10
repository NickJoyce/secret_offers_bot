from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import ChannelPost
from sqlalchemy import select, update, delete, insert
from sqlalchemy import desc


async def get_channel_post(id):
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(ChannelPost).where(ChannelPost.id == id))
        return user


async def get_channel_posts():
    async with AsyncSessionLocal() as session:
        users = await session.execute(select(ChannelPost))
        return users.scalars().all()
    

async def get_last_channel_post():
    async with AsyncSessionLocal() as session:
        last_channel_post = await session.scalar(select(ChannelPost).order_by(desc(ChannelPost.created_at)))
        return last_channel_post
    
async def update_channel_post(channel_post):
    async with AsyncSessionLocal() as session:
        session.add(channel_post)
        await session.commit()



