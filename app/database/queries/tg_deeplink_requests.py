from app.database.conn import AsyncSessionLocal
from app.database.conn import SyncSession
from app.database.models.tg_bot import DeeplinkRequest
from sqlalchemy import select, update, delete, insert





async def acreate_deeplink_request(items: list[dict]) -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(insert(DeeplinkRequest), items)
        await session.commit()




def create_deeplink_request(items: list[dict]):
    with SyncSession.begin() as session:
        session.execute(insert(DeeplinkRequest), items)

        
        
