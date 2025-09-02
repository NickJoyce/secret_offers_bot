from app.database.conn import AsyncSessionLocal
from app.database.models.tg_bot import GreetingOffer
from sqlalchemy import select, update, delete, insert


async def get_greeting_offer(offer_id):
    async with AsyncSessionLocal() as session:
        greeting_offer = await session.scalar(select(GreetingOffer).where(GreetingOffer.id ==offer_id))
        return greeting_offer

async def update_greeting_offer(greeting_offer):
    async with AsyncSessionLocal() as session:
        session.add(greeting_offer)
        await session.commit()

async def get_greeting_offers():
    async with AsyncSessionLocal() as session:
        greeting_offers = await session.execute(select(GreetingOffer))
        return greeting_offers.scalars().all()


async def create_greeting_offers(items: list[dict]):
    async with AsyncSessionLocal() as session:
        await session.execute(insert(GreetingOffer), items)
        await session.commit()
