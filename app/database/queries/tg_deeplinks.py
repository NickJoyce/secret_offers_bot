from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import DeepLink
from sqlalchemy import select, update, delete, insert


async def get_deeplink(id_):
    async with AsyncSessionLocal() as session:
        deeplink = await session.scalar(select(DeepLink).where(DeepLink.id == id_))
        return deeplink


        
        
