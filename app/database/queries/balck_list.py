from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import BlackList
from sqlalchemy import select, update, delete, insert


async def get_black_list():
    async with AsyncSessionLocal() as session:
        users = await session.execute(select(BlackList))
        return users.scalars().all()



        
        
