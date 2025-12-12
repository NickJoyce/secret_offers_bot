from app.database.conn import AsyncSessionLocal
from app.database.conn import SyncSession
from app.database.models.tg_bot import DeeplinkRequest
from sqlalchemy import select, update, delete, insert


def create_deeplink_request(item: dict) -> None:
    with SyncSession.begin() as session:
        session.execute(insert(DeeplinkRequest), item)


async def acreate_deeplink_request(item: dict) -> None:
    async with AsyncSessionLocal() as session:
        await session.execute(insert(DeeplinkRequest), item)
        await session.commit()

        
        
