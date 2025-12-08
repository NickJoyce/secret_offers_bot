from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import Deeplink
from sqlalchemy import select, update, delete, insert


async def get_deeplink(id_):
    async with AsyncSessionLocal() as session:
        deeplink = await session.scalar(select(Deeplink).where(Deeplink.id == id_))
        return deeplink


        
        
