from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import DeeplinkRequest
from sqlalchemy import select, update, delete, insert


async def create_deeplink_request(items: list[dict]):
    async with AsyncSessionLocal() as session:
        await session.execute(insert(DeeplinkRequest), items)
        await session.commit()

        
        
