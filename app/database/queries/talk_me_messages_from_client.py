from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import TalkMeMessageFromClient
from sqlalchemy import select, update, delete, insert, desc


async def get_talk_me_message_from_client(tg_id):
    async with AsyncSessionLocal() as session:
        talk_me_message_from_client = await session.scalar(select(TalkMeMessageFromClient).where(TalkMeMessageFromClient.tg_id == tg_id))
        return talk_me_message_from_client

async def update_talk_me_message_from_client(talk_me_message_from_client):
    async with AsyncSessionLocal() as session:
        session.add(talk_me_message_from_client)
        await session.commit()

async def get_talk_me_messages_from_client():
    async with AsyncSessionLocal() as session:
        talk_me_messages_from_client = await session.execute(select(TalkMeMessageFromClient))
        return talk_me_messages_from_client.scalars().all()


async def create_talk_me_messages_from_client(items: list[dict]):
    async with AsyncSessionLocal() as session:
        await session.execute(insert(TalkMeMessageFromClient), items)
        await session.commit()
        
async def get_client_id(tg_id):
    async with AsyncSessionLocal() as session:
        last_talk_me_message_from_client = await session.scalar(
            select(TalkMeMessageFromClient)
            .where(TalkMeMessageFromClient.tg_id == tg_id)
            .order_by(desc(TalkMeMessageFromClient.created_at))
            .limit(1)
        )
        if last_talk_me_message_from_client:
            return last_talk_me_message_from_client.client_id




    
