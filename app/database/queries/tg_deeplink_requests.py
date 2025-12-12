from app.database.conn import AsyncSessionLocal
from app.database.conn import SyncSession
from app.database.models.tg_bot import DeeplinkRequest
from sqlalchemy import select, update, delete, insert





async def acreate_deeplink_request(item: dict) -> None:
    async with AsyncSessionLocal() as session:
        # 1. Создаем экземпляр модели из словаря
        new_request = DeeplinkRequest(**item)
        
        # 2. Добавляем в сессию
        session.add(new_request)
        
        # 3. Фиксируем изменения в БД
        await session.commit()
        
        # 4. Обновляем объект, чтобы подтянуть ID и другие поля, созданные БД
        await session.refresh(new_request)
        
        return new_request


def create_deeplink_request(items: list[dict]):
    with SyncSession.begin() as session:
        session.execute(insert(DeeplinkRequest), items)

        
        
